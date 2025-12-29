import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import Terminal from './components/Terminal';
import OutputPanel from './components/OutputPanel';
import WorkflowPanel from './components/WorkflowPanel';
import SettingsModal from './components/SettingsModal';
import AboutModal from './components/AboutModal';
import DonateModal from './components/DonateModal';

const AppContainer = styled.div`
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: #1e1e1e;
  color: #d4d4d4;
`;

const MainContent = styled.div`
  display: flex;
  flex: 1;
  overflow: hidden;
`;

const CenterPanel = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
`;

function App() {
  const [activeTab, setActiveTab] = useState('terminal');
  const [terminalOutput, setTerminalOutput] = useState([]);
  const [suggestions, setSuggestions] = useState([]);
  const [showSettings, setShowSettings] = useState(false);
  const [showAbout, setShowAbout] = useState(false);
  const [showDonate, setShowDonate] = useState(false);
  const [currentWorkflow, setCurrentWorkflow] = useState(null);

  useEffect(() => {
    // Setup Electron IPC listeners
    if (window.electronAPI) {
      window.electronAPI.onNewSession(() => {
        setTerminalOutput([]);
        setSuggestions([]);
      });

      window.electronAPI.onOpenSettings(() => {
        setShowSettings(true);
      });

      window.electronAPI.onRunWorkflow((workflow) => {
        setCurrentWorkflow(workflow);
        setActiveTab('workflow');
      });

      window.electronAPI.onShowAbout(() => {
        setShowAbout(true);
      });
    }

    return () => {
      if (window.electronAPI) {
        window.electronAPI.removeListener('new-session');
        window.electronAPI.removeListener('open-settings');
        window.electronAPI.removeListener('run-workflow');
        window.electronAPI.removeListener('show-about');
      }
    };
  }, []);

  const handleCommandExecute = async (command) => {
    const newOutput = {
      timestamp: new Date().toISOString(),
      command: command,
      output: 'Executing...'
    };
    setTerminalOutput([...terminalOutput, newOutput]);

    if (window.electronAPI) {
      const result = await window.electronAPI.executeCommand(command);
      setTerminalOutput(prev => [
        ...prev.slice(0, -1),
        { ...newOutput, output: result.output || 'Command executed' }
      ]);

      // Get AI suggestions
      const suggestionsResult = await window.electronAPI.getSuggestions(command);
      setSuggestions(suggestionsResult.suggestions || []);
    }
  };

  const handleAnalyze = async () => {
    if (window.electronAPI) {
      const result = await window.electronAPI.analyzeState();
      setTerminalOutput([...terminalOutput, {
        timestamp: new Date().toISOString(),
        command: 'analyze',
        output: JSON.stringify(result, null, 2)
      }]);
    }
  };

  const handleGenerateReport = async () => {
    if (window.electronAPI) {
      const result = await window.electronAPI.generateReport();
      alert(`Report generated: ${result.reportPath}`);
    }
  };

  return (
    <AppContainer>
      <Header 
        onAnalyze={handleAnalyze}
        onGenerateReport={handleGenerateReport}
        onShowAbout={() => setShowAbout(true)}
        onShowDonate={() => setShowDonate(true)}
      />
      <MainContent>
        <Sidebar 
          activeTab={activeTab}
          setActiveTab={setActiveTab}
        />
        <CenterPanel>
          {activeTab === 'terminal' && (
            <Terminal 
              output={terminalOutput}
              onExecute={handleCommandExecute}
            />
          )}
          {activeTab === 'workflow' && (
            <WorkflowPanel 
              workflow={currentWorkflow}
              onExecute={handleCommandExecute}
            />
          )}
          {activeTab === 'output' && (
            <OutputPanel 
              output={terminalOutput}
            />
          )}
        </CenterPanel>
        <OutputPanel 
          suggestions={suggestions}
          onSuggestionClick={handleCommandExecute}
        />
      </MainContent>
      
      {showSettings && (
        <SettingsModal onClose={() => setShowSettings(false)} />
      )}
      
      {showAbout && (
        <AboutModal onClose={() => setShowAbout(false)} />
      )}
      
      {showDonate && (
        <DonateModal onClose={() => setShowDonate(false)} />
      )}
    </AppContainer>
  );
}

export default App;
