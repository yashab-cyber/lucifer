import React, { useState } from 'react';
import styled from 'styled-components';
import { FiX, FiSave } from 'react-icons/fi';

const Overlay = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
`;

const Modal = styled.div`
  background: #2d2d2d;
  border: 2px solid #ff4444;
  border-radius: 12px;
  width: 700px;
  max-width: 90%;
  max-height: 90vh;
  overflow-y: auto;
`;

const Header = styled.div`
  padding: 20px 30px;
  border-bottom: 1px solid #444;
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const Title = styled.h2`
  margin: 0;
  color: #ff4444;
`;

const CloseButton = styled.button`
  background: transparent;
  border: none;
  color: #888;
  cursor: pointer;
  font-size: 24px;
  
  &:hover {
    color: #ff4444;
  }
`;

const Content = styled.div`
  padding: 30px;
`;

const Section = styled.div`
  margin-bottom: 25px;
`;

const Label = styled.label`
  display: block;
  color: #4ec9b0;
  margin-bottom: 8px;
  font-weight: 500;
`;

const Input = styled.input`
  width: 100%;
  padding: 10px 15px;
  background: #1e1e1e;
  border: 2px solid #333;
  color: #d4d4d4;
  border-radius: 6px;
  font-size: 14px;

  &:focus {
    outline: none;
    border-color: #ff4444;
  }
`;

const Select = styled.select`
  width: 100%;
  padding: 10px 15px;
  background: #1e1e1e;
  border: 2px solid #333;
  color: #d4d4d4;
  border-radius: 6px;
  font-size: 14px;

  &:focus {
    outline: none;
    border-color: #ff4444;
  }
`;

const SaveButton = styled.button`
  width: 100%;
  padding: 12px;
  background: #ff4444;
  border: none;
  color: white;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  font-size: 16px;
  margin-top: 20px;

  &:hover {
    background: #ff6666;
  }
`;

const SettingsModal = ({ onClose }) => {
  const [settings, setSettings] = useState({
    aiProvider: 'anthropic',
    apiKey: '',
    logLevel: 'INFO',
    confirmCommands: true,
  });

  const handleSave = () => {
    // Save settings logic here
    alert('Settings saved!');
    onClose();
  };

  return (
    <Overlay onClick={onClose}>
      <Modal onClick={(e) => e.stopPropagation()}>
        <Header>
          <Title>Settings</Title>
          <CloseButton onClick={onClose}>
            <FiX />
          </CloseButton>
        </Header>
        <Content>
          <Section>
            <Label>AI Provider</Label>
            <Select
              value={settings.aiProvider}
              onChange={(e) => setSettings({...settings, aiProvider: e.target.value})}
            >
              <option value="anthropic">Anthropic (Claude)</option>
              <option value="openai">OpenAI (GPT-4)</option>
              <option value="ollama">Ollama (Local)</option>
            </Select>
          </Section>

          <Section>
            <Label>API Key</Label>
            <Input
              type="password"
              value={settings.apiKey}
              onChange={(e) => setSettings({...settings, apiKey: e.target.value})}
              placeholder="Enter your API key..."
            />
          </Section>

          <Section>
            <Label>Log Level</Label>
            <Select
              value={settings.logLevel}
              onChange={(e) => setSettings({...settings, logLevel: e.target.value})}
            >
              <option value="DEBUG">DEBUG</option>
              <option value="INFO">INFO</option>
              <option value="WARNING">WARNING</option>
              <option value="ERROR">ERROR</option>
            </Select>
          </Section>

          <SaveButton onClick={handleSave}>
            <FiSave /> Save Settings
          </SaveButton>
        </Content>
      </Modal>
    </Overlay>
  );
};

export default SettingsModal;
