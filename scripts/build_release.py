from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST_DIR = ROOT / "dist"
BUILD_DIR = ROOT / "build"
ENTRYPOINT = ROOT / "src" / "lightflipper" / "__main__.py"
OUTPUT_EXE = DIST_DIR / "LightFlipper.exe"
OUTPUT_EXE_TEXT = "dist/LightFlipper.exe"


def run(command: list[str]) -> None:
    print(f"Running: {' '.join(command)}")
    subprocess.run(command, cwd=str(ROOT), check=True)


def ensure_clean_output() -> None:
    for path in (DIST_DIR, BUILD_DIR):
        if path.exists():
            shutil.rmtree(path)


def build_exe() -> Path:
    ensure_clean_output()
    DIST_DIR.mkdir(parents=True, exist_ok=True)

    pyinstaller_command = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--onefile",
        "--windowed",
        "--name",
        "LightFlipper",
        "--distpath",
        str(DIST_DIR),
        "--workpath",
        str(BUILD_DIR),
        "--specpath",
        str(ROOT),
        "--paths",
        str(ROOT / "src"),
        "--hidden-import",
        "PySide6",
        "--hidden-import",
        "bleak",
        "--hidden-import",
        "serial",
        str(ENTRYPOINT),
    ]

    run(pyinstaller_command)

    exe_path = OUTPUT_EXE
    if not exe_path.exists():
        fallback = DIST_DIR / "LightFlipper" / "LightFlipper.exe"
        if fallback.exists():
            exe_path = fallback
        else:
            raise FileNotFoundError(f"Expected built executable at {OUTPUT_EXE} or {fallback}.")

    print(f"Built release executable: {exe_path}")
    if str(exe_path.relative_to(ROOT)) == OUTPUT_EXE_TEXT:
        print(f"Release target: {OUTPUT_EXE_TEXT}")
    return exe_path


def main() -> int:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    build_exe()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
