"""Test configuration for pytest."""

import pytest


@pytest.fixture
def sample_terminal_output():
    """Sample terminal output for testing."""
    return """
root@kali:~# nmap -sV 192.168.1.100
Starting Nmap 7.94 ( https://nmap.org )
Nmap scan report for 192.168.1.100
Host is up (0.0010s latency).
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.2p1
80/tcp   open  http    Apache httpd 2.4.41
443/tcp  open  ssl/http Apache httpd 2.4.41
"""


@pytest.fixture
def mock_config():
    """Mock configuration for testing."""
    from lucifer.core.config import Config

    return Config(
        ai_provider="anthropic",
        anthropic_api_key="test_key",
        terminal_capture_buffer_size=1000,
        confirmation_required=False,
    )
