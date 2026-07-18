"""Declick a sample with ffmpeg's adeclip (autoregressive de-clipping).

adeclip won a 5-method bench-off (vs adeclick, a scipy median/MAD declicker,
noisereduce, and DeepFilterNet) on a real sample: cleanest result. The two
denoisers (noisereduce, DeepFilterNet) gutted the audio; the median filter went
lo-fi/"radio". adeclip repairs only the damaged samples via AR interpolation and
leaves the rest of the track untouched.
"""
from __future__ import annotations
import subprocess
from pathlib import Path

from common.audio import resolve_out_dir


def declick(src, out_folder=None) -> Path:
    """mp3 -> ffmpeg adeclip -> <stem>-declicked.mp3 (320k). Returns the output path."""
    src = Path(src)
    out = resolve_out_dir(src, out_folder) / f"{src.stem}-declicked.mp3"
    subprocess.run(
        ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
         "-i", str(src), "-af", "adeclip", "-b:a", "320k", str(out)],
        check=True,
    )
    return out
