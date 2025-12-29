"""
Example: Screenshot analysis

This example demonstrates computer vision and screenshot analysis.
"""

import asyncio
from lucifer import LuciferAssistant
from pathlib import Path


async def main():
    """Analyze screenshots with AI."""
    assistant = LuciferAssistant()

    try:
        print("Capturing and analyzing screenshot...")

        # Capture current screen
        screenshot = assistant.screen_capture.capture_screenshot()

        # Save screenshot
        screenshot_path = Path("example_screenshot.jpg")
        assistant.screen_capture.save_screenshot(screenshot_path, screenshot)
        print(f"Screenshot saved: {screenshot_path}")

        # Extract text with OCR
        if assistant.config.ocr_enabled:
            text = assistant.ocr_engine.extract_text(screenshot)
            print(f"\nExtracted text:\n{text[:200]}...")

        # Analyze with AI
        print("\nAnalyzing screenshot with AI...")
        analysis = await assistant.ai_engine.analyze_screenshot(
            screenshot,
            question="What security-related information is visible in this screenshot?"
        )

        print(f"\nAI Analysis:\n{analysis['analysis']}")

        # Detect UI elements
        ui_elements = assistant.image_analyzer.detect_ui_elements(screenshot)
        print(f"\nDetected UI elements:")
        print(f"- Buttons: {len(ui_elements['buttons'])}")
        print(f"- Text fields: {len(ui_elements['text_fields'])}")

    finally:
        assistant.stop()


if __name__ == "__main__":
    asyncio.run(main())
