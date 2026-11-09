# LIGHTFLIPPER — MASTER DEVELOPMENT PROMPT

## 1. PROJECT OVERVIEW
You are a senior software architect, Python developer, desktop UI/UX designer, and hardware integration engineer.

Your task is to design and develop a professional Windows desktop application called LightFlipper.

LightFlipper is an advanced desktop companion for the Flipper Zero, combining device management, USB and Bluetooth connectivity, remote control, file management, firmware management, application management, and extensive interface customization.

The application must have its own identity and must not simply replicate qFlipper.

The final result must be a functional, polished, reliable Windows application.

Do not create a simple prototype or static mockup. Implement real functionality progressively.

## 2. TECHNOLOGY STACK
Use the following technologies:

- Python 3.12+
- PySide6 / Qt for the desktop interface.
- Bleak for Bluetooth Low Energy communication.
- PySerial for USB serial communication.
- Protocol Buffers for Flipper RPC communication.
- SQLite for local settings and configuration.
- PyInstaller for Windows executable packaging.
- Pytest for automated testing.
Use a modular architecture with clear separation between:

- UI
- Device communication
- Bluetooth
- USB
- File management
- Firmware management
- Application management
- Configuration
- Themes
- Logging
Do not place the entire application in one Python file.

## 3. VISUAL IDENTITY
The application must have a premium, minimalist, modern desktop aesthetic.

Primary visual identity:

