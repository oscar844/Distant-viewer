"""Build DistantViewer.py into a standalone Windows exe and publish it.

    python tools/publish.py [DistantViewer.py] [--root <release folder>] [--no-publish]

Run it with the Python environment that has the app's requirements plus
PyInstaller installed (see requirements-build.txt).

1. PyInstaller (onedir) builds the app into build/<version>/ next to this repo.
2. The build is copied to <root>/builds/<version>/.
3. The launcher (<root>/Distant Viewer.exe) is built if it isn't there yet. It
   always starts the newest build, so shortcuts never need changing.
4. <root>/latest.json is written last, atomically - a running copy only ever
   sees a manifest that names a complete build. Its notes are the source's
   APP_UPDATE_NOTES, shown in the app's "Update ready" pop-up.

The default <root> is a "release" folder beside this repository's folder.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
REPO = TOOLS.parent
PYTHON = Path(sys.executable)
ICON = REPO / "DistantViewerIcon.ico"
STAGE_ROOT = REPO / "build"
DEFAULT_ROOT = REPO.parent / "release"


def run(command, **kwargs):
    print(">", " ".join(str(part) for part in command), flush=True)
    subprocess.run([str(part) for part in command], check=True, **kwargs)


def source_info(source: Path) -> tuple[str, str]:
    text = source.read_text(encoding="utf-8")
    version = re.search(r'^APP_VERSION\s*=\s*"([^"]+)"', text, re.M).group(1)
    notes = re.search(r'^APP_UPDATE_NOTES\s*=\s*"""\\?\n?(.*?)"""', text, re.M | re.S)
    return version, notes.group(1).strip() if notes else ""


def build_app(source: Path, version: str) -> Path:
    stage = STAGE_ROOT / version
    if stage.exists():
        shutil.rmtree(stage)
    (stage / "src").mkdir(parents=True)
    entry = stage / "src" / "DistantViewer.py"
    shutil.copy2(source, entry)
    run([
        PYTHON, "-m", "PyInstaller", "--noconfirm", "--clean", "--onedir", "--windowed",
        "--name", "Distant Viewer",
        "--icon", ICON,
        "--add-data", f"{ICON}{os.pathsep}.",
        # Loaded by name at runtime (optional_module), so PyInstaller can't see them.
        "--hidden-import", "cv2", "--hidden-import", "numpy",
        "--distpath", stage / "dist", "--workpath", stage / "build", "--specpath", stage,
        entry,
    ])
    built = stage / "dist" / "Distant Viewer"
    assert (built / "Distant Viewer.exe").exists(), "build produced no exe"
    return built


def build_launcher(root: Path):
    stage = STAGE_ROOT / "launcher"
    if stage.exists():
        shutil.rmtree(stage)
    stage.mkdir(parents=True)
    run([
        PYTHON, "-m", "PyInstaller", "--noconfirm", "--clean", "--onefile", "--windowed",
        "--name", "Distant Viewer", "--icon", ICON,
        "--distpath", stage / "dist", "--workpath", stage / "build", "--specpath", stage,
        TOOLS / "launcher.py",
    ])
    shutil.copy2(stage / "dist" / "Distant Viewer.exe", root / "Distant Viewer.exe")


def main():
    args = sys.argv[1:]
    positional = [arg for index, arg in enumerate(args) if not arg.startswith("--") and (index == 0 or args[index - 1] != "--root")]
    source = Path(positional[0]).resolve() if positional else REPO / "DistantViewer.py"
    root = Path(args[args.index("--root") + 1]).resolve() if "--root" in args else DEFAULT_ROOT
    publish = "--no-publish" not in args
    version, notes = source_info(source)
    print(f"building {version} from {source}", flush=True)
    started = time.time()
    built = build_app(source, version)
    target = root / "builds" / version
    (root / "builds").mkdir(parents=True, exist_ok=True)
    if target.exists():
        raise SystemExit(f"{target} already exists - bump APP_VERSION before publishing again")
    shutil.copytree(built, target)
    if not (root / "Distant Viewer.exe").exists():
        build_launcher(root)
    if publish:
        manifest = {
            "version": version,
            "build": f"builds/{version}",
            "notes": notes,
            "published": time.strftime("%Y-%m-%d %H:%M"),
        }
        temp = root / "latest.json.tmp"
        temp.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        os.replace(temp, root / "latest.json")
    size = sum(f.stat().st_size for f in target.rglob("*") if f.is_file()) / 2**20
    print(f"done: {target} ({size:.0f} MB) in {time.time() - started:.0f}s; published={publish}", flush=True)


if __name__ == "__main__":
    main()
