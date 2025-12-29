"""
Lucifer - AI-powered cybersecurity automation assistant.

An intelligent assistant for penetration testing and bug bounty hunting that captures
terminal output and GUI interactions using computer vision to provide AI-powered
automation and assistance.
"""

__version__ = "1.0.0"
__author__ = "Lucifer Team"
__license__ = "MIT"

from lucifer.core.assistant import LuciferAssistant
from lucifer.core.config import Config

__all__ = ["LuciferAssistant", "Config"]
