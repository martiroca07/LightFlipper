from lightflipper.file_manager import FlipperFileManager


def test_file_manager_lists_and_creates_directories():
    manager = FlipperFileManager()

    listing = manager.list_directory("/")
    assert any(item.name == "nfc" for item in listing)

    created = manager.create_directory("custom", "/")
    assert created is True
    assert any(item.name == "custom" for item in manager.list_directory("/"))


def test_file_manager_uploads_renames_and_deletes_files():
    manager = FlipperFileManager()
    upload = manager.upload_file("/nfc/hello.txt", b"hello world")
    assert upload is True

    renamed = manager.rename_file("/nfc/hello.txt", "hello-renamed.txt")
    assert renamed is True
    assert manager.get_file("/nfc/hello-renamed.txt") is not None

    deleted = manager.delete_file("/nfc/hello-renamed.txt")
    assert deleted is True
    assert manager.get_file("/nfc/hello-renamed.txt") is None


def test_file_manager_rejects_invalid_paths():
    manager = FlipperFileManager()

    assert manager.create_directory("", "/") is False
    assert manager.upload_file("", b"no") is False
    assert manager.get_file("/missing/file.txt") is None
