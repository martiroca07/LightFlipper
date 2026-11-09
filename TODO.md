# LightFlipper TODO

## Phase 1: Application foundation
- [x] Scaffold project structure
- [x] Build main window and navigation shell
- [x] Implement theme engine
- [x] Implement settings persistence
- [x] Add test coverage for settings and themes
- [x] Add persistent color and typography customization
- [x] Add sidebar visibility control
- [x] Add original pixel-art navigation and action icons
- [ ] Expand dashboard widgets
- [ ] Add logging and diagnostics viewer

## Phase 2: Connectivity
- [x] USB detection and diagnostics
- [x] Device info collection
- [x] Serial port management
- [ ] Connection recovery workflows

## Phase 3: Bluetooth
- [x] BLE scanning and pairing foundation
- [x] Bluetooth connection handling and validation
- [x] RPC transport layer abstraction
- [ ] Add BLE discovery and connection controls to the desktop UI
- [ ] Connection handling and retries

## Phase 4: Remote control
- [x] Screen synchronization UI scaffold
- [x] Controller buttons and events
- [ ] Send remote button press/release over the active USB/BLE device transport
- [ ] Verify remote button events and live screen updates over BLE on hardware
- [ ] Refresh optimization and live device frame updates

## Phase 5: File management
- [x] File Manager page gated on device connection
- [ ] Implement live device filesystem transport before enabling file actions
- [ ] Real hardware-backed file transfer synchronization

## Phase 6+: Firmware and applications
- [x] Local `.dfu` selection and validation via qFlipper CLI
- [ ] Validate firmware installation on physical hardware
- [ ] App management
- [ ] Wi-Fi Devboard workflows
