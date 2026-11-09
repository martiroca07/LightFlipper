# Changelog

## [0.1.2] - 2026-11-09
- Added exclusive sidebar selection and disabled device-dependent pages while disconnected.
- Added persistent color and typography customization, sidebar visibility, and original pixel-art icons.
- Replaced mock file listings with an explicit unavailable state until live filesystem transport exists.
- Added USB-only local `.dfu` installation through the official qFlipper CLI, with validation and confirmation.
- Fixed Windows font loading for readable packaged UI text.
- Configured GitHub Releases to generate notes comparing each tag with its previous release.

## [0.1.1] - 2026-11-09
- Clarified offline remote-control and sample-filesystem preview states.
- Disabled navigation entries for pages that are not implemented yet.
- Added Qt interaction tests for remote button press and release behavior.

## [0.1.0] - 2026-11-09
- Established the LightFlipper project skeleton.
- Added settings persistence with SQLite.
- Added theme engine and default palette.
- Created the main app shell and navigation layout.
- Added automated tests for theme and settings behavior.
- Added Windows EXE build script and GitHub release workflow.
