"""AI engine for analyzing terminal output and screenshots."""

import asyncio
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

import anthropic
import httpx
import openai
from PIL import Image

from lucifer.core.config import AIProvider, Config, get_config
from lucifer.core.vision import ScreenCapture


class AIEngine(ABC):
    """Abstract base class for AI engines."""

    @abstractmethod
    async def analyze_terminal_output(
        self, output: str, context: Optional[str] = None
    ) -> Dict[str, Any]:
        """Analyze terminal output and provide insights."""
        pass

    @abstractmethod
    async def analyze_screenshot(
        self, image: Image.Image, question: Optional[str] = None
    ) -> Dict[str, Any]:
        """Analyze screenshot and provide insights."""
        pass

    @abstractmethod
    async def suggest_next_steps(
        self, terminal_output: str, screenshot: Optional[Image.Image] = None
    ) -> List[str]:
        """Suggest next steps based on current state."""
        pass

    @abstractmethod
    async def generate_exploit(
        self, vulnerability: str, target_info: Dict[str, Any]
    ) -> str:
        """Generate exploit code or commands."""
        pass


class AnthropicEngine(AIEngine):
    """Anthropic Claude AI engine."""

    def __init__(self, config: Config):
        """Initialize Anthropic engine."""
        self.config = config
        self.client = anthropic.Anthropic(api_key=config.anthropic_api_key)
        self.model = config.anthropic_model
        self.screen_capture = ScreenCapture()

    async def analyze_terminal_output(
        self, output: str, context: Optional[str] = None
    ) -> Dict[str, Any]:
        """Analyze terminal output using Claude."""
        prompt = f"""You are a cybersecurity expert analyzing terminal output from a penetration testing session.

Terminal Output:
{output}

{f"Context: {context}" if context else ""}

Please analyze this output and provide:
1. Summary of what's happening
2. Any vulnerabilities or interesting findings
3. Potential security issues
4. Recommended next steps

Provide your analysis in JSON format with keys: summary, findings, vulnerabilities, recommendations."""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                messages=[{"role": "user", "content": prompt}],
            )

            response_text = message.content[0].text

            # Parse response (simplified - in production, use proper JSON parsing)
            return {
                "analysis": response_text,
                "model": self.model,
                "timestamp": message.id,
            }

        except Exception as e:
            return {"error": str(e)}

    async def analyze_screenshot(
        self, image: Image.Image, question: Optional[str] = None
    ) -> Dict[str, Any]:
        """Analyze screenshot using Claude's vision capabilities."""
        # Convert image to base64
        base64_image = self.screen_capture.to_base64(image)

        prompt = question or "Analyze this screenshot from a security perspective. Identify any relevant information, potential vulnerabilities, or interesting findings."

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/jpeg",
                                    "data": base64_image,
                                },
                            },
                            {"type": "text", "text": prompt},
                        ],
                    }
                ],
            )

            return {
                "analysis": message.content[0].text,
                "model": self.model,
                "timestamp": message.id,
            }

        except Exception as e:
            return {"error": str(e)}

    async def suggest_next_steps(
        self, terminal_output: str, screenshot: Optional[Image.Image] = None
    ) -> List[str]:
        """Suggest next penetration testing steps."""
        prompt = f"""Based on this penetration testing session output, suggest the next 3-5 most effective steps:

Terminal Output:
{terminal_output}

Provide specific, actionable commands or techniques. Focus on:
- Enumeration techniques
- Vulnerability exploitation
- Privilege escalation
- Lateral movement
- Data exfiltration

Return ONLY a JSON array of command strings."""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}],
            )

            response_text = message.content[0].text

            # Extract suggestions (simplified parsing)
            import json
            import re

            # Try to find JSON array in response
            match = re.search(r'\[.*\]', response_text, re.DOTALL)
            if match:
                return json.loads(match.group(0))
            else:
                # Fallback: split by newlines
                return [
                    line.strip()
                    for line in response_text.split("\n")
                    if line.strip()
                ][:5]

        except Exception as e:
            return [f"Error generating suggestions: {e}"]

    async def generate_exploit(
        self, vulnerability: str, target_info: Dict[str, Any]
    ) -> str:
        """Generate exploit code or commands."""
        prompt = f"""Generate an exploit or attack commands for the following vulnerability:

Vulnerability: {vulnerability}

Target Information:
{target_info}

Provide:
1. Exploit code or commands
2. Explanation of how it works
3. Prerequisites
4. Expected outcome

Format as executable script or commands with comments."""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                messages=[{"role": "user", "content": prompt}],
            )

            return message.content[0].text

        except Exception as e:
            return f"Error generating exploit: {e}"


