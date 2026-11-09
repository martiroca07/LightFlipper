from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from lightflipper.release_notes import build_release_notes


def main() -> int:
    if len(sys.argv) not in (2, 3):
        raise SystemExit("Usage: generate_release_notes.py <current-tag> [previous-tag]")

    current_tag = sys.argv[1]
    previous_tag = sys.argv[2] if len(sys.argv) == 3 and sys.argv[2] else None
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    notes = build_release_notes(changelog, current_tag, previous_tag)
    (ROOT / "release-notes.md").write_text(notes, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())