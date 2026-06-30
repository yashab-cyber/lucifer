"""Main Lucifer AI Assistant."""

import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from lucifer.core.ai_engine import AIEngine, create_ai_engine
from lucifer.core.config import Config, get_config
from lucifer.core.terminal_capture import TerminalCapture, TerminalMonitor
from lucifer.core.vision import ImageAnalyzer, OCREngine, ScreenCapture, ScreenRecorder
from lucifer.utils.logger import get_logger
from lucifer.utils.report_generator import ReportGenerator


class LuciferAssistant:
    """Main AI assistant for cybersecurity automation."""

    def __init__(self, config: Optional[Config] = None):
        """
        Initialize Lucifer assistant.

        Args:
            config: Optional configuration, uses global if None
        """
        self.config = config or get_config()
        self.logger = get_logger(__name__)
        self.console = Console()

        # Initialize components
        self.ai_engine: AIEngine = create_ai_engine(self.config)
        self.terminal_capture: Optional[TerminalCapture] = None
        self.terminal_monitor: Optional[TerminalMonitor] = None
        self.screen_capture = ScreenCapture(quality=self.config.screenshot_quality)
        self.ocr_engine = OCREngine(language=self.config.ocr_language)
        self.image_analyzer = ImageAnalyzer()
        self.screen_recorder: Optional[ScreenRecorder] = None
        self.report_generator = ReportGenerator(
            output_dir=self.config.report_dir,
            format=self.config.report_format,
        )

        # Session state
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_data: Dict = {
            "start_time": datetime.now().isoformat(),
            "commands": [],
            "findings": [],
            "screenshots": [],
        }

        self.logger.info(f"Lucifer assistant initialized - Session: {self.session_id}")

    async def start_terminal_monitoring(self, shell: str = "/bin/bash") -> None:
        """
        Start monitoring terminal output.

        Args:
            shell: Shell to monitor
        """
        if self.terminal_capture is not None:
            self.logger.warning("Terminal monitoring already active")
            return

        self.console.print("[green]Starting terminal monitoring...[/green]")

        # Create terminal capture with callback
        def on_output(text: str):
            self._handle_terminal_output(text)

        self.terminal_capture = TerminalCapture(
            buffer_size=self.config.terminal_capture_buffer_size,
            callback=on_output,
        )

        self.terminal_capture.start_shell_capture(shell)

        # Set up terminal monitor for pattern matching
        self.terminal_monitor = TerminalMonitor(self.terminal_capture)
        self._setup_pattern_monitoring()
        self.terminal_monitor.start_monitoring()

        self.logger.info("Terminal monitoring started")

    def _handle_terminal_output(self, text: str) -> None:
        """Handle new terminal output."""
        # Log output
        self.logger.debug(f"Terminal output: {text[:100]}...")

        # Check for interesting patterns
        if any(
            pattern in text.lower()
            for pattern in ["error", "failed", "denied", "vulnerable", "exploit"]
        ):
            self.session_data["findings"].append({
                "timestamp": datetime.now().isoformat(),
                "type": "terminal_output",
                "content": text,
            })

    def _setup_pattern_monitoring(self) -> None:
        """Set up pattern-based monitoring."""
        if not self.terminal_monitor:
            return

        # Monitor for interesting security patterns
        patterns = {
            "root@": lambda text: self.logger.info("Root access detected"),
            "Password:": lambda text: self.logger.info("Password prompt detected"),
            "exploit": lambda text: self.logger.info("Exploit activity detected"),
            "shell": lambda text: self.logger.info("Shell access detected"),
        }

        for pattern, callback in patterns.items():
            self.terminal_monitor.add_pattern(pattern, callback)

    async def analyze_current_state(self) -> Dict:
        """
        Analyze current terminal and screen state.

        Returns:
            Analysis results
        """
        self.console.print("[yellow]Analyzing current state...[/yellow]")

        results = {"timestamp": datetime.now().isoformat()}

        # Capture and analyze terminal output
        if self.terminal_capture:
            terminal_output = self.terminal_capture.get_recent_output(lines=50)
            terminal_analysis = await self.ai_engine.analyze_terminal_output(
                terminal_output
            )
            results["terminal_analysis"] = terminal_analysis

        # Capture and analyze screenshot
        screenshot = self.screen_capture.capture_screenshot()
        screenshot_path = (
            self.config.report_dir / f"screenshot_{self.session_id}_{len(self.session_data['screenshots'])}.jpg"
        )
        self.screen_capture.save_screenshot(screenshot_path, screenshot)
        self.session_data["screenshots"].append(str(screenshot_path))

        # OCR extraction
        if self.config.ocr_enabled:
            ocr_text = self.ocr_engine.extract_text(screenshot)
            results["ocr_text"] = ocr_text

        # Vision analysis
        screenshot_analysis = await self.ai_engine.analyze_screenshot(screenshot)
        results["screenshot_analysis"] = screenshot_analysis

        # Detect UI elements
        ui_elements = self.image_analyzer.detect_ui_elements(screenshot)
        results["ui_elements"] = ui_elements

        self.logger.info("State analysis completed")
        return results

    async def suggest_next_actions(self) -> List[str]:
        """
        Get AI suggestions for next actions.

        Returns:
            List of suggested commands/actions
        """
        self.console.print("[cyan]Getting AI suggestions...[/cyan]")

        terminal_output = ""
        if self.terminal_capture:
            terminal_output = self.terminal_capture.get_recent_output(lines=100)

        suggestions = await self.ai_engine.suggest_next_steps(terminal_output)

        # Display suggestions
        self.console.print(Panel.fit(
            "\n".join(f"{i+1}. {cmd}" for i, cmd in enumerate(suggestions)),
            title="[bold]Suggested Next Steps[/bold]",
            border_style="cyan",
        ))

        return suggestions

    async def execute_command(
        self, command: str, confirm: bool = True
    ) -> Optional[str]:
        """
        Execute a command in the monitored terminal.

        Args:
            command: Command to execute
            confirm: Whether to require confirmation

        Returns:
            Command output or None if cancelled
        """
        # Check if command is dangerous
        if self.config.dangerous_commands_filter and self._is_dangerous_command(command):
            self.console.print(f"[red]Warning: Potentially dangerous command: {command}[/red]")
            if confirm and not self._confirm_action(f"Execute: {command}"):
                return None

        # Confirm execution
        if confirm and self.config.confirmation_required:
            if not self._confirm_action(f"Execute: {command}"):
                return None

        # Log command
        self.session_data["commands"].append({
            "timestamp": datetime.now().isoformat(),
            "command": command,
        })

        # Execute in terminal
        if self.terminal_capture:
            self.terminal_capture.send_command(command)
            await asyncio.sleep(2)  # Wait for output
            output = self.terminal_capture.get_recent_output(lines=20)
            return output
        else:
            self.logger.warning("No terminal capture active")
            return None

    def _is_dangerous_command(self, command: str) -> bool:
        """Check if command is potentially dangerous."""
        dangerous_patterns = [
            "rm -rf",
            "dd if=",
            "mkfs",
            "format",
            ":(){:|:&};:",  # Fork bomb
            "chmod 777",
            "chmod -R 777",
        ]
        return any(pattern in command for pattern in dangerous_patterns)

    def _confirm_action(self, prompt: str) -> bool:
        """Ask user for confirmation."""
        from prompt_toolkit import prompt as pt_prompt

        response = pt_prompt(f"{prompt} (y/n): ")
        return response.lower() in ["y", "yes"]

    async def run_automated_recon(self, target: str) -> Dict:
        """
        Run automated reconnaissance on target.

        Args:
            target: Target IP/domain

        Returns:
            Reconnaissance results
        """
        self.console.print(f"[bold cyan]Starting automated recon on {target}[/bold cyan]")

        results = {
            "target": target,
            "timestamp": datetime.now().isoformat(),
            "scans": {},
        }

        # Define recon commands
        recon_commands = [
            f"nmap -sV -sC {target}",
            f"nmap -p- {target}",
            f"whatweb {target}",
            f"dig {target}",
            f"whois {target}",
        ]

        for cmd in recon_commands:
            self.console.print(f"[yellow]Running: {cmd}[/yellow]")
            output = await self.execute_command(cmd, confirm=False)
            if output:
                results["scans"][cmd] = output

                # Analyze output
                analysis = await self.ai_engine.analyze_terminal_output(
                    output, context=f"Reconnaissance scan: {cmd}"
                )
                results["scans"][f"{cmd}_analysis"] = analysis

        return results

    def start_recording(self) -> None:
        """Start recording screen activity."""
        if self.screen_recorder is None:
            self.screen_recorder = ScreenRecorder(
                fps=2, output_dir=self.config.report_dir / "recordings"
            )
        self.screen_recorder.start_recording()
        self.console.print("[green]Screen recording started[/green]")

    def stop_recording(self) -> Path:
        """Stop recording and save video."""
        if self.screen_recorder is None:
            raise RuntimeError("No recording in progress")

        video_path = self.screen_recorder.stop_recording()
        self.console.print(f"[green]Recording saved: {video_path}[/green]")
        return video_path

    async def generate_report(self) -> Path:
        """
        Generate final report.

        Returns:
            Path to generated report
        """
        self.console.print("[cyan]Generating report...[/cyan]")

        # Add session end time
        self.session_data["end_time"] = datetime.now().isoformat()

        # Generate report
        report_path = self.report_generator.generate_report(
            session_id=self.session_id,
            data=self.session_data,
        )

        self.console.print(f"[green]Report generated: {report_path}[/green]")
        return report_path

    def stop(self) -> None:
        """Stop the assistant and clean up."""
        self.console.print("[yellow]Stopping Lucifer assistant...[/yellow]")

        if self.terminal_monitor:
            self.terminal_monitor.stop_monitoring()

        if self.terminal_capture:
            self.terminal_capture.stop()

        if self.screen_recorder and self.screen_recorder._recording:
            self.stop_recording()

        # Generate final report if auto-generate enabled
        if self.config.auto_generate_report:
            try:
                loop = asyncio.get_running_loop()
                if loop.is_running():
                    loop.create_task(self.generate_report())
                else:
                    asyncio.run(self.generate_report())
            except RuntimeError:
                try:
                    asyncio.run(self.generate_report())
                except Exception as e:
                    self.logger.error(f"Failed to generate report: {e}")

        self.logger.info("Lucifer assistant stopped")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()
