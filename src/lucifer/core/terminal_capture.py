"""Terminal output capture and monitoring."""

import asyncio
import os
import pty
import select
import subprocess
import threading
import time
from collections import deque
from datetime import datetime
from pathlib import Path
from typing import Callable, Deque, Optional

import pyte


class TerminalCapture:
    """Captures and monitors terminal output."""

    def __init__(
        self,
        buffer_size: int = 10000,
        callback: Optional[Callable[[str], None]] = None,
    ):
        """
        Initialize terminal capture.

        Args:
            buffer_size: Maximum number of lines to keep in buffer
            callback: Optional callback function called with new output
        """
        self.buffer_size = buffer_size
        self.callback = callback
        self.output_buffer: Deque[str] = deque(maxlen=buffer_size)
        self.screen = pyte.Screen(80, 24)
        self.stream = pyte.Stream(self.screen)
        self._capturing = False
        self._capture_thread: Optional[threading.Thread] = None
        self._process: Optional[subprocess.Popen] = None
        self._master_fd: Optional[int] = None
        self._lock = threading.Lock()

    def start_shell_capture(self, shell: str = "/bin/bash") -> None:
        """
        Start capturing a new shell session.

        Args:
            shell: Path to shell executable
        """
        if self._capturing:
            raise RuntimeError("Already capturing")

        self._capturing = True
        self._capture_thread = threading.Thread(
            target=self._capture_loop, args=(shell,), daemon=True
        )
        self._capture_thread.start()

    def _capture_loop(self, shell: str) -> None:
        """Main capture loop running in separate thread."""
        try:
            # Create pseudo-terminal
            self._master_fd, slave_fd = pty.openpty()

            # Start shell process
            self._process = subprocess.Popen(
                [shell],
                stdin=slave_fd,
                stdout=slave_fd,
                stderr=slave_fd,
                start_new_session=True,
            )

            os.close(slave_fd)

            # Read output from master
            while self._capturing:
                ready, _, _ = select.select([self._master_fd], [], [], 0.1)
                if ready:
                    try:
                        data = os.read(self._master_fd, 1024)
                        if not data:
                            break

                        # Decode and process output
                        text = data.decode("utf-8", errors="replace")
                        self._process_output(text)

                    except OSError:
                        break

        except Exception as e:
            print(f"Terminal capture error: {e}")
        finally:
            self._cleanup()

    def _process_output(self, text: str) -> None:
        """Process captured output."""
        with self._lock:
            # Feed to pyte screen emulator
            self.stream.feed(text)

            # Get current screen display
            display = "\n".join(self.screen.display)

            # Add to buffer
            timestamp = datetime.now().isoformat()
            entry = f"[{timestamp}] {display}"
            self.output_buffer.append(entry)

            # Call callback if provided
            if self.callback:
                try:
                    self.callback(text)
                except Exception as e:
                    print(f"Callback error: {e}")

    def send_command(self, command: str) -> None:
        """
        Send command to the captured shell.

        Args:
            command: Command to execute
        """
        if not self._capturing or self._master_fd is None:
            raise RuntimeError("Not capturing")

        command_bytes = (command + "\n").encode("utf-8")
        os.write(self._master_fd, command_bytes)

    def get_recent_output(self, lines: int = 50) -> str:
        """
        Get recent output from buffer.

        Args:
            lines: Number of recent lines to retrieve

        Returns:
            Recent output as string
        """
        with self._lock:
            recent = list(self.output_buffer)[-lines:]
            return "\n".join(recent)

    def get_all_output(self) -> str:
        """Get all buffered output."""
        with self._lock:
            return "\n".join(self.output_buffer)

    def stop(self) -> None:
        """Stop capturing."""
        self._capturing = False
        if self._capture_thread:
            self._capture_thread.join(timeout=2.0)
        self._cleanup()

    def _cleanup(self) -> None:
        """Clean up resources."""
        if self._process:
            try:
                self._process.terminate()
                self._process.wait(timeout=1.0)
            except Exception:
                try:
                    self._process.kill()
                except Exception:
                    pass
            self._process = None

        if self._master_fd is not None:
            try:
                os.close(self._master_fd)
            except Exception:
                pass
            self._master_fd = None

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()


class TerminalMonitor:
    """Monitors terminal output and triggers actions based on patterns."""

    def __init__(self, capture: TerminalCapture):
        """
        Initialize terminal monitor.

        Args:
            capture: TerminalCapture instance to monitor
        """
        self.capture = capture
        self.patterns: dict[str, Callable[[str], None]] = {}
        self._monitoring = False
        self._monitor_thread: Optional[threading.Thread] = None

    def add_pattern(self, pattern: str, callback: Callable[[str], None]) -> None:
        """
        Add pattern to monitor for.

        Args:
            pattern: String pattern to match
            callback: Function to call when pattern is found
        """
        self.patterns[pattern] = callback

    def start_monitoring(self) -> None:
        """Start monitoring terminal output."""
        if self._monitoring:
            return

        self._monitoring = True
        self._monitor_thread = threading.Thread(
            target=self._monitoring_loop, daemon=True
        )
        self._monitor_thread.start()

    def _monitoring_loop(self) -> None:
        """Monitoring loop."""
        last_position = 0

        while self._monitoring:
            output = self.capture.get_all_output()
            new_output = output[last_position:]

            if new_output:
                for pattern, callback in self.patterns.items():
                    if pattern in new_output:
                        try:
                            callback(new_output)
                        except Exception as e:
                            print(f"Pattern callback error: {e}")

                last_position = len(output)

            time.sleep(0.5)

    def stop_monitoring(self) -> None:
        """Stop monitoring."""
        self._monitoring = False
        if self._monitor_thread:
            self._monitor_thread.join(timeout=2.0)
