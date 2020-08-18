import React, {Component} from 'react';
import styled from '@emotion/styled';
import {css, keyframes} from '@emotion/core';
import {Location} from '@reach/router';
import TippyLogo from '../images/logo.svg';
import {MEDIA, Container, Flex, ExternalLink} from './Framework';
import GitHub from 'react-feather/dist/icons/github';
import Menu from 'react-feather/dist/icons/menu';
import TextGradient from './TextGradient';
import {version} from '../../../package.json';
import {Link} from 'gatsby';
import {getVersionFromPath, CURRENT_MAJOR} from '../utils';
import bubbles from '../images/bubbles.svg';

// Firefox needs `rotate()` for it to be smooth...
const hover = keyframes`
  from {
    transform: translate3d(0, 4px, 0) rotate(0);
  }

  to {
    transform: translate3d(0, 10px, 0) rotate(0.01deg);
  }
`;

const HeaderRoot = styled.header`
  position: relative;
  background-image: radial-gradient(
    circle at 0% 20%,
    #a09eff,
    #4884f0,
    #b3e0fa
  );
  background-repeat: no-repeat;
  background-size: cover;
  padding: 25px 0;
  text-align: center;
  margin-bottom: 50px;
  color: white;

  &::before {
    content: '';
    position: absolute;
    top: -50px;
    display: block;
    background-image: url(${bubbles});
    background-size: cover;
    width: 100%;
    height: calc(100vh + 50px);
  }
`;

const Logo = styled.img`
  display: block;
  height: 72px;
  margin: 0 auto 10px;
  animation: ${hover} 2s ease-in-out infinite alternate;
`;

const Title = styled.h1`
  display: inline-block;
  font-size: 56px;
  font-weight: 400;
  margin-top: 0;
  margin-bottom: 25px;
`;

const ButtonLink = styled(ExternalLink)`
  background: rgba(255, 255, 255, 0.15);
  padding: 12px 24px;
  border-radius: 4px;
  transition: all 0.25s;
  color: #ffffff;
  margin: 0 8px 8px;
  font-weight: bold;
  font-size: 18px;
  font-weight: 500;
  will-change: opacity;

  &:hover {
    background: white;
    border-bottom-color: white;
    box-shadow: 0 8px 16px -2px rgba(0, 32, 128, 0.25);
    text-decoration: none;
  }
`;

export const MenuButton = styled.button`
  position: absolute;
  top: -10px;
  left: 25px;
  color: rgb(36, 58, 89);
  font-weight: bold;
  border: none;
  background: none;
  text-transform: uppercase;
  border-radius: 4px;
  padding: 0;

  ${MEDIA.lg} {
    display: none;
  }
`;

const Version = styled.a`
  display: inline-block;
  background: rgb(255, 255, 255, 0.95);
  color: #7761d1;
  font-weight: bold;
  margin: 16px 0;
  padding: 6px 12px;
  border-radius: 16px;
  font-size: 14px;

  ${MEDIA.md} {
    margin: 16px 0;
  }
`;

const OldVersionWarning = styled.div`
  position: relative;
  background: #fff5c5;
  color: #333;
  z-index: 2;
  text-align: center;
  padding: 10px 0;
  font-size: 16px;
  font-weight: bold;
`;

const svgStyles = css`
  margin: -16px 0 -32px;

  ${MEDIA.md} {
    margin: -10% 0 -32px;
    margin-left: -250px;
  }

  @media (min-width: 1700px) {
    margin: -9% 0 -32px;
  }
`;

const iconStyles = {
  verticalAlign: '-7px',
  marginRight: '8px',
};

const githubStyles = {
  ...iconStyles,
  width: '24px',
  height: '24px',
  color: '#333',
};

const menuStyles = {
  width: '40px',
  height: '40px',
};

class Header extends Component {
  render() {
    const {isNavOpen, openNav} = this.props;

    return (
      <>
        <Location>
          {({location}) =>
            getVersionFromPath(location.pathname) !== CURRENT_MAJOR && (
              <OldVersionWarning>
                <Container>
                  <span role="img" aria-label="alert">
                    ❗
                  </span>{' '}
                  You're viewing the previous major version's docs.{' '}
                  <Link to="/">Click here</Link> to view the latest version.
                </Container>
              </OldVersionWarning>
            )
          }
        </Location>

        <HeaderRoot>
          <Container>
            <Logo src={TippyLogo} draggable="false" alt="Tippy Logo" />
            <Title>
              <TextGradient>Tippy.js</TextGradient>
            </Title>
            <Flex justify="center">
              <ButtonLink href="https://github.com/atomiks/tippyjs">
                <GitHub style={githubStyles} />
                View on GitHub
              </ButtonLink>
            </Flex>
            <Version href="https://github.com/atomiks/tippyjs/releases">
              Currently v{version}
            </Version>
            <MenuButton
              aria-label="Menu"
              aria-expanded={isNavOpen ? 'true' : 'false'}
              onClick={openNav}
            >
              <Menu style={menuStyles} />
            </MenuButton>
          </Container>
          <svg
            css={svgStyles}
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 1920 240"
            fill="white"
          >
            <g>
              <path d="M1920,144.5l0,95.5l-1920,0l0,-65.5c196,-36 452.146,-15.726 657.5,8.5c229.698,27.098 870,57 1262.5,-38.5Z" />
            </g>
          </svg>
        </HeaderRoot>
      </>
    );
  }
}

export default Header;
