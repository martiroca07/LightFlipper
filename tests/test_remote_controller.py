from lightflipper.remote import RemoteController, RemoteButton


def test_remote_controller_tracks_button_state():
    controller = RemoteController()

    assert controller.press_button(RemoteButton.UP) is True
    assert controller.is_pressed(RemoteButton.UP) is True
    assert controller.press_button(RemoteButton.OK) is True
    assert controller.get_pressed_buttons() == [RemoteButton.UP, RemoteButton.OK]

    controller.release_button(RemoteButton.UP)
    assert controller.is_pressed(RemoteButton.UP) is False


def test_remote_controller_rejects_unknown_button_name():
    controller = RemoteController()

    assert controller.press_button("invalid") is False
    assert controller.last_error is not None


def test_remote_controller_updates_screen_buffer():
    controller = RemoteController()
    controller.set_screen_buffer("frame-01")

    assert controller.screen_buffer == "frame-01"
    assert controller.screen_sync_enabled is True
