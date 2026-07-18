"""Download YouTube URLs as highest-quality mp3s, named by slugified video title."""
from __future__ import annotations
from pathlib import Path

from common.audio import slugify_title


def download_urls(urls, out_folder, bitrate: str = "320", retries: int = 3):
    """Download each URL to out_folder as <slug-of-title>.mp3 at the best quality.

    Returns a list of result dicts: {url, title, slug, path, ok, error}.
    One failing URL does not stop the batch. Each URL is retried up to
    `retries` times (transient 403s from YouTube are common).
    """
    import time
    import yt_dlp

    out_dir = Path(out_folder)
    out_dir.mkdir(parents=True, exist_ok=True)
    results = []

    for url in urls:
        rec = {"url": url, "title": None, "slug": None, "path": None, "ok": False, "error": None}
        for attempt in range(1, retries + 1):
          try:
            # 1) probe for the title so we can slugify the filename ourselves
            with yt_dlp.YoutubeDL({"quiet": True, "no_warnings": True, "noplaylist": True}) as ydl:
                info = ydl.extract_info(url, download=False)
            title = info.get("title", info.get("id", "track"))
            slug = slugify_title(title)
            rec["title"], rec["slug"] = title, slug

            # 2) download bestaudio -> mp3 at the requested bitrate
            opts = {
                "quiet": True,
                "no_warnings": True,
                "noplaylist": True,
                "format": "bestaudio/best",
                "outtmpl": str(out_dir / f"{slug}.%(ext)s"),
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": bitrate,
                }],
            }
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([url])

            path = out_dir / f"{slug}.mp3"
            rec["path"] = path
            rec["ok"] = path.exists()
            if not rec["ok"]:
                rec["error"] = "mp3 not found after download"
            else:
                rec["error"] = None
                break  # success
          except Exception as exc:  # noqa: BLE001 - keep the batch going
            rec["error"] = f"{type(exc).__name__}: {exc} (attempt {attempt}/{retries})"
          if attempt < retries:
            time.sleep(2 * attempt)  # ponytail: linear backoff, swap for jitter if YT rate-limits harder
        results.append(rec)

    return results
