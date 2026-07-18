# Reproducible unified env build (Windows, Python 3.11).
#
# torch (cu121), audio-separator and aubio are installed via pip in a specific
# ORDER on top of Poetry's core deps. `poetry install` alone is NOT enough (it
# would pull CPU torch + numpy>=2). Always use this script for a fresh build.
#
#   powershell -ExecutionPolicy Bypass -File .\scripts\setup_env.ps1
$ErrorActionPreference = "Stop"
# This script lives in scripts/ but the venv + pyproject live at the repo root.
Set-Location (Split-Path $PSScriptRoot -Parent)

Write-Host "[1/5] Poetry core deps + venv (Python 3.11)" -ForegroundColor Cyan
poetry env use "C:\Program Files\Python311\python.exe"
poetry install --no-root

$py = ".\.venv\Scripts\python.exe"

Write-Host "[2/5] torch + torchaudio + torchvision (cu121)" -ForegroundColor Cyan
& $py -m pip install torch==2.4.1 torchvision==0.19.1 torchaudio==2.4.1 `
    --index-url https://download.pytorch.org/whl/cu121

Write-Host "[3/5] audio-separator (pinned 0.28; numpy<2)" -ForegroundColor Cyan
& $py -m pip install "audio-separator[gpu]>=0.28,<0.29"

Write-Host "[4/5] restore cu121 torch trio (0.28 pulls CPU torch)" -ForegroundColor Cyan
& $py -m pip install --force-reinstall --no-deps torch==2.4.1 torchvision==0.19.1 torchaudio==2.4.1 `
    --index-url https://download.pytorch.org/whl/cu121

Write-Host "[5/5] aubio (BPM tracker)" -ForegroundColor Cyan
& $py -m pip install aubio

Write-Host "`nVerifying imports + CUDA..." -ForegroundColor Cyan
& $py -c "import torch,numpy,aubio,pydub,yt_dlp,slugify; from audio_separator.separator import Separator; print('OK torch',torch.__version__,'cuda',torch.cuda.is_available(),'numpy',numpy.__version__)"
Write-Host "Done." -ForegroundColor Green
