"""Shared paths/config for all modules.

Models live under MODELS_DIR (off the system drive). The BS-RoFormer separator
checkpoint is cached there and reused by separate_song.
"""
from __future__ import annotations
from pathlib import Path

MODELS_DIR = Path(r"D:\ai-models\audio-models")
SEPARATOR_DIR = MODELS_DIR / "separator"
SEPARATOR_MODEL = "model_bs_roformer_ep_317_sdr_12.9755.ckpt"

REPO_DIR = Path(__file__).resolve().parents[1]

SEPARATOR_DIR.mkdir(parents=True, exist_ok=True)
