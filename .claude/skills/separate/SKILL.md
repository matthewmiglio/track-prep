---
name: separate
description: Split an audio/video file into vocals + instrumental mp3s using BS-RoFormer. Use when the user runs /separate, or asks to separate/split a track into stems, isolate vocals, or extract an instrumental. Takes an input path and an optional output folder.
---

# /separate

Convert an input (mp4/mp3/wav/...) to mp3, run BS-RoFormer separation, and export
`<name>-instrumental.mp3` and `<name>-vocals.mp3`.

## Arguments
`/separate {input path} {output folder}`
- **input** (required): the source audio/video file.
- **output folder** (optional): where to save the stems. If omitted, the stems
  are written next to the input file (sister files).

## How to run
Run the `separate_song` module with the project's unified venv:

```powershell
& "C:\My_Files\my_programs\intrumental-lyric-separator\.venv\Scripts\python.exe" `
  "C:\My_Files\my_programs\intrumental-lyric-separator\separate_song\cli.py" `
  "<input>" "<output folder>"
```

Omit the second argument entirely if the user did not give an output folder.
Always double-quote both paths (filenames often contain spaces and brackets).

## After running
Report the two output paths from the script's `=== done ===` summary. The first
run downloads the ~639 MB separator model to `D:\ai-models\audio-models\separator`;
later runs reuse it.
