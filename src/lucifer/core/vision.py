"""Computer vision and GUI capture functionality."""

import base64
import io
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import cv2
import mss
import numpy as np
import pytesseract
from PIL import Image


class ScreenCapture:
    """Handles screen capture and processing."""

    def __init__(self, quality: int = 95, monitor_number: int = 1):
        """
        Initialize screen capture.

        Args:
            quality: JPEG quality (1-100)
            monitor_number: Monitor to capture (1-indexed)
        """
        self.quality = quality
        self.monitor_number = monitor_number
        try:
            self.sct = mss.MSS()
        except Exception as e:
            import sys
            print(f"Warning: Failed to initialize mss ScreenCapture (no X display?): {e}", file=sys.stderr)
            self.sct = None

    def capture_screenshot(self) -> Image.Image:
        """
        Capture current screen.

        Returns:
            PIL Image of the screen
        """
        if not self.sct:
            return Image.new("RGB", (800, 600), color="black")
        monitor = self.sct.monitors[self.monitor_number]
        screenshot = self.sct.grab(monitor)
        img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
        return img

    def capture_region(
        self, x: int, y: int, width: int, height: int
    ) -> Image.Image:
        """
        Capture specific screen region.

        Args:
            x: X coordinate
            y: Y coordinate
            width: Width of region
            height: Height of region

        Returns:
            PIL Image of the region
        """
        if not self.sct:
            return Image.new("RGB", (width, height), color="black")
        monitor = {"top": y, "left": x, "width": width, "height": height}
        screenshot = self.sct.grab(monitor)
        img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
        return img

    def save_screenshot(self, filepath: Path, img: Optional[Image.Image] = None) -> None:
        """
        Save screenshot to file.

        Args:
            filepath: Path to save screenshot
            img: Optional image to save, captures new one if None
        """
        if img is None:
            img = self.capture_screenshot()

        filepath.parent.mkdir(parents=True, exist_ok=True)
        img.save(filepath, quality=self.quality, optimize=True)

    def to_base64(self, img: Image.Image) -> str:
        """
        Convert image to base64 string.

        Args:
            img: PIL Image

        Returns:
            Base64 encoded string
        """
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=self.quality)
        return base64.b64encode(buffer.getvalue()).decode("utf-8")


class OCREngine:
    """Optical Character Recognition engine."""

    def __init__(self, language: str = "eng"):
        """
        Initialize OCR engine.

        Args:
            language: Tesseract language code
        """
        self.language = language

    def extract_text(self, img: Image.Image) -> str:
        """
        Extract text from image.

        Args:
            img: PIL Image

        Returns:
            Extracted text
        """
        try:
            text = pytesseract.image_to_string(img, lang=self.language)
            return text.strip()
        except Exception as e:
            print(f"OCR error: {e}")
            return ""

    def extract_text_with_boxes(
        self, img: Image.Image
    ) -> List[Dict[str, any]]:
        """
        Extract text with bounding boxes.

        Args:
            img: PIL Image

        Returns:
            List of dicts with text and bounding box info
        """
        try:
            data = pytesseract.image_to_data(
                img, lang=self.language, output_type=pytesseract.Output.DICT
            )
            results = []
            for i, text in enumerate(data["text"]):
                if text.strip():
                    results.append({
                        "text": text,
                        "x": data["left"][i],
                        "y": data["top"][i],
                        "width": data["width"][i],
                        "height": data["height"][i],
                        "confidence": data["conf"][i],
                    })
            return results
        except Exception as e:
            print(f"OCR error: {e}")
            return []


class ImageAnalyzer:
    """Analyzes images for security-relevant information."""

    def __init__(self):
        """Initialize image analyzer."""
        self.ocr = OCREngine()

    def detect_terminals(self, img: Image.Image) -> List[Dict[str, any]]:
        """
        Detect terminal windows in screenshot.

        Args:
            img: PIL Image

        Returns:
            List of detected terminal regions
        """
        # Convert to OpenCV format
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

        # Detect dark regions (terminals are typically dark)
        _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)

        # Find contours
        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        terminals = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            # Filter by size (terminals are usually large)
            if w > 400 and h > 300:
                terminals.append({"x": x, "y": y, "width": w, "height": h})

        return terminals

    def find_text_in_image(self, img: Image.Image, search_text: str) -> List[Dict]:
        """
        Find specific text in image.

        Args:
            img: PIL Image
            search_text: Text to search for

        Returns:
            List of locations where text was found
        """
        text_boxes = self.ocr.extract_text_with_boxes(img)
        matches = []

        search_lower = search_text.lower()
        for box in text_boxes:
            if search_lower in box["text"].lower():
                matches.append(box)

        return matches

    def detect_ui_elements(self, img: Image.Image) -> Dict[str, List[Dict]]:
        """
        Detect various UI elements (buttons, text fields, etc.).

        Args:
            img: PIL Image

        Returns:
            Dictionary of detected UI elements by type
        """
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

        # Detect edges
        edges = cv2.Canny(gray, 50, 150)

        # Find contours for potential UI elements
        contours, _ = cv2.findContours(
            edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )

        buttons = []
        text_fields = []

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / float(h) if h > 0 else 0

            # Heuristic: buttons are wider than tall, moderate size
            if 1.5 < aspect_ratio < 5 and 50 < w < 300 and 20 < h < 60:
                buttons.append({"x": x, "y": y, "width": w, "height": h})

            # Heuristic: text fields are long and thin
            elif aspect_ratio > 5 and 100 < w < 500 and 15 < h < 40:
                text_fields.append({"x": x, "y": y, "width": w, "height": h})

        return {"buttons": buttons, "text_fields": text_fields}


class ScreenRecorder:
    """Records screen activity for analysis."""

    def __init__(self, fps: int = 2, output_dir: Path = Path("recordings")):
        """
        Initialize screen recorder.

        Args:
            fps: Frames per second
            output_dir: Directory to save recordings
        """
        self.fps = fps
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.capture = ScreenCapture()
        self._recording = False
        self._frames: List[Image.Image] = []

    def start_recording(self) -> None:
        """Start recording screen."""
        self._recording = True
        self._frames = []

        import threading

        def record_loop():
            while self._recording:
                frame = self.capture.capture_screenshot()
                self._frames.append(frame)
                time.sleep(1.0 / self.fps)

        self._thread = threading.Thread(target=record_loop, daemon=True)
        self._thread.start()

    def stop_recording(self) -> Path:
        """
        Stop recording and save video.

        Returns:
            Path to saved video file
        """
        self._recording = False
        if hasattr(self, "_thread"):
            self._thread.join(timeout=2.0)

        # Save frames as video
        if not self._frames:
            raise ValueError("No frames recorded")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = self.output_dir / f"recording_{timestamp}.mp4"

        # Convert frames to video using OpenCV
        first_frame = np.array(self._frames[0])
        height, width = first_frame.shape[:2]

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(
            str(output_path), fourcc, self.fps, (width, height)
        )

        for frame in self._frames:
            frame_cv = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
            out.write(frame_cv)

        out.release()
        self._frames = []

        return output_path
