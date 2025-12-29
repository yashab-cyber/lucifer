const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  executeCommand: (command) => ipcRenderer.invoke('execute-command', command),
  getSuggestions: (context) => ipcRenderer.invoke('get-suggestions', context),
  analyzeState: () => ipcRenderer.invoke('analyze-state'),
  generateReport: () => ipcRenderer.invoke('generate-report'),
  
  // Event listeners
  onNewSession: (callback) => ipcRenderer.on('new-session', callback),
  onOpenSettings: (callback) => ipcRenderer.on('open-settings', callback),
  onRunWorkflow: (callback) => ipcRenderer.on('run-workflow', (event, workflow) => callback(workflow)),
  onShowAbout: (callback) => ipcRenderer.on('show-about', callback),
  
  // Remove listeners
  removeListener: (channel) => ipcRenderer.removeAllListeners(channel)
});
