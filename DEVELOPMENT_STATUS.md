# LightFlipper Development Status

## Completed features
- Project structure created and package discovery configured for editable installs.
- Application shell scaffold implemented with a dark orange UI and navigation panel.
- Dashboard starter layout added for the main desktop window.
- Theme engine implemented with default palette and custom theme creation support.
- SQLite-backed settings persistence added for application configuration.
- Automated test coverage created for theme, settings, USB, Bluetooth, and remote-control behavior.
- USB port detection implemented for Flipper-like serial devices.
- USB connection manager implemented with explicit mock-mode support for tests and hardware-safe validation.
- Bluetooth discovery and connection manager implemented with Flipper-device filtering and mock-safe connection validation.
- Remote-control controller model implemented, with screen buffer tracking and button state handling.
- Remote-control page added to the desktop shell with directional, OK, and Back controls.
- App startup and UI smoke tests validated in an offscreen Qt environment.
- Remote controls now clearly show offline preview state; held buttons return to idle state after release.
- Sidebar selection is exclusive; Remote Control and File Manager are gated behind a device connection.
- File Manager no longer presents mock entries as device files; live filesystem transport remains unavailable.
- Settings persist palette colors, font family, font size, and sidebar visibility.
- Original pixel-art icons are generated in-app and recolor with the selected accent.
- Local `.dfu` firmware installation uses the official qFlipper CLI, USB-only gating, format checks, and explicit confirmation.
- Qt integration tests cover connection gates, button press/release, theme persistence, icons, and firmware format checks.
- Windows system font fallback is registered without bundling system fonts.
- Windows EXE startup verified in offscreen mode without a connected Flipper device.
- GitHub release workflow publishes the matching `CHANGELOG.md` bullets plus a compare link to the previous tag; the generator has regression tests.
- This public status document is the portable project checkpoint for continuing work from another computer; it must stay free of prompts and secrets.

## Continuity notes
- Before tagging a release, add a dated version section with user-facing bullets to `CHANGELOG.md` and bump `pyproject.toml`.
- Run `python scripts/generate_release_notes.py <current-tag> <previous-tag>` to preview the exact GitHub release body.
- Keep `.ai/` and `dist/` ignored; do not commit private handoff notes or generated executables.
- Do not describe File Manager, remote transport, or firmware installation as hardware-verified until tested on a physical Flipper.

## In-progress features
- Application management workflows and physical validation of firmware installation.
- Remote-control transport over the active USB/BLE session, including press/release events and live screen synchronization.
- Live transport protocols for production hardware sessions.
- Real device-backed file transfer and desktop synchronization.

## Known limitations
- Real hardware validation for USB, Bluetooth, and remote-control features remains pending on actual Flipper hardware.
- Firmware installation delegates to qFlipper CLI and has not been run against physical hardware in this environment.
- BLE discovery is implemented at the library layer, but the desktop Settings page currently exposes USB connection only.
- Remote-control buttons currently update only local UI state; no live RPC commands are sent over BLE or USB yet.
- True live screen synchronization and RPC payload handling still need a hardware-validated transport layer.

## Outstanding bugs
- Live file operations, remote-control transport, and firmware update outcomes need physical-device verification.

## Hardware tests required
- USB serial device detection on Windows with a real Flipper Zero.
- Bluetooth device discovery and pairing validation.
- Remote-control button and screen synchronization against real hardware.
- Remote-control button press/release delivery over BLE and screen updates from the device.
- Flipper RPC communication through real hardware.
- qFlipper CLI firmware installation with a known-good `.dfu` and inserted microSD card.

## Next development tasks
1. Implement BLE discovery and connection controls in the desktop UI.
2. Implement a hardware-backed RPC transport and route remote button press/release over active USB/BLE.
3. Validate remote screen synchronization and controls over BLE on a physical Flipper.
4. Implement live Flipper filesystem browsing and transfers.
5. Validate qFlipper `.dfu` installation on a physical Flipper with microSD.
6. Continue app catalog, firmware metadata, and changelog workflows.
