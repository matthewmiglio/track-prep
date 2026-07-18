"""CLI: declick a sample with ffmpeg adeclip.

    python declicker/cli.py INPUT.mp3 [OUTPUT_FOLDER]
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from declicker.declick import declick  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description="Declick a sample (ffmpeg adeclip).")
    ap.add_argument("input", type=Path, help="Source mp3 (or any audio).")
    ap.add_argument("output", nargs="?", default=None, help="Output folder (default: next to input).")
    args = ap.parse_args()

    if not args.input.exists():
        print(f"ERROR: input not found: {args.input}", file=sys.stderr)
        return 2

    out = declick(args.input, args.output)
    print(f"[+] declicked -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
