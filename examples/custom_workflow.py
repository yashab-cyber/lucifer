"""
Example: Custom workflow creation

This example shows how to create and execute custom workflows.
"""

import asyncio
from lucifer import LuciferAssistant
from lucifer.automation.workflows import WorkflowManager, WorkflowStep, PentestWorkflow


async def main():
    """Create and run a custom workflow."""
    assistant = LuciferAssistant()

    try:
        await assistant.start_terminal_monitoring()

        # Create custom workflow
        custom_workflow = PentestWorkflow(
            name="Custom API Testing",
            description="Test API endpoints for vulnerabilities",
            ai_engine=assistant.ai_engine,
            terminal_capture=assistant.terminal_capture,
        )

        # Add custom steps
        custom_workflow.add_step(
            WorkflowStep(
                name="API Discovery",
                command="curl -s {target}/api/v1/ | jq .",
                description="Discover API endpoints",
                timeout=30,
            )
        )

        custom_workflow.add_step(
            WorkflowStep(
                name="Test Authentication",
                command="curl -X POST {target}/api/v1/auth -d '{}'",
                description="Test authentication endpoint",
                timeout=20,
            )
        )

        # Execute workflow
        target = "https://api.example.com"
        results = await custom_workflow.execute({"target": target})

        print("Workflow completed!")
        print(f"Steps executed: {len(results['steps'])}")

    finally:
        assistant.stop()


if __name__ == "__main__":
    asyncio.run(main())
