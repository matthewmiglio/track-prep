"""Split a music track into vocals + instrumental stems using BS-RoFormer (viperx).

Usage:
    poetry run python separate.py -i SONG.mp3 -v VOCALS.wav -n INSTRUMENTAL.wav
"""
from __future__ import annotations
import argparse
import shutil
import sys
import tempfile
from pathlib import Path

MODEL_FILENAME = "model_bs_roformer_ep_317_sdr_12.9755.ckpt"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Separate vocals from instrumental using BS-RoFormer.")
    p.add_argument("-i", "--input", required=True, type=Path,
                   help="Source music file (mp3, wav, flac, etc.)")
    p.add_argument("-v", "--vocals", required=True, type=Path,
                   help="Output path for the vocals stem (e.g. vocals.wav)")
    p.add_argument("-n", "--instrumental", required=True, type=Path,
                   help="Output path for the instrumental stem (e.g. instrumental.wav)")
    return p.parse_args()


def main() -> int:
    args = parse_args()

    src: Path = args.input
    if not src.exists():
        print(f"ERROR: input not found: {src}", file=sys.stderr)
        return 2

    for out in (args.vocals, args.instrumental):
        out.parent.mkdir(parents=True, exist_ok=True)

    from audio_separator.separator import Separator

    with tempfile.TemporaryDirectory(prefix="ils_") as tmp:
        sep = Separator(
            output_dir=tmp,
            output_format="WAV",
            log_level=30,
        )
        print(f"[+] loading model {MODEL_FILENAME}...")
        sep.load_model(model_filename=MODEL_FILENAME)
        print(f"[+] separating {src.name}...")
        produced = sep.separate(str(src))
        paths = [Path(tmp) / f for f in produced]

        vocals_src = next((p for p in paths if "vocals" in p.name.lower()), None)
        inst_src = next((p for p in paths if p != vocals_src), None)
        if vocals_src is None or inst_src is None:
            print(f"ERROR: could not classify outputs: {paths}", file=sys.stderr)
            return 3

        shutil.move(str(vocals_src), str(args.vocals))
        shutil.move(str(inst_src), str(args.instrumental))

    print(f"[ok] vocals       -> {args.vocals}")
    print(f"[ok] instrumental -> {args.instrumental}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
