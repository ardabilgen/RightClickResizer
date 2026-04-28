"""Tests for video converter module."""
import os
import pytest
from video_converter import is_video_file, VIDEO_EXTENSIONS


def test_video_extensions_list():
    """Test that video extensions are defined."""
    assert len(VIDEO_EXTENSIONS) > 0
    assert '.mp4' in VIDEO_EXTENSIONS
    assert '.avi' in VIDEO_EXTENSIONS
    assert '.mov' in VIDEO_EXTENSIONS


def test_is_video_file():
    """Test video file detection."""
    assert is_video_file("test.mp4")
    assert is_video_file("test.AVI")
    assert is_video_file("test.MOV")
    assert not is_video_file("test.jpg")
    assert not is_video_file("test.png")
    assert not is_video_file("test.txt")
