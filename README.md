<p align="center">
  <img src="DistantViewerIcon.png" width="96" alt="Distant Viewer icon">
</p>

<h1 align="center">Distant Viewer</h1>

<p align="center">
A fast Windows desktop app for browsing, sorting and searching a large local
image &amp; video library, and for finding and saving new media from
booru-style imageboards.
</p>

> **18+ notice:** the imageboards this app can search host adult content.
> You are responsible for following each site's terms of service and your local
> laws.

## Features

**Saved library**
- Two buckets, *Unfiltered* and *Filtered*, for sorting what you keep. A pop-out
  viewer keeps a running "deleted + moved on" count while you sort.
- Instant tag search with tabs, `a|b` any-of terms, and colour-coded tags.
- Sort by download date, upload date, move date, name, size or random.
- Smooth with 100,000+ files: thumbnails load only near what's on screen, and
  moves and deletes run in the background.
- Copy any image straight to the clipboard, or show it in Explorer.

**Explore**
- Search Gelbooru, e621, Realbooru and Rule34.xxx, one site or all at once.
- Middle-click to save, or "Save All From Search" for a whole result set.
- Hidden tags (results carrying them are skipped) and a blacklist for posts you
  never want to download again.

**More**
- **Duplicates** - perceptual matching of images, GIFs and videos across
  resolutions and formats.
- **Waifu page** - every character, VTuber, artist and series in your library,
  with portraits you can crop and profiles pulled from the web.
- **Repair tools** - fill in missing tags and upload dates, rebuild video
  thumbnails.
- Themes (classic or frosted, your own colours) and a top or left toolbar.

## Requirements

- Windows 10 or 11 (it uses the Windows Shell for thumbnails and Explorer).
- Python 3.12 or newer.

## Run from source

```bash
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\python DistantViewer.py
```

`opencv-python-headless` and `numpy` are optional. Without them, video
thumbnails fall back to Windows' own and duplicate matching skips video frames.

## Site accounts

Searching works without an account, but Gelbooru and Rule34.xxx limit what
their API returns without one. To add yours:

1. Log in on the site and open **My Account > Options**. Copy your **user ID**
   and **API key** from **API Access Credentials**.
2. In the app, paste them into **Settings > Explore > Site accounts**.

They are saved only on your PC, in `site_accounts.json` in the app's data
folder. They are never part of the code.

## Where your data lives

| What | Where |
| --- | --- |
| Settings, caches, logs, site accounts | `%APPDATA%\Distant Viewer` (movable in **Settings > Saved Library**) |
| Saved images and videos | The folder chosen in **Settings > Saved Library** (with `unfiltered` and `filtered` inside) |

## Build a standalone exe

```bash
.venv\Scripts\pip install -r requirements-build.txt
.venv\Scripts\python tools\publish.py
```

This builds `release\builds\<version>\Distant Viewer.exe` in a `release` folder
next to this repository, plus a small `release\Distant Viewer.exe` launcher that
always opens the newest build. A running copy notices newly published builds
and offers to restart into them, showing the release notes from
`APP_UPDATE_NOTES` in `DistantViewer.py`.

note 
One scanner on VirusTotal (1/71) flags Pillow’s standard image modules - a known false positive for Python apps. Windows Defender and the other 70 engines report it clean.
