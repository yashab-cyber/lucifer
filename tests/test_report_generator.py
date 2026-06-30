"""Unit tests for report generator utility."""

import json
from pathlib import Path
import pytest
from lucifer.utils.report_generator import ReportGenerator


def test_report_generator_formats(tmp_path):
    """Test report generation in different formats."""
    session_id = "test_session_123"
    data = {
        "start_time": "2026-06-30T12:00:00",
        "end_time": "2026-06-30T13:00:00",
        "commands": [
            {"timestamp": "2026-06-30T12:05:00", "command": "nmap localhost"}
        ],
        "findings": [
            {"timestamp": "2026-06-30T12:10:00", "type": "port_scan", "content": "Port 80 open"}
        ],
        "screenshots": []
    }

    # 1. Test Markdown Report
    generator_md = ReportGenerator(output_dir=tmp_path, format="markdown")
    md_path = generator_md.generate_report(session_id, data)
    assert md_path.exists()
    assert md_path.name == f"report_{session_id}.md"
    content_md = md_path.read_text()
    assert "Lucifer Penetration Testing Report" in content_md
    assert "nmap localhost" in content_md
    assert "Port 80 open" in content_md

    # 2. Test HTML Report
    generator_html = ReportGenerator(output_dir=tmp_path, format="html")
    html_path = generator_html.generate_report(session_id, data)
    assert html_path.exists()
    assert html_path.name == f"report_{session_id}.html"
    content_html = html_path.read_text()
    assert "🔥 Lucifer Penetration Testing Report" in content_html
    assert "nmap localhost" in content_html

    # 3. Test JSON Report
    generator_json = ReportGenerator(output_dir=tmp_path, format="json")
    json_path = generator_json.generate_report(session_id, data)
    assert json_path.exists()
    assert json_path.name == f"report_{session_id}.json"
    with open(json_path) as f:
        json_data = json.load(f)
    assert json_data["session_id"] == session_id
    assert json_data["data"]["commands"][0]["command"] == "nmap localhost"


def test_unsupported_format(tmp_path):
    """Test that unsupported formats raise ValueError."""
    generator = ReportGenerator(output_dir=tmp_path, format="pdf")
    with pytest.raises(ValueError, match="Unsupported format: pdf"):
        generator.generate_report("session_1", {})
