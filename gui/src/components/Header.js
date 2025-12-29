import React from 'react';
import styled from 'styled-components';
import { FiActivity, FiSettings, FiFileText, FiZap, FiHeart, FiInfo } from 'react-icons/fi';

const HeaderContainer = styled.header`
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 20px;
  background: linear-gradient(135deg, #2d0a0e 0%, #1e1e1e 100%);
  border-bottom: 2px solid #ff4444;
  box-shadow: 0 2px 10px rgba(255, 68, 68, 0.3);
`;

const LogoSection = styled.div`
  display: flex;
  align-items: center;
  gap: 15px;
`;

const Logo = styled.img`
  height: 40px;
  width: 40px;
  filter: drop-shadow(0 0 10px rgba(255, 68, 68, 0.5));
`;

const Title = styled.h1`
  font-size: 24px;
  font-weight: bold;
  background: linear-gradient(135deg, #ff4444 0%, #ff8844 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin: 0;
  letter-spacing: 2px;
`;

const Subtitle = styled.div`
  font-size: 11px;
  color: #888;
  margin-top: -2px;
`;

const Actions = styled.div`
  display: flex;
  gap: 10px;
`;

const ActionButton = styled.button`
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: ${props => props.primary ? '#ff4444' : props.donate ? '#ff4499' : 'transparent'};
  border: 2px solid ${props => props.primary ? '#ff4444' : props.donate ? '#ff4499' : '#555'};
  color: ${props => props.primary || props.donate ? '#fff' : '#d4d4d4'};
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;

  &:hover {
    background: ${props => props.primary ? '#ff6666' : props.donate ? '#ff66aa' : '#333'};
    border-color: ${props => props.primary ? '#ff6666' : props.donate ? '#ff66aa' : '#ff4444'};
    transform: translateY(-2px);
    box-shadow: 0 4px 12px ${props => props.donate ? 'rgba(255, 68, 153, 0.4)' : 'rgba(255, 68, 68, 0.3)'};
  }

  &:active {
    transform: translateY(0);
  }
`;

const CreatorBadge = styled.div`
  font-size: 10px;
  color: #888;
  display: flex;
  align-items: center;
  gap: 4px;
  margin-right: 10px;
  
  a {
    color: #ff4499;
    text-decoration: none;
    font-weight: 600;
    
    &:hover {
      color: #ff66aa;
      text-decoration: underline;
    }
  }
`;

const Header = ({ onAnalyze, onGenerateReport, onShowAbout, onShowDonate }) => {
  return (
    <HeaderContainer>
      <LogoSection>
        <Logo src="/icon.png" alt="Lucifer" />
        <div>
          <Title>LUCIFER</Title>
          <Subtitle>AI Cybersecurity Automation Assistant</Subtitle>
        </div>
      </LogoSection>
      <Actions>
        <CreatorBadge>
          Made with ❤️ by <a href="https://www.linkedin.com/in/yashab-alam" target="_blank" rel="noopener noreferrer">Yashab Alam</a>
        </CreatorBadge>
        <ActionButton onClick={onAnalyze}>
          <FiActivity /> Analyze
        </ActionButton>
        <ActionButton onClick={onGenerateReport}>
          <FiFileText /> Report
        </ActionButton>
        <ActionButton onClick={onShowAbout}>
          <FiInfo /> About
        </ActionButton>
        <ActionButton donate onClick={onShowDonate}>
          <FiHeart /> Donate
        </ActionButton>
        <ActionButton primary>
          <FiZap /> AI Assist
        </ActionButton>
      </Actions>
    </HeaderContainer>
  );
};

export default Header;
