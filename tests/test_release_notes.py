from lightflipper.release_notes import build_release_notes


def test_release_notes_include_current_changes_and_previous_tag_comparison():
    changelog = """# Changelog

## [0.1.2] - 2026-11-09
- Added pixel-art icons.
- Added safe DFU updates.

## [0.1.1] - 2026-11-09
- Clarified offline preview.
"""

    notes = build_release_notes(changelog, "v0.1.2", "v0.1.1")

    assert "Changes since v0.1.1" in notes
    assert "Added pixel-art icons." in notes
    assert "Added safe DFU updates." in notes
    assert "compare/v0.1.1...v0.1.2" in notes
    assert "Clarified offline preview." not in notes


def test_release_notes_fail_if_version_has_no_changelog_section():
    try:
        build_release_notes("# Changelog\n", "v0.1.2", "v0.1.1")
    except ValueError as error:
        assert "0.1.2" in str(error)
    else:
        raise AssertionError("Missing release changelog section should be rejected.")