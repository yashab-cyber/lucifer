const { app, BrowserWindow, ipcMain, Menu } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow;
let pythonProcess;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 1200,
    minHeight: 700,
    icon: path.join(__dirname, '../public/icon.png'),
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    },
    backgroundColor: '#1e1e1e',
    title: 'Lucifer - AI Cybersecurity Assistant',
    autoHideMenuBar: false,
  });

  // Create application menu
  const template = [
    {
      label: 'File',
      submenu: [
        {
          label: 'New Session',
          accelerator: 'CmdOrCtrl+N',
          click: () => {
            mainWindow.webContents.send('new-session');
          }
        },
        { type: 'separator' },
        {
          label: 'Settings',
          accelerator: 'CmdOrCtrl+,',
          click: () => {
            mainWindow.webContents.send('open-settings');
          }
        },
        { type: 'separator' },
        { role: 'quit' }
      ]
    },
    {
      label: 'Edit',
      submenu: [
        { role: 'undo' },
        { role: 'redo' },
        { type: 'separator' },
        { role: 'cut' },
        { role: 'copy' },
        { role: 'paste' }
      ]
    },
    {
      label: 'View',
      submenu: [
        { role: 'reload' },
        { role: 'forceReload' },
        { role: 'toggleDevTools' },
        { type: 'separator' },
        { role: 'resetZoom' },
        { role: 'zoomIn' },
        { role: 'zoomOut' },
        { type: 'separator' },
        { role: 'togglefullscreen' }
      ]
    },
    {
      label: 'Workflows',
      submenu: [
        {
          label: 'Reconnaissance',
          click: () => {
            mainWindow.webContents.send('run-workflow', 'recon');
          }
        },
        {
          label: 'Web Application',
          click: () => {
            mainWindow.webContents.send('run-workflow', 'webapp');
          }
        },
        {
          label: 'Exploitation',
          click: () => {
            mainWindow.webContents.send('run-workflow', 'exploit');
          }
        },
        {
          label: 'Privilege Escalation',
          click: () => {
            mainWindow.webContents.send('run-workflow', 'privesc');
          }
        }
      ]
    },
    {
      label: 'Help',
      submenu: [
        {
          label: 'Documentation',
          click: async () => {
            const { shell } = require('electron');
            await shell.openExternal('https://github.com/yashab-cyber/lucifer');
          }
        },
        {
          label: 'Report Issue',
          click: async () => {
            const { shell } = require('electron');
            await shell.openExternal('https://github.com/yashab-cyber/lucifer/issues');
          }
        },
        { type: 'separator' },
        {
          label: 'About',
          click: () => {
            mainWindow.webContents.send('show-about');
          }
        }
      ]
    }
  ];

  const menu = Menu.buildFromTemplate(template);
  Menu.setApplicationMenu(menu);

  // Load the app
  const startUrl = process.env.ELECTRON_START_URL || `file://${path.join(__dirname, '../build/index.html')}`;
  mainWindow.loadURL(startUrl);

  // Open DevTools in development
  if (process.env.NODE_ENV === 'development') {
    mainWindow.webContents.openDevTools();
  }

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

// Start Python backend
function startPythonBackend() {
  const pythonPath = process.env.PYTHON_PATH || 'python3';
  const scriptPath = path.join(__dirname, '../../src/lucifer/server.py');

  pythonProcess = spawn(pythonPath, [scriptPath]);

  pythonProcess.stdout.on('data', (data) => {
    console.log(`Python: ${data}`);
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`Python Error: ${data}`);
  });

  pythonProcess.on('close', (code) => {
    console.log(`Python process exited with code ${code}`);
  });
}

app.whenReady().then(() => {
  createWindow();
  startPythonBackend();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (pythonProcess) {
    pythonProcess.kill();
  }
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// IPC handlers
ipcMain.handle('execute-command', async (event, command) => {
  // Send command to Python backend
  return { success: true, output: 'Command executed' };
});

ipcMain.handle('get-suggestions', async (event, context) => {
  // Get AI suggestions from Python backend
  return { suggestions: ['nmap -sV target', 'gobuster dir -u target'] };
});

ipcMain.handle('analyze-state', async (event) => {
  // Analyze current state
  return { analysis: 'System analyzed' };
});

ipcMain.handle('generate-report', async (event) => {
  // Generate report
  return { reportPath: '/path/to/report.html' };
});
