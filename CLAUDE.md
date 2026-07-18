# CLAUDE.md — lay of the land

Audio sample-prep toolkit. One shared Poetry venv, four focused CLI modules + one
orchestrator. Windows, Python 3.11, cu121 torch, ffmpeg on PATH.

Run everything with the shared venv: `.\.venv\Scripts\python.exe <module>\cli.py ...`

## Modules

| Dir | Does | Entry | Output |
|-----|------|-------|--------|
| `separate_song/` | Vocal/instrumental split (BS-RoFormer) | `separate_song\cli.py IN [OUT]` | `-instrumental.mp3`, `-vocals.mp3` |
| `bpm_inference/` | BPM detect (aubio) + beat-snap cut | `bpm_inference\cli.py IN [OUT]` | `-cut.mp3`, prints BPM + beats |
| `youtube_download/` | YouTube URL → 320k mp3, slug-named | `youtube_download\cli.py -o OUT URL...` | `<slug>.mp3` |
| `declicker/` | Remove clicks/pops (ffmpeg adeclip) | `declicker\cli.py IN [OUT]` | `-declicked.mp3` |
| `scripts/process_sample.py` | Full pipeline: separate + BPM + synced cut of both stems | `scripts\process_sample.py IN [OUT]` | `-<bpm>bpm-<beats>bars-{instrumental,vocals}.mp3` |

`OUT` folder is optional on the single-file modules → writes next to input.

## Shared

- `common/config.py` — model paths (`D:\ai-models\audio-models`).
- `common/audio.py` — load/export/convert/slugify/output-dir helpers.
- `scripts/setup_env.ps1` — **the** way to build the env (order-sensitive; plain `poetry install` gets CPU torch + numpy 2 and breaks things).
- `scripts/separate.py`, `scripts/batch_separate.py` — legacy, superseded by `separate_song/`.

## Skills

`.claude/skills/` wrap the modules as slash commands: `/separate`, `/bpm-extract`,
`/process-new-sample`, `/download-songs`, `/import-spotify-local-song`.

## Gotcha

Numba `UnpicklingError: invalid load key` = corrupt cache. Clear it:
`Get-ChildItem .venv\Lib\site-packages -Recurse -Include *.nbi,*.nbc | Remove-Item -Force`

Full detail (setup, model download, why aubio/adeclip won their bench-offs): see `README.md`.
