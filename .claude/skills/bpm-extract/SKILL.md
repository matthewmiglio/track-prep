---
name: bpm-extract
description: Detect a track's BPM and cut it so it starts and ends on a beat, then print beat count + detected BPM. Use when the user runs /bpm-extract, or asks to get the BPM/tempo of a track, beat-trim/beat-snap a clip, or cut audio to a beat. Takes an input mp3 and an optional output folder.
---

# /bpm-extract

Detect BPM with aubio, trim the track to its first/last detected beat, save the
cut mp3, and print a summary (total beats + detected BPM).

## Arguments
`/bpm-extract {input mp3} {output folder}`
- **input** (required): the source mp3 (or any audio file).
- **output folder** (optional): where to save the cut file. If omitted, it is
  written next to the input file (sister file) as `<name>-cut.mp3`.

## How to run
Run the `bpm_inference` module with the project's unified venv:

```powershell
& "C:\My_Files\my_programs\intrumental-lyric-separator\.venv\Scripts\python.exe" `
  "C:\My_Files\my_programs\intrumental-lyric-separator\bpm_inference\cli.py" `
  "<input>" "<output folder>"
```

Omit the second argument entirely if the user did not give an output folder.
Always double-quote both paths.

## After running
Report the script's `=== summary ===`: detected BPM, total beats, the cut window,
and the output path.
