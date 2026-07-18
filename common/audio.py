"""Shared audio helpers: format conversion, mp3 export, slugify, output-dir logic."""
from __future__ import annotations
from pathlib import Path


def resolve_out_dir(src: Path, out_folder) -> Path:
    """Output dir: the given folder, or the input's own folder (sister files)."""
    d = Path(out_folder) if out_folder else Path(src).parent
    d.mkdir(parents=True, exist_ok=True)
    return d


def load_segment(path: Path):
    """Load any audio/video file as a pydub AudioSegment (via ffmpeg)."""
    from pydub import AudioSegment
    return AudioSegment.from_file(str(path))


def export_segment(seg, path: Path, bitrate: str = "320k") -> Path:
    """Export a pydub AudioSegment to mp3."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    seg.export(str(path), format="mp3", bitrate=bitrate)
    return path


def ensure_wav(path: Path, tmp: str) -> Path:
    """Return a .wav for `path` (convert via pydub if needed). aubio reads wav best."""
    path = Path(path)
    if path.suffix.lower() == ".wav":
        return path
    out = Path(tmp) / (path.stem + ".wav")
    load_segment(path).export(str(out), format="wav")
    return out


def as_mp3_source(src: Path, tmp: str) -> Path:
    """Ensure an mp3 source for separation (convert only if not already mp3)."""
    src = Path(src)
    if src.suffix.lower() == ".mp3":
        return src
    out = Path(tmp) / (src.stem + ".mp3")
    return export_segment(load_segment(src), out)


def slugify_title(title: str) -> str:
    """Slugify a string into a safe filename stem (lowercase, hyphenated)."""
    from slugify import slugify
    return slugify(title) or "track"
