document.addEventListener('DOMContentLoaded', () => {
    // Quickstart Tab Switching Logic
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetTab = btn.getAttribute('data-tab');

            // Deactivate all buttons & contents
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            // Activate current
            btn.classList.add('active');
            document.getElementById(targetTab).classList.add('active');
        });
    });

    // Copy to Clipboard Logic
    const copyButtons = [
        { btn: 'copy-install-btn', content: 'tab-install' },
        { btn: 'copy-config-btn', content: 'tab-config' },
        { btn: 'copy-run-btn', content: 'tab-run' }
    ];

    copyButtons.forEach(item => {
        const btnEl = document.getElementById(item.btn);
        if (btnEl) {
            btnEl.addEventListener('click', () => {
                const contentEl = document.querySelector(`#${item.content} code`);
                if (contentEl) {
                    const textToCopy = contentEl.innerText;
                    navigator.clipboard.writeText(textToCopy).then(() => {
                        // Change button state
                        const originalHtml = btnEl.innerHTML;
                        btnEl.innerHTML = '<i class="fas fa-check"></i> Copied!';
                        btnEl.style.background = '#00f0ff';
                        btnEl.style.color = '#000000';

                        setTimeout(() => {
                            btnEl.innerHTML = originalHtml;
                            btnEl.style.background = '';
                            btnEl.style.color = '';
                        }, 2000);
                    }).catch(err => {
                        console.error('Could not copy text: ', err);
                    });
                }
            });
        }
    });

    // Interactive Terminal Simulation
    const terminalOutput = document.getElementById('terminal-output-container');
    const typedText = document.getElementById('typed-text');
    
    const simulationSteps = [
        {
            type: 'input',
            text: 'lucifer start --interactive'
        },
        {
            type: 'output',
            html: '<span class="output-info">[06/30/26 19:00:01] INFO - Initializing Lucifer AI Assistant...</span>\n' +
                  '<span class="output-info">[06/30/26 19:00:02] INFO - Session: 20260630_190002 started.</span>\n' +
                  '<span class="output-success">✓ ScreenCapture initialized (Running headless sandbox fallback)</span>\n' +
                  '<span class="output-success">✓ Async AI Engine client configured (anthropic-claude-3.5-sonnet)</span>\n' +
                  '\n' +
                  '<span class="prompt">lucifer&gt;</span> '
        },
        {
            type: 'input',
            text: 'workflow recon 192.168.1.15'
        },
        {
            type: 'output',
            html: '\n' +
                  '<span class="output-info">Executing workflow: Reconnaissance on 192.168.1.15</span>\n' +
                  '------------------------------------------------------------\n' +
                  '  <span class="output-warn">Running: nmap -sn 192.168.1.15</span>\n' +
                  '  Host is up (0.0012s latency).\n' +
                  '  <span class="output-success">✓ Host Discovery completed.</span>\n' +
                  '\n' +
                  '  <span class="output-warn">Running: nmap -p- -T4 192.168.1.15</span>\n' +
                  '  PORT    STATE SERVICE\n' +
                  '  22/tcp  open  ssh\n' +
                  '  80/tcp  open  http\n' +
                  '  443/tcp open  ssl/http\n' +
                  '  <span class="output-success">✓ Port Scan completed. Ports found: 22, 80, 443</span>\n' +
                  '\n' +
                  '<span class="output-info">[06/30/26 19:00:15] INFO - Querying AI engine for next actions...</span>\n' +
                  '\n' +
                  '======================= <span class="output-success">AI SUGGESTIONS</span> =======================\n' +
                  'Based on open ports (22, 80, 443), execute these steps:\n' +
                  '1. <span class="output-success">whatweb http://192.168.1.15</span> (Web technology identification)\n' +
                  '2. <span class="output-success">gobuster dir -u http://192.168.1.15 -w common.txt</span> (Directory fuzzing)\n' +
                  '3. <span class="output-success">nikto -h http://192.168.1.15</span> (Vulnerability scanning)\n' +
                  '============================================================\n' +
                  '\n' +
                  '<span class="prompt">lucifer&gt;</span> '
        },
        {
            type: 'input',
            text: 'report'
        },
        {
            type: 'output',
            html: '\n' +
                  '<span class="output-info">Generating session report...</span>\n' +
                  '<span class="output-success">✓ Report successfully saved as: reports/report_20260630_190002.html</span>\n' +
                  '<span class="output-success">✓ Report successfully saved as: reports/report_20260630_190002.md</span>\n' +
                  '\n' +
                  '<span class="prompt">lucifer&gt;</span> '
        },
        {
            type: 'input',
            text: 'exit'
        },
        {
            type: 'output',
            html: '\n' +
                  '<span class="output-info">Stopping Lucifer assistant...</span>\n' +
                  '<span class="output-info">[06/30/26 19:00:25] INFO - Lucifer assistant stopped.</span>\n' +
                  'Lucifer terminated.\n' +
                  '\n' +
                  '<span class="output-success">Thank you for using Lucifer!</span>'
        }
    ];

    let currentStep = 0;

    function typeWriter(text, i, fnCallback) {
        if (i < text.length) {
            typedText.innerHTML = text.substring(0, i+1) + '<span aria-hidden="true"></span>';
            setTimeout(() => {
                typeWriter(text, i + 1, fnCallback);
            }, 50);
        } else if (typeof fnCallback == 'function') {
            setTimeout(fnCallback, 1000);
        }
    }

    function runSimulation() {
        if (currentStep >= simulationSteps.length) {
            // Loop simulation after delay
            setTimeout(() => {
                terminalOutput.innerHTML = '';
                typedText.innerHTML = '';
                currentStep = 0;
                runSimulation();
            }, 6000);
            return;
        }

        const step = simulationSteps[currentStep];

        if (step.type === 'input') {
            typeWriter(step.text, 0, () => {
                // Add input line to output history
                terminalOutput.innerHTML += `<div class="terminal-line"><span class="prompt">lucifer@assistant:~$</span> ${step.text}</div>`;
                typedText.innerHTML = '';
                currentStep++;
                runSimulation();
            });
        } else if (step.type === 'output') {
            terminalOutput.innerHTML += `<div>${step.html}</div>`;
            currentStep++;
            // Scroll to bottom of terminal
            const demoTerm = document.getElementById('demo-terminal');
            demoTerm.scrollTop = demoTerm.scrollHeight;
            
            setTimeout(() => {
                runSimulation();
            }, 1500);
        }
    }

    // Start simulation
    runSimulation();
});
