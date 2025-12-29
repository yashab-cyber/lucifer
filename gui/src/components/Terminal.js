import React, { useState, useRef, useEffect } from 'react';
import styled from 'styled-components';
import { FiSend } from 'react-icons/fi';

const TerminalContainer = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #1e1e1e;
  overflow: hidden;
`;

const OutputArea = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  font-family: 'Courier New', monospace;
  font-size: 14px;
  line-height: 1.6;
`;

const OutputLine = styled.div`
  margin-bottom: 15px;
  
  .timestamp {
    color: #666;
    font-size: 12px;
  }
  
  .command {
    color: #4ec9b0;
    margin: 5px 0;
    
    &::before {
      content: '❯ ';
      color: #ff4444;
      font-weight: bold;
    }
  }
  
  .output {
    color: #d4d4d4;
    white-space: pre-wrap;
    margin-left: 20px;
  }
`;

const InputArea = styled.div`
  display: flex;
  align-items: center;
  padding: 15px 20px;
  background: #252525;
  border-top: 1px solid #333;
  gap: 10px;
`;

const Prompt = styled.span`
  color: #ff4444;
  font-weight: bold;
  font-family: 'Courier New', monospace;
`;

const Input = styled.input`
  flex: 1;
  background: #1e1e1e;
  border: 2px solid #333;
  color: #d4d4d4;
  padding: 10px 15px;
  font-family: 'Courier New', monospace;
  font-size: 14px;
  border-radius: 6px;
  outline: none;
  
  &:focus {
    border-color: #ff4444;
  }
`;

const SendButton = styled.button`
  background: #ff4444;
  border: none;
  color: #fff;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
  transition: all 0.3s ease;
  
  &:hover {
    background: #ff6666;
    transform: translateY(-2px);
  }
  
  &:active {
    transform: translateY(0);
  }
`;

const Terminal = ({ output, onExecute }) => {
  const [command, setCommand] = useState('');
  const outputRef = useRef(null);

  useEffect(() => {
    if (outputRef.current) {
      outputRef.current.scrollTop = outputRef.current.scrollHeight;
    }
  }, [output]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (command.trim()) {
      onExecute(command);
      setCommand('');
    }
  };

  return (
    <TerminalContainer>
      <OutputArea ref={outputRef}>
        {output.length === 0 && (
          <div style={{ color: '#666', textAlign: 'center', marginTop: '100px' }}>
            <p>Welcome to Lucifer Terminal</p>
            <p style={{ fontSize: '12px', marginTop: '10px' }}>
              Type commands or use AI suggestions to get started
            </p>
          </div>
        )}
        {output.map((item, index) => (
          <OutputLine key={index}>
            <div className="timestamp">{new Date(item.timestamp).toLocaleTimeString()}</div>
            <div className="command">{item.command}</div>
            <div className="output">{item.output}</div>
          </OutputLine>
        ))}
      </OutputArea>
      <InputArea>
        <Prompt>lucifer❯</Prompt>
        <form onSubmit={handleSubmit} style={{ flex: 1, display: 'flex', gap: '10px' }}>
          <Input
            type="text"
            value={command}
            onChange={(e) => setCommand(e.target.value)}
            placeholder="Enter command..."
            autoFocus
          />
          <SendButton type="submit">
            <FiSend /> Execute
          </SendButton>
        </form>
      </InputArea>
    </TerminalContainer>
  );
};

export default Terminal;
