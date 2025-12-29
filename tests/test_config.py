"""Unit tests for configuration."""

import pytest
from lucifer.core.config import Config, AIProvider


def test_config_defaults():
    """Test default configuration values."""
    config = Config()
    assert config.ai_provider == AIProvider.ANTHROPIC
    assert config.log_level.value == "INFO"
    assert config.confirmation_required is True


def test_config_validation():
    """Test configuration validation."""
    # Without API key
    config = Config()
    assert config.validate_ai_credentials() is False

    # With API key
    config = Config(anthropic_api_key="test_key")
    assert config.validate_ai_credentials() is True
