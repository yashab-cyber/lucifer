"""Unit tests for terminal capture functionality."""

import pytest
from lucifer.core.terminal_capture import TerminalCapture


def test_terminal_capture_initialization():
    """Test terminal capture initialization."""
    capture = TerminalCapture(buffer_size=100)
    assert capture.buffer_size == 100
    assert len(capture.output_buffer) == 0


def test_terminal_capture_output_buffer():
    """Test output buffer management."""
    capture = TerminalCapture(buffer_size=10)

    # Add some output
    for i in range(15):
        capture.output_buffer.append(f"line {i}")

    # Buffer should be limited to size
    assert len(capture.output_buffer) == 10
