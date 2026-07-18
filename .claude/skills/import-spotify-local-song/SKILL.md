---
name: import-spotify-local-song
description: Download a YouTube URL as an mp3 into the Spotify local-files folder (E:\my_files\my audio\spotify local songs). No separation, no BPM — just the mp3. Use when the user runs /import-spotify-local-song, or asks to add/import a song as a Spotify local file from a YouTube link.
---

# /import-spotify-local-song

Download a single YouTube URL as a 320 kbps mp3 (named by slugified video title)
straight into the Spotify "local files" folder so Spotify can pick it up. No
separation, no BPM — just the mp3.

## Arguments
`/import-spotify-local-song {youtube url}`
- **url** (required): the YouTube link.

## Destination (fixed)
`E:\my_files\my audio\spotify local songs`

## How to run
Run the `youtube_download` module with the project's unified venv, pointing `-o`
at the fixed Spotify local-files folder:

```powershell
& "C:\My_Files\my_programs\intrumental-lyric-separator\.venv\Scripts\python.exe" `
  "C:\My_Files\my_programs\intrumental-lyric-separator\youtube_download\cli.py" `
  -o "E:\my_files\my audio\spotify local songs" "<youtube url>"
```

The folder is created automatically if it doesn't exist.

## After running
Report the downloaded mp3 filename and confirm it landed in the Spotify local-files
folder. Remind the user that Spotify must have that folder added under
Settings → Local Files for it to appear.
