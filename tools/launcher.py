"""Distant Viewer launcher: starts the newest published build.

Lives at <release>/Distant Viewer.exe next to latest.json. The builds live in
<release>/builds/<version>/, so the launcher - and any shortcut pointing at it -
never changes when a new version is published."""
import ctypes
import json
import subprocess
import sys
from pathlib import Path

APP_EXE = "Distant Viewer.exe"


def fail(message: str):
    ctypes.windll.user32.MessageBoxW(None, message, "Distant Viewer", 0x10)
    sys.exit(1)


def newest_build(root: Path) -> Path | None:
    try:
        manifest = json.loads((root / "latest.json").read_text(encoding="utf-8"))
        exe = root / str(manifest["build"]) / APP_EXE
        if exe.exists():
            return exe
    except (OSError, ValueError, KeyError, TypeError):
        pass
    # latest.json missing or naming a build that isn't there: newest build folder.
    candidates = [path for path in (root / "builds").glob(f"*/{APP_EXE}") if path.is_file()]
    return max(candidates, key=lambda path: path.stat().st_mtime) if candidates else None


def main():
    root = Path(sys.executable if getattr(sys, "frozen", False) else __file__).resolve().parent
    exe = newest_build(root)
    if exe is None:
        fail(f"No Distant Viewer build was found in\n{root / 'builds'}")
    try:
        subprocess.Popen([str(exe), *sys.argv[1:]], cwd=str(exe.parent), close_fds=True)
    except OSError as exc:
        fail(f"Could not start Distant Viewer.\n\n{exc}")


if __name__ == "__main__":
    main()
