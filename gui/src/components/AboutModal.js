import React from 'react';
import styled from 'styled-components';
import { FiX, FiGithub, FiLinkedin, FiInstagram, FiMail } from 'react-icons/fi';

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
  width: 600px;
  max-width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 40px rgba(255, 68, 68, 0.3);
`;

const Header = styled.div`
  padding: 20px 30px;
  border-bottom: 1px solid #444;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(135deg, #2d0a0e 0%, #2d2d2d 100%);
`;

const Title = styled.h2`
  margin: 0;
  color: #ff4444;
  font-size: 24px;
`;

const CloseButton = styled.button`
  background: transparent;
  border: none;
  color: #888;
  cursor: pointer;
  font-size: 24px;
  padding: 0;
  transition: color 0.3s ease;

  &:hover {
    color: #ff4444;
  }
`;

const Content = styled.div`
  padding: 30px;
`;

const LogoSection = styled.div`
  text-align: center;
  margin-bottom: 30px;
`;

const Logo = styled.img`
  width: 100px;
  height: 100px;
  filter: drop-shadow(0 0 20px rgba(255, 68, 68, 0.5));
  margin-bottom: 15px;
`;

const AppName = styled.h1`
  font-size: 36px;
  background: linear-gradient(135deg, #ff4444 0%, #ff8844 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin: 0;
  letter-spacing: 3px;
`;

const Version = styled.div`
  color: #888;
  font-size: 14px;
  margin-top: 5px;
`;

const Description = styled.p`
  color: #d4d4d4;
  text-align: center;
  margin: 20px 0;
  line-height: 1.6;
`;

const Section = styled.div`
  margin: 25px 0;
`;

const SectionTitle = styled.h3`
  color: #ff4444;
  font-size: 18px;
  margin-bottom: 15px;
  border-bottom: 2px solid #ff4444;
  padding-bottom: 8px;
`;

const AuthorInfo = styled.div`
  text-align: center;
  padding: 20px;
  background: #1e1e1e;
  border-radius: 8px;
  margin: 20px 0;
`;

const AuthorName = styled.div`
  font-size: 20px;
  color: #4ec9b0;
  font-weight: bold;
  margin-bottom: 10px;
`;

const SocialLinks = styled.div`
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 15px;
`;

const SocialLink = styled.a`
  color: #888;
  font-size: 24px;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 5px;

  &:hover {
    color: #ff4444;
    transform: translateY(-3px);
  }
`;

const InfoList = styled.ul`
  list-style: none;
  padding: 0;
  
  li {
    padding: 8px 0;
    color: #d4d4d4;
    
    strong {
      color: #4ec9b0;
      margin-right: 10px;
    }
  }
`;

const DonateButton = styled.a`
  display: block;
  text-align: center;
  background: linear-gradient(135deg, #ff4444 0%, #ff8844 100%);
  color: white;
  padding: 12px 24px;
  border-radius: 8px;
  text-decoration: none;
  font-weight: bold;
  margin-top: 20px;
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(255, 68, 68, 0.4);
  }
`;

const AboutModal = ({ onClose }) => {
  return (
    <Overlay onClick={onClose}>
      <Modal onClick={(e) => e.stopPropagation()}>
        <Header>
          <Title>About Lucifer</Title>
          <CloseButton onClick={onClose}>
            <FiX />
          </CloseButton>
        </Header>
        <Content>
          <LogoSection>
            <Logo src="/icon.png" alt="Lucifer" />
            <AppName>LUCIFER</AppName>
            <Version>Version 1.0.0</Version>
          </LogoSection>

          <Description>
            AI-Powered Cybersecurity Automation Assistant for penetration testing
            and bug bounty hunting. Combines terminal capture, computer vision,
            and artificial intelligence for intelligent security testing.
          </Description>

          <Section>
            <SectionTitle>🔥 Created By</SectionTitle>
            <AuthorInfo>
              <AuthorName>Yashab Alam</AuthorName>
              <div style={{ color: '#888', fontSize: '14px' }}>
                Security Researcher & Developer
              </div>
              <SocialLinks>
                <SocialLink 
                  href="https://www.linkedin.com/in/yashab-alam" 
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <FiLinkedin /> LinkedIn
                </SocialLink>
                <SocialLink 
                  href="https://www.instagram.com/yashab.alam" 
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <FiInstagram /> Instagram
                </SocialLink>
                <SocialLink 
                  href="mailto:yashabalam9@gmail.com"
                >
                  <FiMail /> Email
                </SocialLink>
              </SocialLinks>
            </AuthorInfo>
          </Section>

          <Section>
            <SectionTitle>📋 Features</SectionTitle>
            <InfoList>
              <li><strong>•</strong> Real-time terminal capture & monitoring</li>
              <li><strong>•</strong> Computer vision & screenshot analysis</li>
              <li><strong>•</strong> AI-powered suggestions (Claude, GPT-4, Ollama)</li>
              <li><strong>•</strong> Automated pentesting workflows</li>
              <li><strong>•</strong> Professional report generation</li>
              <li><strong>•</strong> Screen recording capabilities</li>
            </InfoList>
          </Section>

          <Section>
            <SectionTitle>📜 License & Legal</SectionTitle>
            <InfoList>
              <li><strong>License:</strong> MIT License</li>
              <li><strong>⚠ Important:</strong> For authorized testing only</li>
              <li><strong>Repository:</strong> github.com/yashab-cyber/lucifer</li>
            </InfoList>
          </Section>

          <DonateButton href="mailto:yashabalam9@gmail.com?subject=Lucifer Donation">
            ❤️ Support This Project
          </DonateButton>
        </Content>
      </Modal>
    </Overlay>
  );
};

export default AboutModal;
