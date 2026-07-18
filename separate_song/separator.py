"""Vocal / instrumental separation using BS-RoFormer (audio-separator)."""
from __future__ import annotations
import tempfile
from pathlib import Path

from common import config
from common.audio import as_mp3_source, load_segment, export_segment, resolve_out_dir


def separate_stems(audio_path: Path, tmp: str):
    """Separate `audio_path` into (vocals_wav, instrumental_wav) inside `tmp`.

    Loads the BS-RoFormer model once from the shared model cache.
    """
    from audio_separator.separator import Separator

    sep = Separator(
        output_dir=tmp,
        output_format="WAV",
        log_level=30,
        model_file_dir=str(config.SEPARATOR_DIR),
    )
    sep.load_model(model_filename=config.SEPARATOR_MODEL)
    produced = [Path(tmp) / f for f in sep.separate(str(audio_path))]

    vocals = next((p for p in produced if "vocals" in p.name.lower()), None)
    inst = next((p for p in produced if p != vocals), None)
    if vocals is None or inst is None:
        raise RuntimeError(f"could not classify separator outputs: {produced}")
    return vocals, inst


def separate_to_files(src: Path, out_folder=None):
    """Convert src->mp3, separate, export <name>-instrumental.mp3 + <name>-vocals.mp3.

    Returns (instrumental_path, vocals_path). out_folder=None -> sister files.
    """
    src = Path(src)
    out_dir = resolve_out_dir(src, out_folder)
    stem = src.stem
    inst_out = out_dir / f"{stem}-instrumental.mp3"
    voc_out = out_dir / f"{stem}-vocals.mp3"

    with tempfile.TemporaryDirectory(prefix="sep_") as tmp:
        mp3 = as_mp3_source(src, tmp)
        vocals_wav, inst_wav = separate_stems(mp3, tmp)
        export_segment(load_segment(inst_wav), inst_out)
        export_segment(load_segment(vocals_wav), voc_out)

    return inst_out, voc_out
