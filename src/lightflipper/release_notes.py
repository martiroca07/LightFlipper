from __future__ import annotations

import re


_SECTION_PATTERN = re.compile(r"^##\s+\[([^]]+)\][^\n]*\n", re.MULTILINE)


def _normalize_version(version: str) -> str:
    return version.strip().removeprefix("v")


def build_release_notes(
    changelog: str,
    current_tag: str,
    previous_tag: str | None = None,
) -> str:
    current_version = _normalize_version(current_tag)
    sections = list(_SECTION_PATTERN.finditer(changelog))
    current_index = next(
        (
            index
            for index, match in enumerate(sections)
            if _normalize_version(match.group(1)) == current_version
        ),
        None,
    )
    if current_index is None:
        raise ValueError(f"CHANGELOG.md has no section for version {current_version}.")

    section = sections[current_index]
    end = sections[current_index + 1].start() if current_index + 1 < len(sections) else len(changelog)
    changes = [
        line.strip()
        for line in changelog[section.end():end].splitlines()
        if line.strip().startswith(("- ", "* "))
    ]

    heading = (
        f"## Changes since {previous_tag} ({current_tag})"
        if previous_tag
        else f"## Changes in {current_tag}"
    )
    notes = [heading, ""]
    notes.extend(changes or ["- See the full comparison for details."])
    if previous_tag:
        compare_url = (
            "https://github.com/martiroca07/LightFlipper/compare/"
            f"{previous_tag}...{current_tag}"
        )
        notes.extend(("", f"[Full comparison: {previous_tag}...{current_tag}]({compare_url})"))
    return "\n".join(notes) + "\n"