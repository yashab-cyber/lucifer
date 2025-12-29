"""Configuration management for Lucifer."""

import os
from enum import Enum
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AIProvider(str, Enum):
    """Supported AI providers."""

    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    OLLAMA = "ollama"


class LogLevel(str, Enum):
    """Logging levels."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class Config(BaseSettings):
    """Main configuration class for Lucifer."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # AI Provider Configuration
    ai_provider: AIProvider = Field(default=AIProvider.ANTHROPIC)
    
    # Anthropic Configuration
    anthropic_api_key: Optional[str] = Field(default=None)
    anthropic_model: str = Field(default="claude-3-5-sonnet-20241022")
    
    # OpenAI Configuration
    openai_api_key: Optional[str] = Field(default=None)
    openai_model: str = Field(default="gpt-4-turbo-preview")
    
    # Ollama Configuration
    ollama_base_url: str = Field(default="http://localhost:11434")
    ollama_model: str = Field(default="llama2")

    # Terminal Capture Settings
    terminal_capture_buffer_size: int = Field(default=10000)
    terminal_capture_interval: float = Field(default=0.5)

    # Screenshot Settings
    screenshot_interval: float = Field(default=2.0)
    screenshot_quality: int = Field(default=95, ge=1, le=100)
    ocr_enabled: bool = Field(default=True)
    ocr_language: str = Field(default="eng")

    # Logging Configuration
    log_level: LogLevel = Field(default=LogLevel.INFO)
    log_file: Path = Field(default=Path("logs/lucifer.log"))

    # Automation Settings
    auto_suggest_commands: bool = Field(default=True)
    auto_execute_safe_commands: bool = Field(default=False)
    confirmation_required: bool = Field(default=True)

    # Security Settings
    dangerous_commands_filter: bool = Field(default=True)
    audit_log_enabled: bool = Field(default=True)
    audit_log_file: Path = Field(default=Path("logs/audit.log"))

    # Report Settings
    report_format: str = Field(default="markdown")
    report_dir: Path = Field(default=Path("reports"))
    auto_generate_report: bool = Field(default=True)

    def __init__(self, **kwargs):
        """Initialize configuration and create necessary directories."""
        super().__init__(**kwargs)
        self._create_directories()

    def _create_directories(self) -> None:
        """Create necessary directories if they don't exist."""
        directories = [
            self.log_file.parent,
            self.audit_log_file.parent,
            self.report_dir,
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    def validate_ai_credentials(self) -> bool:
        """Validate that required AI credentials are present."""
        if self.ai_provider == AIProvider.ANTHROPIC:
            return bool(self.anthropic_api_key)
        elif self.ai_provider == AIProvider.OPENAI:
            return bool(self.openai_api_key)
        elif self.ai_provider == AIProvider.OLLAMA:
            return True  # Ollama doesn't require API key
        return False


# Global config instance
_config: Optional[Config] = None


def get_config() -> Config:
    """Get or create the global config instance."""
    global _config
    if _config is None:
        _config = Config()
    return _config


def reset_config() -> None:
    """Reset the global config instance (useful for testing)."""
    global _config
    _config = None
