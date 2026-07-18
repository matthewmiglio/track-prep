"""/process-new-sample orchestrator: separate + BPM + beat-cut BOTH stems in sync.

    python process_sample.py INPUT.(mp4|mp3|...) [OUTPUT_FOLDER]

Pipeline:
  1. convert -> mp3 and separate into vocals + instrumental
  2. detect BPM + beats on the instrumental (the reliable beat source)
  3. cut BOTH stems to the SAME [first_beat, last_beat] window (start/end on a
     beat, stays sample-aligned)
  4. save <name>-<bpm>bpm-<beatcount>bars-<instrumental|vocals>.mp3
"""
from __future__ import annotations
import argparse
import sys
import tempfile
from pathlib import Path

# run-as-script from scripts/: put the repo root on sys.path so the modules import.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.audio import as_mp3_source, load_segment, export_segment, resolve_out_dir
from separate_song.separator import separate_stems
from bpm_inference.bpm import detect_bpm_beats, cut_to_beats


def main() -> int:
    ap = argparse.ArgumentParser(description="Separate + BPM + beat-cut both stems in sync.")
    ap.add_argument("input", type=Path, help="Source mp4/mp3/wav/...")
    ap.add_argument("output", nargs="?", default=None, help="Output folder (default: next to input).")
    args = ap.parse_args()

    src: Path = args.input
    if not src.exists():
        print(f"ERROR: input not found: {src}", file=sys.stderr)
        return 2

    # ponytail: explicit output overrides both; otherwise stems split to their default homes.
    if args.output:
        inst_dir = voc_dir = resolve_out_dir(src, args.output)
    else:
        inst_dir = Path(r"E:\my_files\my audio\Samples\_full_songs")
        voc_dir = Path(r"E:\my_files\my audio\Samples\_full_lyrics")
        inst_dir.mkdir(parents=True, exist_ok=True)
        voc_dir.mkdir(parents=True, exist_ok=True)
    stem = src.stem

    with tempfile.TemporaryDirectory(prefix="proc_") as tmp:
        mp3 = as_mp3_source(src, tmp)
        print(f"[+] separating {src.name} ...")
        vocals_wav, inst_wav = separate_stems(mp3, tmp)

        print("[+] detecting BPM + beats on instrumental ...")
        bpm, beats = detect_bpm_beats(inst_wav, tmp)
        bpm_i, n_beats = int(round(bpm)), len(beats)

        # same cut window for both stems -> they stay in sync
        inst_cut, t0, t1 = cut_to_beats(load_segment(inst_wav), beats)
        voc_cut, _, _ = cut_to_beats(load_segment(vocals_wav), beats)

        inst_out = inst_dir / f"{stem}-{bpm_i}bpm-{n_beats}bars-instrumental.mp3"
        voc_out = voc_dir / f"{stem}-{bpm_i}bpm-{n_beats}bars-vocals.mp3"
        export_segment(inst_cut, inst_out)
        export_segment(voc_cut, voc_out)

    print("\n=== summary ===")
    print(f"detected BPM : {bpm:.1f}  (filename: {bpm_i}bpm)")
    print(f"total beats  : {n_beats}")
    print(f"cut window   : {t0:.2f}s -> {t1:.2f}s  ({inst_cut.duration_seconds:.2f}s)")
    print(f"instrumental -> {inst_out}")
    print(f"vocals       -> {voc_out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
