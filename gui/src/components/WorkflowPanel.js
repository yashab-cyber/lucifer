import React, { useState } from 'react';
import styled from 'styled-components';
import { FiPlay, FiPackage } from 'react-icons/fi';

const WorkflowContainer = styled.div`
  flex: 1;
  padding: 30px;
  overflow-y: auto;
`;

const WorkflowHeader = styled.div`
  margin-bottom: 30px;
`;

const WorkflowTitle = styled.h2`
  color: #ff4444;
  font-size: 28px;
  margin-bottom: 10px;
`;

const WorkflowDescription = styled.p`
  color: #888;
  font-size: 14px;
`;

const WorkflowGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 30px;
`;

const WorkflowCard = styled.div`
  background: #2d2d2d;
  border: 2px solid ${props => props.active ? '#ff4444' : '#333'};
  border-radius: 8px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.3s ease;

  &:hover {
    border-color: #ff4444;
    transform: translateY(-5px);
    box-shadow: 0 5px 20px rgba(255, 68, 68, 0.2);
  }
`;

const CardIcon = styled.div`
  font-size: 36px;
  margin-bottom: 15px;
  color: #ff4444;
`;

const CardTitle = styled.h3`
  color: #d4d4d4;
  margin-bottom: 10px;
  font-size: 18px;
`;

const CardDescription = styled.p`
  color: #888;
  font-size: 13px;
  line-height: 1.5;
  margin-bottom: 15px;
`;

const RunButton = styled.button`
  width: 100%;
  padding: 10px;
  background: #ff4444;
  border: none;
  color: white;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.3s ease;

  &:hover {
    background: #ff6666;
  }
`;

const TargetInput = styled.input`
  width: 100%;
  padding: 12px;
  background: #1e1e1e;
  border: 2px solid #333;
  color: #d4d4d4;
  border-radius: 6px;
  margin-bottom: 20px;
  font-size: 14px;

  &:focus {
    outline: none;
    border-color: #ff4444;
  }
`;

const workflows = [
  {
    id: 'recon',
    name: 'Reconnaissance',
    icon: '🔍',
    description: 'Comprehensive target reconnaissance and enumeration including port scanning, service detection, and DNS enumeration.'
  },
  {
    id: 'webapp',
    name: 'Web Application',
    icon: '🌐',
    description: 'Automated web vulnerability assessment including directory enumeration, nikto scanning, and SQL injection testing.'
  },
  {
    id: 'exploit',
    name: 'Exploitation',
    icon: '💥',
    description: 'Vulnerability exploitation workflow including Metasploit searches and exploit database queries.'
  },
  {
    id: 'privesc',
    name: 'Privilege Escalation',
    icon: '⬆️',
    description: 'Linux privilege escalation enumeration including SUID binaries, sudo permissions, and LinPEAS.'
  }
];

const WorkflowPanel = ({ workflow, onExecute }) => {
  const [target, setTarget] = useState('');
  const [selectedWorkflow, setSelectedWorkflow] = useState(workflow);

  const handleRunWorkflow = (workflowId) => {
    if (target) {
      onExecute(`workflow ${workflowId} ${target}`);
    } else {
      alert('Please enter a target');
    }
  };

  return (
    <WorkflowContainer>
      <WorkflowHeader>
        <WorkflowTitle>Pentesting Workflows</WorkflowTitle>
        <WorkflowDescription>
          Select and run automated penetration testing workflows
        </WorkflowDescription>
        <TargetInput
          type="text"
          placeholder="Enter target IP or domain..."
          value={target}
          onChange={(e) => setTarget(e.target.value)}
        />
      </WorkflowHeader>

      <WorkflowGrid>
        {workflows.map(wf => (
          <WorkflowCard 
            key={wf.id}
            active={selectedWorkflow === wf.id}
            onClick={() => setSelectedWorkflow(wf.id)}
          >
            <CardIcon>{wf.icon}</CardIcon>
            <CardTitle>{wf.name}</CardTitle>
            <CardDescription>{wf.description}</CardDescription>
            <RunButton onClick={() => handleRunWorkflow(wf.id)}>
              <FiPlay /> Run Workflow
            </RunButton>
          </WorkflowCard>
        ))}
      </WorkflowGrid>
    </WorkflowContainer>
  );
};

export default WorkflowPanel;
