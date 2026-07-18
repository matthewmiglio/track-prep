"""CLI: detect BPM, cut to start/end on a beat, print summary.

    python bpm_inference/cli.py INPUT.mp3 [OUTPUT_FOLDER]
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bpm_inference.bpm import extract_and_cut  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description="Extract BPM and beat-snap-trim a track.")
    ap.add_argument("input", type=Path, help="Source mp3 (or any audio).")
    ap.add_argument("output", nargs="?", default=None, help="Output folder (default: next to input).")
    args = ap.parse_args()

    if not args.input.exists():
        print(f"ERROR: input not found: {args.input}", file=sys.stderr)
        return 2

    print(f"[+] analyzing {args.input.name} ...")
    r = extract_and_cut(args.input, args.output)

    print("\n=== summary ===")
    print(f"detected BPM : {r['bpm']:.1f}")
    print(f"total beats  : {r['n_beats']}")
    print(f"cut window   : {r['t0']:.2f}s -> {r['t1']:.2f}s  ({r['duration']:.2f}s)")
    print(f"output       : {r['output']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
