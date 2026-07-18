---
name: download-songs
description: Download one or more YouTube URLs as highest-quality mp3s, named by slugified video title. Use when the user runs /download-songs, or gives YouTube links and asks to download them as mp3 / grab the audio / pull songs into a folder. Takes one or more URLs and an output folder.
---

# /download-songs

Download YouTube URLs as 320 kbps mp3s, each named `<slug-of-video-title>.mp3`.

## Arguments
`/download-songs {output folder} {url1} {url2} ...`
- **output folder** (required): where to save the mp3s.
- **urls** (one or more): YouTube links.

(If the user only gives URLs and no folder, ask where to save them, or default to
a `samples/` folder under the repo and tell them.)

## How to run
Run the `youtube_download` module with the project's unified venv. The `-o` flag
takes the output folder; URLs are positional:

```powershell
& "C:\My_Files\my_programs\intrumental-lyric-separator\.venv\Scripts\python.exe" `
  "C:\My_Files\my_programs\intrumental-lyric-separator\youtube_download\cli.py" `
  -o "<output folder>" "<url1>" "<url2>"
```

For a long list, write the URLs to a text file (one per line) and use
`--from-file urls.txt` instead of positional URLs.

## After running
Report the script's `=== summary ===`: which slugified mp3s were downloaded (and
any failures), and the destination folder.
