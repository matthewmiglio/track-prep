"""CLI: separate a track into vocals + instrumental mp3s.

    python separate_song/cli.py INPUT.(mp4|mp3|...) [OUTPUT_FOLDER]
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path

# allow running as a plain script (python separate_song/cli.py ...)
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from separate_song.separator import separate_to_files  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description="Separate a track into vocals + instrumental mp3s.")
    ap.add_argument("input", type=Path, help="Source mp4/mp3/wav/...")
    ap.add_argument("output", nargs="?", default=None, help="Output folder (default: next to input).")
    args = ap.parse_args()

    if not args.input.exists():
        print(f"ERROR: input not found: {args.input}", file=sys.stderr)
        return 2

    print(f"[+] separating {args.input.name} ...")
    inst_out, voc_out = separate_to_files(args.input, args.output)

    print("\n=== done ===")
    print(f"instrumental -> {inst_out}")
    print(f"vocals       -> {voc_out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
