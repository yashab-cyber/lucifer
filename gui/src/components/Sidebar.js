import React from 'react';
import styled from 'styled-components';
import { FiTerminal, FiLayers, FiActivity, FiSettings } from 'react-icons/fi';

const SidebarContainer = styled.aside`
  width: 70px;
  background: #252525;
  border-right: 1px solid #333;
  display: flex;
  flex-direction: column;
  padding: 20px 0;
  gap: 10px;
`;

const SidebarButton = styled.button`
  width: 100%;
  padding: 15px 0;
  background: ${props => props.active ? '#ff4444' : 'transparent'};
  border: none;
  color: ${props => props.active ? '#fff' : '#888'};
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
  font-size: 10px;

  &:hover {
    background: ${props => props.active ? '#ff4444' : '#333'};
    color: #fff;
  }

  svg {
    font-size: 24px;
  }
`;

const Sidebar = ({ activeTab, setActiveTab }) => {
  return (
    <SidebarContainer>
      <SidebarButton 
        active={activeTab === 'terminal'}
        onClick={() => setActiveTab('terminal')}
      >
        <FiTerminal />
        <span>Terminal</span>
      </SidebarButton>
      <SidebarButton 
        active={activeTab === 'workflow'}
        onClick={() => setActiveTab('workflow')}
      >
        <FiLayers />
        <span>Workflows</span>
      </SidebarButton>
      <SidebarButton 
        active={activeTab === 'output'}
        onClick={() => setActiveTab('output')}
      >
        <FiActivity />
        <span>Analysis</span>
      </SidebarButton>
    </SidebarContainer>
  );
};

export default Sidebar;
