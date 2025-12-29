"""Flask server for GUI integration."""

import asyncio
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

from lucifer.core.assistant import LuciferAssistant
from lucifer.core.config import get_config
from lucifer.automation.workflows import WorkflowManager
from lucifer.utils.logger import get_logger

app = Flask(__name__)
CORS(app)
logger = get_logger(__name__)

# Global assistant instance
assistant = None
workflow_manager = None


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'ok', 'message': 'Lucifer backend is running'})


@app.route('/api/execute', methods=['POST'])
async def execute_command():
    """Execute a command."""
    try:
        data = request.json
        command = data.get('command')
        
        if not command:
            return jsonify({'error': 'No command provided'}), 400
        
        # Execute command
        output = await assistant.execute_command(command, confirm=False)
        
        return jsonify({
            'success': True,
            'output': output or 'Command executed'
        })
    except Exception as e:
        logger.error(f"Command execution error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/suggest', methods=['POST'])
async def get_suggestions():
    """Get AI suggestions."""
    try:
        data = request.json
        context = data.get('context', '')
        
        # Get suggestions
        suggestions = await assistant.suggest_next_actions()
        
        return jsonify({
            'suggestions': suggestions
        })
    except Exception as e:
        logger.error(f"Suggestions error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/analyze', methods=['POST'])
async def analyze_state():
    """Analyze current state."""
    try:
        # Analyze state
        analysis = await assistant.analyze_current_state()
        
        return jsonify({
            'analysis': analysis
        })
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/workflow/<workflow_name>', methods=['POST'])
async def run_workflow(workflow_name):
    """Run a workflow."""
    try:
        data = request.json
        target = data.get('target')
        
        if not target:
            return jsonify({'error': 'No target provided'}), 400
        
        context = {'target': target, 'ports': '80,443'}
        results = await workflow_manager.execute_workflow(workflow_name, context)
        
        return jsonify({
            'success': True,
            'results': results
        })
    except Exception as e:
        logger.error(f"Workflow error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/report', methods=['POST'])
async def generate_report():
    """Generate report."""
    try:
        report_path = await assistant.generate_report()
        
        return jsonify({
            'success': True,
            'reportPath': str(report_path)
        })
    except Exception as e:
        logger.error(f"Report generation error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/config', methods=['GET'])
def get_configuration():
    """Get current configuration."""
    try:
        config = get_config()
        
        return jsonify({
            'aiProvider': config.ai_provider.value,
            'logLevel': config.log_level.value,
            'confirmationRequired': config.confirmation_required,
            'ocrEnabled': config.ocr_enabled,
        })
    except Exception as e:
        logger.error(f"Config error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/config', methods=['POST'])
def update_configuration():
    """Update configuration."""
    try:
        data = request.json
        # Update config logic here
        
        return jsonify({
            'success': True,
            'message': 'Configuration updated'
        })
    except Exception as e:
        logger.error(f"Config update error: {e}")
        return jsonify({'error': str(e)}), 500


async def initialize_assistant():
    """Initialize the assistant."""
    global assistant, workflow_manager
    
    assistant = LuciferAssistant()
    await assistant.start_terminal_monitoring()
    
    workflow_manager = WorkflowManager(
        assistant.ai_engine,
        assistant.terminal_capture
    )
    
    logger.info("Lucifer assistant initialized")


def main():
    """Main entry point."""
    logger.info("Starting Lucifer backend server...")
    
    # Initialize assistant
    loop = asyncio.get_event_loop()
    loop.run_until_complete(initialize_assistant())
    
    # Start Flask server
    app.run(host='127.0.0.1', port=5000, debug=False)


if __name__ == '__main__':
    main()
