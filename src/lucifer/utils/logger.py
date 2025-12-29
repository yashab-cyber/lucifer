"""Logging utilities."""

import logging
import sys
from pathlib import Path
from typing import Optional

from rich.logging import RichHandler

from lucifer.core.config import get_config


def setup_logger(
    name: str,
    log_file: Optional[Path] = None,
    level: Optional[str] = None,
) -> logging.Logger:
    """
    Set up a logger with file and console handlers.

    Args:
        name: Logger name
        log_file: Optional log file path
        level: Optional log level

    Returns:
        Configured logger
    """
    config = get_config()

    # Get log level
    if level is None:
        level = config.log_level.value

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Remove existing handlers
    logger.handlers = []

    # Console handler with Rich
    console_handler = RichHandler(
        rich_tracebacks=True,
        tracebacks_show_locals=True,
        markup=True,
    )
    console_handler.setLevel(level)
    console_formatter = logging.Formatter("%(message)s")
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File handler
    log_path = log_file or config.log_file
    log_path.parent.mkdir(parents=True, exist_ok=True)

    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(level)
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get or create a logger.

    Args:
        name: Logger name

    Returns:
        Logger instance
    """
    logger = logging.getLogger(name)

    # Set up logger if not already configured
    if not logger.handlers:
        setup_logger(name)

    return logger


class AuditLogger:
    """Audit logger for security-sensitive operations."""

    def __init__(self):
        """Initialize audit logger."""
        config = get_config()
        self.enabled = config.audit_log_enabled
        if self.enabled:
            self.logger = setup_logger(
                "audit",
                log_file=config.audit_log_file,
                level="INFO",
            )

    def log_command(self, command: str, user: str = "system") -> None:
        """Log executed command."""
        if self.enabled:
            self.logger.info(f"COMMAND | User: {user} | Command: {command}")

    def log_access(self, resource: str, action: str, user: str = "system") -> None:
        """Log resource access."""
        if self.enabled:
            self.logger.info(f"ACCESS | User: {user} | Action: {action} | Resource: {resource}")

    def log_security_event(self, event: str, details: str = "") -> None:
        """Log security event."""
        if self.enabled:
            self.logger.warning(f"SECURITY | Event: {event} | Details: {details}")
