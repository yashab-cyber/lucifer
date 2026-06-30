# Lucifer v1.0.0 - Stability & Performance Release

We are excited to announce the first official stable release of **Lucifer (v1.0.0)**! This release introduces critical stability fixes, headless environment robustness, fully asynchronous AI engines, expanded unit testing, and dependency updates.

---

## 🚀 Key Improvements & Bug Fixes

### 1. 🖥 Headless & Containerized Execution Support
- **Issue:** Previously, `ScreenCapture` initialized screenshot mechanisms (`mss.MSS()`) unconditionally. In headless environments (CI/CD pipelines, Docker containers, or SSH sessions) lacking a running X11 server, this caused the assistant to crash on startup, preventing even basic CLI operations from running.
- **Fix:** Handled X11 connection failures gracefully during initialization. `ScreenCapture` now flags when a display is missing and falls back to generating a blank placeholder image on capture rather than throwing exceptions and crashing.

### 2. ⚡ Event-Loop-Aware CLI Teardown
- **Issue:** On application stop, `LuciferAssistant.stop()` scheduled asynchronous report generation using `asyncio.create_task()`. When called from synchronous contexts or after the main loop exited, this resulted in `RuntimeError: no running event loop` and crashed CLI termination.
- **Fix:** Upgraded teardown logic to safely detect active event loops. It schedules report generation on the running loop if active, runs it synchronously using `asyncio.run()` if inactive, and catches failures gracefully.

### 3. 🔄 Fully Asynchronous AI Engines
- **Issue:** While methods like `analyze_terminal_output` were defined as async coroutines, they called blocking, synchronous SDK clients internally (`anthropic.Anthropic` and `openai.OpenAI`), which blocked the single-threaded event loop during API calls.
- **Fix:** Ported `AnthropicEngine` and `OpenAIEngine` to use modern asynchronous clients (`AsyncAnthropic` and `AsyncOpenAI`) and awaited all completion requests.

### 4. 🎛 Fixed Terminal Monitoring CPU Spin
- **Issue:** The terminal capture background thread loop used `asyncio.sleep(0.5)` without awaiting it inside a non-async thread. This did not pause execution, causing a `RuntimeWarning` and pinning the CPU core at 100%.
- **Fix:** Switched to `time.sleep(0.5)` for correct background thread sleeping.
- **Improvement:** Replaced deprecated `preexec_fn=os.setsid` in `subprocess.Popen` with the modern `start_new_session=True` parameter to avoid process deadlocks in multi-threaded environments.

### 5. 📦 Dependency Cleanups
- **Issue:** Missing standard project dependencies (`jinja2`, `flask`, `flask-cors`) caused import errors during server execution. An obsolete PyPI package dependency on `asyncio` was also present.
- **Fix:** Added missing packages to `dependencies` in `pyproject.toml` and removed the built-in `asyncio` library dependency.

---

## 🧪 Enhanced Unit Test Coverage
We introduced comprehensive unit tests to ensure long-term stability:
- **`tests/test_vision.py`**: Tests the new headless environment fallback behavior of `ScreenCapture`.
- **`tests/test_report_generator.py`**: Tests the generation of Markdown, HTML, and JSON reports (increasing `ReportGenerator` coverage to **98%**).
- **Results:** Overall project test coverage has increased to **24%**, and all tests pass with zero warnings.

---

## 📥 Installation & Getting Started

```bash
# Clone the repository
git clone https://github.com/yashab-cyber/luciferSec.git
cd luciferSec

# Run the installation script
./install.sh

# Activate virtualenv
source venv/bin/activate

# Verify configuration
lucifer config-check

# Start interactive assistant
lucifer start --interactive
```

---
*Created with ❤️ by Yashab Alam*
