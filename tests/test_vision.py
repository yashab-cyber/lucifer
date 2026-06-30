"""Unit tests for vision/screenshot functionality."""

import pytest
from PIL import Image
from lucifer.core.vision import ScreenCapture


def test_screen_capture_initialization_headless():
    """Test that ScreenCapture initializes even if headless (without X server)."""
    # X11 connection should fail or bypass in test environment, but it shouldn't crash
    capture = ScreenCapture(quality=90)
    assert capture.quality == 90
    assert capture.monitor_number == 1
    # sct will be None if X display is not available, which is expected
    # But it shouldn't crash initialization


def test_screen_capture_methods_fallback():
    """Test that capture methods return valid dummy images if headless."""
    capture = ScreenCapture()
    # Mock self.sct to None to force fallback mode
    capture.sct = None

    screenshot = capture.capture_screenshot()
    assert isinstance(screenshot, Image.Image)
    assert screenshot.size == (800, 600)

    region = capture.capture_region(10, 20, 100, 20)
    assert isinstance(region, Image.Image)
    assert region.size == (100, 20)

    # Test conversion to base64 works with PIL Images
    b64_str = capture.to_base64(region)
    assert isinstance(b64_str, str)
    assert len(b64_str) > 0
