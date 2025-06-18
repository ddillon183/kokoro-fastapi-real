import os
import pytest
import asyncio
from pathlib import Path
from unittest.mock import patch

from api.src.core.paths import (
    _find_file,
    _scan_directories,
    get_content_type,
    get_temp_dir_size,
    get_temp_file_path,
    list_temp_files,
)

@pytest.mark.asyncio
async def test_find_file_exists(tmp_path):
    """Test finding an existing file."""
    test_file = tmp_path / "test.txt"
    test_file.write_text("hello")

    found_path = await _find_file("test.txt", [str(tmp_path)])
    assert found_path == str(test_file)

@pytest.mark.asyncio
async def test_find_file_not_exists(tmp_path):
    """Test missing file raises error."""
    with pytest.raises(FileNotFoundError, match="File not found"):
        await _find_file("not_here.txt", [str(tmp_path)])

@pytest.mark.asyncio
async def test_find_file_with_filter(tmp_path):
    """Test finding file with filter."""
    test_file = tmp_path / "test.txt"
    test_file.write_text("data")

    filter_fn = lambda p: p.endswith(".txt")
    found_path = await _find_file("test.txt", [str(tmp_path)], filter_fn)
    assert found_path == str(test_file)

@pytest.mark.asyncio
async def test_scan_directories():
    """Test scanning directories."""
    mock_entry = type("MockEntry", (), {"name": "test.txt"})()

    with (
        patch("aiofiles.os.path.exists") as mock_exists,
        patch("aiofiles.os.scandir") as mock_scandir,
    ):
        mock_exists.return_value = True
        mock_scandir.return_value = [mock_entry]

        files = await _scan_directories(["/test/path"])
        assert "test.txt" in files

@pytest.mark.asyncio
async def test_get_content_type():
    """Test content type detection."""
    test_cases = [
        ("test.html", "text/html"),
        ("test.js", "application/javascript"),
        ("test.css", "text/css"),
        ("test.png", "image/png"),
        ("test.unknown", "application/octet-stream"),
    ]

    for filename, expected in test_cases:
        content_type = await get_content_type(filename)
        assert content_type == expected

@pytest.mark.asyncio
async def test_get_temp_file_path():
    """Test temp file path generation."""
    with (
        patch("aiofiles.os.path.exists") as mock_exists,
        patch("aiofiles.os.makedirs") as mock_makedirs,
    ):
        mock_exists.return_value = False

        path = await get_temp_file_path("test.wav")
        assert "test.wav" in path
        mock_makedirs.assert_called_once()

@pytest.mark.asyncio
async def test_list_temp_files():
    """Test listing temp files."""

    class MockEntry:
        def __init__(self, name):
            self.name = name

        def is_file(self):
            return True

    mock_entry = MockEntry("test.wav")

    with (
        patch("aiofiles.os.path.exists") as mock_exists,
        patch("aiofiles.os.scandir") as mock_scandir,
    ):
        mock_exists.return_value = True
        mock_scandir.return_value = [mock_entry]

        files = await list_temp_files()
        assert "test.wav" in files

@pytest.mark.asyncio
async def test_get_temp_dir_size():
    """Test getting temp directory size."""

    class MockEntry:
        def __init__(self, path):
            self.path = path

        def is_file(self):
            return True

    mock_entry = MockEntry("/tmp/test.wav")
    mock_stat = type("MockStat", (), {"st_size": 1024})()

    with (
        patch("aiofiles.os.path.exists") as mock_exists,
        patch("aiofiles.os.scandir") as mock_scandir,
        patch("aiofiles.os.stat") as mock_stat_fn,
    ):
        mock_exists.return_value = True
        mock_scandir.return_value = [mock_entry]
        mock_stat_fn.return_value = mock_stat

        size = await get_temp_dir_size()
        assert size == 1024
