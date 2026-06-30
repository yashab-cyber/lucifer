import React from 'react';
import styled from 'styled-components';
import { FiX, FiHeart, FiMail, FiLinkedin, FiInstagram, FiGithub } from 'react-icons/fi';

const ModalOverlay = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.85);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(5px);
`;

const ModalContent = styled.div`
  background: linear-gradient(135deg, #1e1e1e 0%, #2d0a0e 100%);
  border: 2px solid #ff4499;
  border-radius: 12px;
  padding: 30px;
  max-width: 600px;
  width: 90%;
  max-height: 85vh;
  overflow-y: auto;
  box-shadow: 0 8px 32px rgba(255, 68, 153, 0.3);
  position: relative;

  &::-webkit-scrollbar {
    width: 8px;
  }

  &::-webkit-scrollbar-track {
    background: #1e1e1e;
    border-radius: 4px;
  }

  &::-webkit-scrollbar-thumb {
    background: #ff4499;
    border-radius: 4px;
  }
`;

const CloseButton = styled.button`
  position: absolute;
  top: 15px;
  right: 15px;
  background: transparent;
  border: none;
  color: #888;
  cursor: pointer;
  font-size: 24px;
  padding: 5px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;

  &:hover {
    color: #ff4499;
    transform: rotate(90deg);
  }
`;

const Title = styled.h2`
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 28px;
  color: #ff4499;
  margin: 0 0 10px 0;
`;

const Subtitle = styled.p`
  color: #888;
  margin: 0 0 25px 0;
  font-size: 14px;
`;

const Section = styled.div`
  margin-bottom: 25px;
`;

const SectionTitle = styled.h3`
  color: #ff6666;
  font-size: 18px;
  margin: 0 0 15px 0;
  display: flex;
  align-items: center;
  gap: 8px;
`;

const CreatorCard = styled.div`
  background: rgba(255, 68, 153, 0.1);
  border: 1px solid #ff4499;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 25px;
  text-align: center;
`;

const CreatorName = styled.h3`
  font-size: 24px;
  color: #ff4499;
  margin: 0 0 10px 0;
`;

const CreatorTitle = styled.p`
  color: #aaa;
  margin: 0 0 15px 0;
  font-size: 14px;
`;

const SocialLinks = styled.div`
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-top: 15px;
`;

const SocialLink = styled.a`
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 15px;
  background: rgba(255, 68, 153, 0.2);
  border: 1px solid #ff4499;
  border-radius: 6px;
  color: #ff4499;
  text-decoration: none;
  font-size: 13px;
  transition: all 0.3s ease;

  &:hover {
    background: rgba(255, 68, 153, 0.3);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(255, 68, 153, 0.4);
  }
`;

const DonationOption = styled.div`
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid #444;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 12px;
  transition: all 0.3s ease;

  &:hover {
    border-color: #ff4499;
    background: rgba(255, 68, 153, 0.1);
  }
`;

const OptionTitle = styled.div`
  font-weight: 600;
  color: #ff6666;
  margin-bottom: 5px;
  font-size: 15px;
`;

const OptionValue = styled.div`
  color: #aaa;
  font-size: 13px;
  font-family: 'Courier New', monospace;
  word-break: break-all;
`;

const InfoText = styled.p`
  color: #999;
  font-size: 14px;
  line-height: 1.6;
  margin: 10px 0;
`;

const HighlightBox = styled.div`
  background: rgba(255, 68, 68, 0.1);
  border-left: 4px solid #ff4444;
  padding: 15px;
  margin: 20px 0;
  border-radius: 4px;
`;

const HighlightText = styled.p`
  color: #ddd;
  font-size: 14px;
  margin: 0;
  line-height: 1.6;
`;

const DonateModal = ({ onClose }) => {
  return (
    <ModalOverlay onClick={onClose}>
      <ModalContent onClick={(e) => e.stopPropagation()}>
        <CloseButton onClick={onClose}>
          <FiX />
        </CloseButton>

        <Title>
          <FiHeart /> Support Lucifer Development
        </Title>
        <Subtitle>Help keep this project alive and growing</Subtitle>

        <CreatorCard>
          <CreatorName>Yashab Alam</CreatorName>
          <CreatorTitle>Cybersecurity Professional & Creator of Lucifer</CreatorTitle>
          
          <SocialLinks>
            <SocialLink href="https://www.linkedin.com/in/yashab-alam" target="_blank" rel="noopener noreferrer">
              <FiLinkedin /> LinkedIn
            </SocialLink>
            <SocialLink href="https://www.instagram.com/yashabcyber" target="_blank" rel="noopener noreferrer">
              <FiInstagram /> Instagram
            </SocialLink>
            <SocialLink href="https://github.com/yashab-cyber" target="_blank" rel="noopener noreferrer">
              <FiGithub /> GitHub
            </SocialLink>
          </SocialLinks>
        </CreatorCard>

        <HighlightBox>
          <HighlightText>
            <strong>Thank you for using Lucifer!</strong> Your support helps me maintain and improve this project,
            add new features, fix bugs, and provide better documentation. Every contribution, no matter
            how small, is deeply appreciated! ❤️
          </HighlightText>
        </HighlightBox>

        <Section>
          <SectionTitle>💰 Donation Methods</SectionTitle>
          
          <DonationOption>
            <OptionTitle>� GitHub Sponsors</OptionTitle>
            <OptionValue>github.com/sponsors/yashab-cyber</OptionValue>
          </DonationOption>

          <DonationOption>
            <OptionTitle>₿ Bitcoin (BTC)</OptionTitle>
            <OptionValue>Contact for address: yashabalam9@gmail.com / yashabalam707@gmail.com</OptionValue>
          </DonationOption>

          <DonationOption>
            <OptionTitle>⟠ Ethereum (ETH)</OptionTitle>
            <OptionValue>Contact for address: yashabalam9@gmail.com / yashabalam707@gmail.com</OptionValue>
          </DonationOption>

          <DonationOption>
            <OptionTitle>💵 USDT (Tether)</OptionTitle>
            <OptionValue>TRC20/ERC20 - Contact: yashabalam9@gmail.com / yashabalam707@gmail.com</OptionValue>
          </DonationOption>

          <DonationOption>
            <OptionTitle>🪙 Other Cryptocurrencies</OptionTitle>
            <OptionValue>Email yashabalam9@gmail.com / yashabalam707@gmail.com for addresses</OptionValue>
          </DonationOption>
        </Section>

        <Section>
          <SectionTitle>💝 What Your Support Helps With</SectionTitle>
          <InfoText>
            • <strong>Maintenance:</strong> Bug fixes, security updates, and compatibility improvements<br/>
            • <strong>New Features:</strong> AI model improvements, new workflows, and integrations<br/>
            • <strong>Documentation:</strong> Better guides, tutorials, and examples<br/>
            • <strong>Community:</strong> Support and help for users<br/>
            • <strong>Infrastructure:</strong> Hosting, testing, and development costs
          </InfoText>
        </Section>

        <Section>
          <SectionTitle>
            <FiMail /> Contact
          </SectionTitle>
          <InfoText>
            For sponsorship inquiries, custom features, or questions:<br/>
            <strong style={{ color: '#ff4499' }}>yashabalam9@gmail.com / yashabalam707@gmail.com</strong>
          </InfoText>
        </Section>

        <HighlightBox>
          <HighlightText style={{ textAlign: 'center' }}>
            <strong>Open Source, Free Forever</strong><br/>
            Lucifer will always be free and open source. Your donations help ensure I can
            continue dedicating time to this project. Thank you for your generosity! 🙏
          </HighlightText>
        </HighlightBox>
      </ModalContent>
    </ModalOverlay>
  );
};

export default DonateModal;
