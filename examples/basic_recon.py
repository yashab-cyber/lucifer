"""
Example: Basic reconnaissance workflow

This example demonstrates how to use Lucifer to perform
automated reconnaissance on a target.
"""

import asyncio
from lucifer import LuciferAssistant


async def main():
    """Run basic reconnaissance."""
    # Create assistant instance
    assistant = LuciferAssistant()

    try:
        print("Starting Lucifer Assistant...")

        # Start terminal monitoring
        await assistant.start_terminal_monitoring()

        # Define target
        target = "scanme.nmap.org"  # Example target (authorized for scanning)

        print(f"\nRunning reconnaissance on {target}...")

        # Run automated reconnaissance
        results = await assistant.run_automated_recon(target)

        print("\n✓ Reconnaissance completed!")
        print(f"Scans performed: {len(results['scans'])}")

        # Get AI suggestions for next steps
        print("\nGetting AI suggestions...")
        suggestions = await assistant.suggest_next_actions()

        print("\nSuggested next steps:")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"{i}. {suggestion}")

        # Generate report
        print("\nGenerating report...")
        report_path = await assistant.generate_report()
        print(f"✓ Report saved to: {report_path}")

    finally:
        # Clean up
        assistant.stop()


if __name__ == "__main__":
    asyncio.run(main())