class OpenAIEngine(AIEngine):
    """OpenAI GPT AI engine."""

    def __init__(self, config: Config):
        """Initialize OpenAI engine."""
        self.config = config
        self.client = openai.OpenAI(api_key=config.openai_api_key)
        self.model = config.openai_model
        self.screen_capture = ScreenCapture()

    async def analyze_terminal_output(
        self, output: str, context: Optional[str] = None
    ) -> Dict[str, Any]:
        """Analyze terminal output using GPT."""
        prompt = f"""You are a cybersecurity expert analyzing terminal output.

Terminal Output:
{output}

{f"Context: {context}" if context else ""}

Analyze and provide: summary, findings, vulnerabilities, recommendations."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2048,
            )

            return {
                "analysis": response.choices[0].message.content,
                "model": self.model,
                "timestamp": response.id,
            }

        except Exception as e:
            return {"error": str(e)}

    async def analyze_screenshot(
        self, image: Image.Image, question: Optional[str] = None
    ) -> Dict[str, Any]:
        """Analyze screenshot using GPT-4 Vision."""
        base64_image = self.screen_capture.to_base64(image)

        prompt = question or "Analyze this screenshot from a security perspective."

        try:
            response = self.client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                },
                            },
                        ],
                    }
                ],
                max_tokens=2048,
            )

            return {
                "analysis": response.choices[0].message.content,
                "model": self.model,
                "timestamp": response.id,
            }

        except Exception as e:
            return {"error": str(e)}

    async def suggest_next_steps(
        self, terminal_output: str, screenshot: Optional[Image.Image] = None
    ) -> List[str]:
        """Suggest next steps."""
        prompt = f"""Based on this pentest output, suggest next 3-5 steps:

{terminal_output}

Return JSON array of commands."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1024,
            )

            import json
            import re

            text = response.choices[0].message.content
            match = re.search(r'\[.*\]', text, re.DOTALL)
            if match:
                return json.loads(match.group(0))
            return text.split("\n")[:5]

        except Exception as e:
            return [f"Error: {e}"]

    async def generate_exploit(
        self, vulnerability: str, target_info: Dict[str, Any]
    ) -> str:
        """Generate exploit code."""
        prompt = f"""Generate exploit for: {vulnerability}
Target: {target_info}

Provide exploit code/commands with explanation."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2048,
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"Error: {e}"


class OllamaEngine(AIEngine):
    """Ollama local AI engine."""

    def __init__(self, config: Config):
        """Initialize Ollama engine."""
        self.config = config
        self.base_url = config.ollama_base_url
        self.model = config.ollama_model

    async def _call_ollama(self, prompt: str) -> str:
        """Call Ollama API."""
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.base_url}/api/generate",
                json={"model": self.model, "prompt": prompt, "stream": False},
            )
            return response.json()["response"]

    async def analyze_terminal_output(
        self, output: str, context: Optional[str] = None
    ) -> Dict[str, Any]:
        """Analyze terminal output using Ollama."""
        prompt = f"""Analyze this terminal output from a security perspective:

{output}

Provide summary, findings, and recommendations."""

        try:
            response = await self._call_ollama(prompt)
            return {"analysis": response, "model": self.model}
        except Exception as e:
            return {"error": str(e)}

    async def analyze_screenshot(
        self, image: Image.Image, question: Optional[str] = None
    ) -> Dict[str, Any]:
        """Ollama vision support varies by model."""
        return {
            "error": "Screenshot analysis requires vision-capable model. Use LLaVA or similar."
        }

    async def suggest_next_steps(
        self, terminal_output: str, screenshot: Optional[Image.Image] = None
    ) -> List[str]:
        """Suggest next steps."""
        prompt = f"""Based on this output, suggest next pentest steps:

{terminal_output}

List 3-5 specific commands."""

        try:
            response = await self._call_ollama(prompt)
            return [line.strip() for line in response.split("\n") if line.strip()][:5]
        except Exception as e:
            return [f"Error: {e}"]

    async def generate_exploit(
        self, vulnerability: str, target_info: Dict[str, Any]
    ) -> str:
        """Generate exploit code."""
        prompt = f"""Generate exploit for {vulnerability}. Target: {target_info}"""

        try:
            return await self._call_ollama(prompt)
        except Exception as e:
            return f"Error: {e}"


def create_ai_engine(config: Optional[Config] = None) -> AIEngine:
    """
    Factory function to create appropriate AI engine.

    Args:
        config: Optional config, uses global if None

    Returns:
        AIEngine instance
    """
    if config is None:
        config = get_config()

    if config.ai_provider == AIProvider.ANTHROPIC:
        return AnthropicEngine(config)
    elif config.ai_provider == AIProvider.OPENAI:
        return OpenAIEngine(config)
    elif config.ai_provider == AIProvider.OLLAMA:
        return OllamaEngine(config)
    else:
        raise ValueError(f"Unsupported AI provider: {config.ai_provider}")
