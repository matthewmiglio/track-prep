"""CLI: download YouTube URLs as highest-quality mp3s (slugified titles).

    python youtube_download/cli.py -o OUTPUT_DIR URL [URL ...]
    python youtube_download/cli.py -o OUTPUT_DIR --from-file urls.txt
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from youtube_download.downloader import download_urls  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description="Download YouTube URLs as mp3s.")
    ap.add_argument("urls", nargs="*", help="YouTube URLs.")
    ap.add_argument("-o", "--out", required=True, type=Path, help="Output directory.")
    ap.add_argument("--from-file", type=Path, default=None,
                    help="Read additional URLs from a file (one per line).")
    ap.add_argument("--bitrate", default="320", help="mp3 bitrate (default 320).")
    args = ap.parse_args()

    urls = list(args.urls)
    if args.from_file:
        urls += [ln.strip() for ln in args.from_file.read_text(encoding="utf-8").splitlines()
                 if ln.strip() and not ln.strip().startswith("#")]
    if not urls:
        print("ERROR: no URLs given (positional or --from-file).", file=sys.stderr)
        return 2

    print(f"[+] downloading {len(urls)} url(s) -> {args.out}")
    results = download_urls(urls, args.out, bitrate=args.bitrate)

    print("\n=== summary ===")
    ok = 0
    for r in results:
        if r["ok"]:
            ok += 1
            print(f"[ok]   {r['slug']}.mp3   ({r['title']})")
        else:
            print(f"[fail] {r['url']}  -> {r['error']}")
    print(f"\n{ok}/{len(results)} downloaded into {args.out}")
    return 0 if ok == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
