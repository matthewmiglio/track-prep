"""BPM detection (aubio) + beat-snap cutting.

aubio was selected as the production tempo tracker in the benchmark
(bpm-detection-benchmarking): lightest weight, fastest, and accurate.
"""
from __future__ import annotations
import tempfile
from pathlib import Path

import numpy as np

from common.audio import ensure_wav, load_segment, export_segment, resolve_out_dir


def detect_bpm_beats(audio_path: Path, tmp: str):
    """Run aubio on `audio_path`; return (bpm, beat_times[seconds] ndarray)."""
    import aubio

    wav = ensure_wav(audio_path, tmp)
    win_s, hop_s = 1024, 512
    src = aubio.source(str(wav), 0, hop_s)  # 0 = keep file samplerate
    tempo = aubio.tempo("default", win_s, hop_s, src.samplerate)

    beats = []
    while True:
        samples, read = src()
        if tempo(samples):
            beats.append(tempo.get_last_s())
        if read < hop_s:
            break

    beats = np.asarray(beats, dtype=float)
    bpm = float(60.0 / np.median(np.diff(beats))) if beats.size > 1 else 0.0
    return bpm, beats


def beat_edge_seconds(beat_times):
    """First/last beat in seconds, or (None, None) if there aren't enough beats."""
    bt = np.asarray(beat_times, dtype=float)
    if bt.size < 2:
        return None, None
    return float(bt.min()), float(bt.max())


def cut_to_beats(seg, beat_times):
    """Slice a pydub segment to [first_beat, last_beat]. Returns (seg, t0, t1)."""
    t0, t1 = beat_edge_seconds(beat_times)
    if t0 is None:
        print("[warn] <2 beats detected -> not cutting (keeping full track)")
        return seg, 0.0, seg.duration_seconds
    return seg[t0 * 1000.0: t1 * 1000.0], t0, t1


def extract_and_cut(src: Path, out_folder=None):
    """Detect BPM, cut src to start/end on a beat, save <name>-cut.mp3.

    Returns dict(bpm, n_beats, t0, t1, duration, output). out_folder=None -> sister.
    """
    src = Path(src)
    out_dir = resolve_out_dir(src, out_folder)
    out = out_dir / f"{src.stem}-cut.mp3"

    with tempfile.TemporaryDirectory(prefix="bpm_") as tmp:
        bpm, beats = detect_bpm_beats(src, tmp)
        cut, t0, t1 = cut_to_beats(load_segment(src), beats)
        export_segment(cut, out)

    return {
        "bpm": bpm, "n_beats": int(len(beats)), "t0": t0, "t1": t1,
        "duration": cut.duration_seconds, "output": out,
    }
