import React from 'react';
import styled from 'styled-components';
import { FiZap, FiClock } from 'react-icons/fi';

const PanelContainer = styled.div`
  width: 350px;
  background: #252525;
  border-left: 1px solid #333;
  display: flex;
  flex-direction: column;
  overflow: hidden;
`;

const PanelHeader = styled.div`
  padding: 15px 20px;
  background: #2d2d2d;
  border-bottom: 1px solid #333;
  font-weight: bold;
  color: #ff4444;
  display: flex;
  align-items: center;
  gap: 10px;
`;

const SuggestionsArea = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 15px;
`;

const SuggestionItem = styled.div`
  background: #1e1e1e;
  border: 1px solid #333;
  border-left: 3px solid #ff4444;
  padding: 12px 15px;
  margin-bottom: 10px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'Courier New', monospace;
  font-size: 13px;

  &:hover {
    background: #2d2d2d;
    border-left-color: #ff6666;
    transform: translateX(5px);
  }

  .command {
    color: #4ec9b0;
    margin-bottom: 5px;
  }

  .description {
    color: #888;
    font-size: 11px;
  }
`;

const EmptyState = styled.div`
  text-align: center;
  color: #666;
  padding: 40px 20px;
  
  svg {
    font-size: 48px;
    margin-bottom: 15px;
    opacity: 0.3;
  }
`;

const OutputPanel = ({ suggestions, onSuggestionClick }) => {
  return (
    <PanelContainer>
      <PanelHeader>
        <FiZap /> AI Suggestions
      </PanelHeader>
      <SuggestionsArea>
        {suggestions.length === 0 ? (
          <EmptyState>
            <FiClock />
            <p>No suggestions yet</p>
            <p style={{ fontSize: '12px', marginTop: '5px' }}>
              Execute commands to get AI-powered suggestions
            </p>
          </EmptyState>
        ) : (
          suggestions.map((suggestion, index) => (
            <SuggestionItem 
              key={index}
              onClick={() => onSuggestionClick(suggestion)}
            >
              <div className="command">{suggestion}</div>
              <div className="description">Click to execute</div>
            </SuggestionItem>
          ))
        )}
      </SuggestionsArea>
    </PanelContainer>
  );
};

export default OutputPanel;
