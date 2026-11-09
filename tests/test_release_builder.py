from pathlib import Path


def test_release_builder_exists_and_has_windows_output_target():
    script = Path(__file__).resolve().parents[1] / "scripts" / "build_release.py"
    assert script.exists(), "Release build script must exist."

    content = script.read_text(encoding="utf-8")
    assert "dist/LightFlipper.exe" in content, "Windows EXE output path is missing."
