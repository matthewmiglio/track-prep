"""Batch-separate every audio file in a folder into vocals + instrumental.

Loads the BS-RoFormer model once and reuses it for every track.

Usage:
    poetry run python batch_separate.py `
        -i  "C:\\Users\\matt\\Downloads\\xxxtentacion\\songs" `
        -v  "D:\\my_files\\my audio\\Samples\\xxxtentacion\\vocals" `
        -n  "D:\\my_files\\my audio\\Samples\\xxxtentacion\\instrumentals"
"""
from __future__ import annotations
import argparse
import shutil
import sys
import tempfile
import time
from pathlib import Path

# Filenames may contain non-cp1252 characters (e.g. fullwidth bar U+FF5C).
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

MODEL_FILENAME = "model_bs_roformer_ep_317_sdr_12.9755.ckpt"
AUDIO_EXTS = {".mp3", ".wav", ".flac", ".m4a", ".ogg", ".aac", ".wma"}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Batch vocal/instrumental separation with BS-RoFormer.")
    p.add_argument("-i", "--input-dir", required=True, type=Path)
    p.add_argument("-v", "--vocals-dir", required=True, type=Path)
    p.add_argument("-n", "--instrumentals-dir", required=True, type=Path)
    p.add_argument("--overwrite", action="store_true",
                   help="Re-process tracks even if outputs already exist.")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    src_dir: Path = args.input_dir
    if not src_dir.is_dir():
        print(f"ERROR: not a directory: {src_dir}", file=sys.stderr)
        return 2

    args.vocals_dir.mkdir(parents=True, exist_ok=True)
    args.instrumentals_dir.mkdir(parents=True, exist_ok=True)

    tracks = sorted([p for p in src_dir.iterdir()
                     if p.is_file() and p.suffix.lower() in AUDIO_EXTS])
    if not tracks:
        print("No audio files found.")
        return 1

    print(f"[+] {len(tracks)} tracks queued")

    from audio_separator.separator import Separator

    with tempfile.TemporaryDirectory(prefix="ils_batch_") as tmp:
        sep = Separator(output_dir=tmp, output_format="WAV", log_level=30)
        print(f"[+] loading {MODEL_FILENAME} (one-time)...")
        sep.load_model(model_filename=MODEL_FILENAME)

        ok = 0
        skipped = 0
        failed: list[str] = []
        t_start = time.time()

        for idx, track in enumerate(tracks, 1):
            stem = track.stem
            voc_out = args.vocals_dir / f"{stem}.wav"
            inst_out = args.instrumentals_dir / f"{stem}.wav"

            if not args.overwrite and voc_out.exists() and inst_out.exists():
                print(f"[{idx:>3}/{len(tracks)}] skip (already done): {stem}")
                skipped += 1
                continue

            t0 = time.time()
            print(f"[{idx:>3}/{len(tracks)}] {stem}")
            try:
                # Clear tmp from any prior iteration's stray files so classification stays clean.
                for f in Path(tmp).iterdir():
                    if f.is_file():
                        f.unlink(missing_ok=True)
                produced = sep.separate(str(track))
                paths = [Path(tmp) / f for f in produced]
                vocals_src = next((p for p in paths if "vocals" in p.name.lower()), None)
                inst_src = next((p for p in paths if p != vocals_src), None)
                if vocals_src is None or inst_src is None:
                    raise RuntimeError(f"could not classify outputs: {paths}")
                shutil.move(str(vocals_src), str(voc_out))
                shutil.move(str(inst_src), str(inst_out))
                ok += 1
                print(f"        ok ({time.time() - t0:.1f}s)")
            except Exception as e:
                failed.append(f"{stem}: {type(e).__name__}: {e}")
                print(f"        FAIL: {e}")

        elapsed = time.time() - t_start
        print(f"\n=== {ok} ok, {skipped} skipped, {len(failed)} failed in {elapsed:.0f}s ===")
        for line in failed:
            print(f"  - {line}")
        return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