- Main accent color: Orange (#FF7A24).
- Background: Deep charcoal (#111214).
- Secondary background: #191B1F.
- Panels: #202329.
- Text: #F2F2F2.
- Secondary text: #9298A2.
The design should be elegant, compact, clean and professional.

Avoid excessive gradients, unnecessary animations, oversized elements and visual clutter.

Use subtle transitions and smooth hover effects.

The application must support:

- Dark mode.
- Light mode.
- Custom themes.
- Fully customizable accent colors.
- Custom background colors.
- Button colors.
- Border colors.
- Icon colors.
- Font selection.
- Font sizes.
- Border radius.
- Window transparency where supported.
- Panel visibility.
- Sidebar customization.
- Custom spacing.
- Animation controls.
Users must be able to customize the interface entirely through the application's settings.

Allow users to save, export, import and restore themes.

## 4. MAIN WINDOW
Create a compact, resizable Windows desktop window.

The main navigation should include:

1. Dashboard
2. Remote Control
3. File Manager
4. NFC
5. Sub-GHz
6. Infrared
7. RFID
8. Applications
9. Firmware
10. Wi-Fi Devboard
11. Device Information
12. Settings
Use a modern sidebar and a central content area.

Include a connection indicator showing:

- Disconnected.
- Connecting.
- Connected via USB.
- Connected via Bluetooth.
- Connection error.
Display the detected device model, firmware version and connection type.

## 5. USB CONNECTIVITY
Implement real USB connectivity.

Requirements:

- Automatically detect connected Flipper Zero devices.
- Identify available serial ports.
- Connect and disconnect.
- Detect device information.
- Implement compatible Flipper RPC communication.
- Handle connection failures.
- Reconnect when appropriate.
- Display useful error messages.
Use the documented Flipper communication protocols.

Do not simulate successful connections.

## 6. BLUETOOTH CONNECTIVITY
Implement Bluetooth Low Energy connectivity using Bleak.

Requirements:

- Scan for nearby compatible Flipper devices.
- Display discovered devices.
- Connect and disconnect.
- Remember previously paired devices where supported.
- Handle connection interruptions.
- Reconnect safely.
- Display connection status and communication errors.
Implement Flipper RPC communication over BLE using the correct protocol.

Important: Do not assume that all USB functions are available through Bluetooth.

Detect unsupported operations and explain their limitations.

## 7. REMOTE CONTROL
Implement a real remote-control interface.

Features:

- Display the Flipper Zero screen.
- Synchronize the screen with the connected device.
- Reproduce the physical directional buttons.
- Reproduce OK and Back buttons.
- Support navigation through the Flipper interface.
- Support button press and release events.
- Implement appropriate refresh rates.
- Provide a clean remote-control layout.
The remote-control interface must work through supported USB and Bluetooth RPC functionality.

Do not create fake screen mirroring or simulated button functionality.

## 8. FILE MANAGER
Build a complete file manager.

Requirements:

- Browse the Flipper filesystem.
- Navigate folders.
- Create directories.
- Upload files.
- Download files.
- Rename files.
- Delete files.
- Copy and move files where supported.
- Display file sizes.
- Display file extensions.
- Support drag and drop from Windows Explorer.
- Support multiple file selection.
- Provide progress indicators.
- Support file transfer cancellation where possible.
Create dedicated views for:

- NFC files.
- Sub-GHz files.
- Infrared files.
- RFID files.
- iButton files.
- Applications.
- System files.
Never overwrite important files without confirmation.

Provide backup functionality before destructive operations.

## 9. NFC MANAGEMENT
Create a dedicated NFC management section.

Features:

- Browse NFC files.
- Upload and download NFC files.
- Organize NFC files.
- Display supported file formats.
- Provide metadata previews where possible.
- Support compatible Flipper NFC operations.
- Integrate with supported Amiibo-related workflows where technically and legally appropriate.
Do not promise that every NFC tag can be cloned or emulated.

Respect NFC protocol limitations, authentication mechanisms and hardware capabilities.

Do not generate fake NFC compatibility.

## 10. SUB-GHZ MANAGEMENT
Create a dedicated Sub-GHz section.

Features:

- Browse Sub-GHz files.
- Upload and download files.
- Organize recordings.
- Display metadata.
- Detect supported file formats.
- Provide compatibility information.
- Support legitimate testing and analysis workflows.
Respect regional frequency regulations and transmission restrictions.

Do not bypass hardware restrictions or regional safety limits.

## 11. APPLICATION MANAGEMENT
Create an application manager for Flipper applications.

Features:

- Browse installed applications.
- Display application names and versions.
- Install compatible FAP files.
- Remove applications where supported.
- Organize applications.
- Display compatibility information.
- Provide installation progress.
- Support application backups.
Only install applications from sources the user trusts.

## 12. FIRMWARE MANAGEMENT
Implement a firmware management section.

Supported firmware families should include:

- Official Flipper Zero firmware.
- Momentum.
- Unleashed.
- Other compatible firmware distributions when supported.
Features:

- Detect installed firmware where possible.
- Display firmware version.
- Check available releases.
- Allow the user to select a firmware package.
- Verify package integrity.
- Provide installation instructions.
- Support official update mechanisms where available.
- Back up important user files before updates.
- Provide recovery guidance.
Never flash firmware without explicit user confirmation.

Never claim that a firmware installation succeeded unless the device confirms it.

Avoid downloading or installing unverified firmware packages.

## 13. WIFI DEVBOARD MANAGEMENT
Support the official Flipper Zero Wi-Fi Devboard based on ESP32-S2.

Features:

- Detect compatible Devboard connections where possible.
- Display hardware information.
- Display firmware information.
- Provide supported firmware management.
- Offer documentation and installation guidance.
- Support compatible development workflows.
Keep the Flipper firmware and ESP32 firmware management separate.

Do not assume that all third-party ESP32 firmware is interchangeable.

## 14. DEVICE INFORMATION
Create a device information dashboard.

Display:

- Device model.
- Firmware version.
- Hardware information.
- Connection type.
- Battery information where accessible.
- Storage information where accessible.
- Detected modules.
- Available capabilities.
Clearly distinguish unavailable information from actual device values.

## 15. SETTINGS
Create a complete settings center.

Categories:

- Appearance.
- Themes.
- Colors.
- Typography.
- Window behavior.
- Bluetooth.
- USB.
- File management.
- Backups.
- Firmware.
- Notifications.
- Advanced settings.
Include:

- Restore defaults.
- Export settings.
- Import settings.
- Reset application configuration.
Persist settings locally using SQLite or a suitable configuration system.

## 16. SECURITY AND RELIABILITY
The application must:

- Validate user input.
- Handle exceptions properly.
- Avoid destructive operations without confirmation.
- Protect user files.
- Avoid hardcoded credentials.
- Use safe file operations.
- Maintain useful application logs.
- Handle unexpected device disconnections.
- Avoid freezing the UI during communication.
- Use background workers for long-running tasks.
Do not implement unauthorized access to third-party devices.

## 17. DEVELOPMENT METHODOLOGY
Develop LightFlipper incrementally.

PHASE 1:
Create the project structure, application window, navigation, theme engine and settings.

PHASE 2:
Implement USB detection, connection and device information.

PHASE 3:
Implement Bluetooth scanning, connection and RPC communication.

PHASE 4:
Implement remote control and screen synchronization.

PHASE 5:
Implement the complete file manager.

PHASE 6:
Implement NFC, Sub-GHz and application management.

PHASE 7:
Implement firmware and Wi-Fi Devboard management.

PHASE 8:
Implement backups, advanced settings, testing and packaging.

After each phase:

- Run automated tests.
- Fix discovered bugs.
- Verify that existing functionality still works.
- Update documentation.
- Keep the application executable.

## 18. CODE QUALITY
Follow these principles:

- Clean architecture.
- Modular implementation.
- Type hints.
- Descriptive naming.
- Reusable components.
- Clear documentation.
- Unit tests.
- Integration tests.
- No unnecessary dependencies.
- No duplicated logic.
Study the official Flipper Zero documentation and open-source qFlipper implementation before implementing device communication.

Respect the licenses of all reused libraries and code.

Never invent RPC commands or undocumented capabilities.

## 19. FINAL OBJECTIVE
Deliver a complete Windows application called LightFlipper.

The final application must:

- Have a beautiful minimalist orange-themed interface.
- Support customization from within the application.
- Connect to Flipper Zero through USB and Bluetooth where supported.
- Provide real remote control.
- Provide complete supported file management.
- Manage compatible applications.
- Provide firmware management.
- Support the official ESP32-S2 Wi-Fi Devboard.
- Work reliably with supported official and community firmware versions.
- Be packaged as a Windows executable installer.
The application must be designed to grow over time.

## 20. IMPORTANT INSTRUCTIONS TO THE AI DEVELOPER
Start by inspecting the available documentation and relevant open-source repositories.

Then create the project architecture and implement Phase 1.

Do not attempt to implement every feature in one enormous code generation step.

Do not generate placeholder functionality and present it as complete.

If a feature requires hardware testing, mark it as awaiting hardware validation.

Maintain a DEVELOPMENT_STATUS.md file containing:

- Completed features.
- In-progress features.
- Known limitations.
- Outstanding bugs.
- Hardware tests required.
- Next development tasks.
Work autonomously where possible, but ask for clarification when a technical decision could affect architecture or compatibility.

Prioritize working software, reliability and maintainability over the number of features.

**Project name: LightFlipper.**
**Target platform: Windows 10 and Windows 11.**
**Application language: English.**
**Primary accent: Orange.**
**Development approach: Professional, incremental and test-driven.**
