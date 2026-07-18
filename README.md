# Instrumental / Lyric Separator — audio toolkit

A small toolkit for prepping music samples: **download** from YouTube, **separate**
vocals from instrumental (BS-RoFormer), and **detect BPM + beat-cut** tracks so they
start and end on a beat. One unified Poetry environment, four focused modules.

## Layout

```
intrumental-lyric-separator/
  pyproject.toml          unified env (Poetry core deps)
  .venv/                  the one shared venv
  common/                 shared helpers
    config.py             model paths (D:\ai-models\audio-models)
    audio.py              load/export/convert/slugify/output-dir
  separate_song/          vocal / instrumental separation (BS-RoFormer)
    separator.py  cli.py
  bpm_inference/          BPM detection (aubio) + beat-snap cutting
    bpm.py        cli.py
  youtube_download/       download YouTube URLs -> highest-quality mp3 (slug names)
    downloader.py cli.py
  declicker/              remove clicks/pops (ffmpeg adeclip, won a 5-method bench)
    declick.py    cli.py
  scripts/                runnable scripts + env build
    setup_env.ps1         reproducible env build (run this, not `poetry install` alone)
    process_sample.py     orchestrator: separate + BPM + cut both stems in sync
    separate.py           (legacy) single-file separation, superseded by separate_song
    batch_separate.py     (legacy) folder batch separation
```

The `scripts/separate.py` / `scripts/batch_separate.py` are the original
single-file scripts, superseded by the `separate_song` module.

## Setup (Windows, Python 3.11)

The stack is order-sensitive (cu121 torch, a numpy<2 pin, a compiled aubio build),
so build it with the script:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\setup_env.ps1
```

`poetry install` alone is **not** sufficient (it pulls CPU torch + numpy>=2).
Requires a C compiler (aubio build), `ffmpeg` on PATH, and an NVIDIA GPU for cu121.

> Numba cache note: if a run dies with `UnpicklingError: invalid load key`, the
> on-disk numba cache got corrupted. Clear it:
> `Get-ChildItem .venv\Lib\site-packages -Recurse -Include *.nbi,*.nbc | Remove-Item -Force`

## Modules / usage

All commands use the shared venv: `.\.venv\Scripts\python.exe`.

### separate_song — vocals + instrumental
```powershell
.\.venv\Scripts\python.exe separate_song\cli.py "song.mp4" "out_folder"
```
→ `out_folder\song-instrumental.mp3`, `out_folder\song-vocals.mp3`
(output folder optional → sister files next to input).

### bpm_inference — BPM + beat-snap cut
```powershell
.\.venv\Scripts\python.exe bpm_inference\cli.py "song.mp3" "out_folder"
```
→ `out_folder\song-cut.mp3`; prints detected BPM + total beats.

### declicker — remove clicks/pops
```powershell
.\.venv\Scripts\python.exe declicker\cli.py "sample.mp3" "out_folder"
```
→ `out_folder\sample-declicked.mp3`. Uses ffmpeg `adeclip`, which won an audible
5-method bench-off (vs `adeclick`, a scipy median/MAD declicker, `noisereduce`,
and DeepFilterNet) — the two denoisers gutted the audio, median went lo-fi.

### youtube_download — URLs to mp3
```powershell
.\.venv\Scripts\python.exe youtube_download\cli.py -o "out_folder" "<url1>" "<url2>"
# or:  --from-file urls.txt
```
→ highest-quality 320k mp3s named `<slug-of-video-title>.mp3`.

### process_sample — full pipeline (separate + BPM + synced cut)
```powershell
.\.venv\Scripts\python.exe scripts\process_sample.py "song.mp4" "out_folder"
```
→ `song-<bpm>bpm-<beats>bars-instrumental.mp3` and `...-vocals.mp3`, both cut to the
**same** beat window so they stay sample-aligned. BPM is detected on the instrumental
(cleaner onsets). The `bars` slot holds the beat count.

## Skills (project-local slash commands)

`.claude/skills/` — each calls the matching module with the shared venv:

| Skill | Module |
|-------|--------|
| `/separate {in} {out?}` | separate_song |
| `/bpm-extract {in} {out?}` | bpm_inference |
| `/process-new-sample {in} {out?}` | scripts/process_sample.py |
| `/download-songs {out} {url...}` | youtube_download |
| `/import-spotify-local-song {url}` | youtube_download → `E:\my_files\my audio\spotify local songs` |

## Models

`D:\ai-models\audio-models\separator\` — BS-RoFormer checkpoint (~639 MB), auto-
downloaded on first separation and reused thereafter.

## BPM method

`aubio` was chosen after an audible 5-method bench-off (librosa, aubio, madmom,
beat_this, BeatNet): lightest weight, fastest, and accurate. The benchmark suite
that decided this has since been removed.
