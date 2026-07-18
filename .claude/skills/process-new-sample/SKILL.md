---
name: process-new-sample
description: Full sample-prep pipeline — separate a track into vocals + instrumental, detect BPM, and beat-cut BOTH stems to the same window so they stay in sync. Use when the user runs /process-new-sample, or asks to fully process/prep a new sample, or wants synced beat-cut stems named by BPM and beat count. Takes an input path and an optional output folder.
---

# /process-new-sample

End-to-end: separate → detect BPM on the instrumental → cut BOTH stems to the same
`[first beat, last beat]` window (so they start/end on a beat and stay
sample-aligned) → save both as
`<name>-<bpm>bpm-<beatcount>bars-instrumental.mp3` and
`<name>-<bpm>bpm-<beatcount>bars-vocals.mp3`.

## Arguments
`/process-new-sample {input path} {output folder}`
- **input** (required): the source mp4/mp3/wav/...
- **output folder** (optional): where to save the two stems. If omitted, the
  instrumental goes to `E:\my_files\my audio\Samples\_full_songs` and the vocals
  to `E:\my_files\my audio\Samples\_full_lyrics`. If given, both go there.

## How to run
Run the `process_sample.py` orchestrator with the project's unified venv:

```powershell
& "C:\My_Files\my_programs\intrumental-lyric-separator\.venv\Scripts\python.exe" `
  "C:\My_Files\my_programs\intrumental-lyric-separator\scripts\process_sample.py" `
  "<input>" "<output folder>"
```

Omit the second argument entirely if the user did not give an output folder.
Always double-quote both paths.

## Notes
- BPM/beats are detected on the **instrumental** (cleaner onsets than the full mix),
  and the identical cut window is applied to the vocals so the two stems line up.
- The filename slot is labelled `bars` per the naming spec but holds the **beat
  count** (the number of detected beats inside the cut).

## After running
Report the script's `=== summary ===`: detected BPM, total beats, the cut window,
and both output paths.
