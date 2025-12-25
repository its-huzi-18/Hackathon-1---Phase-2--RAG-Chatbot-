import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'Advanced Robotics & AI',
  tagline: 'Empowering the next generation of AI and Robotics innovators',
  favicon: 'img/favicon-new.svg',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },

  // Set the production url of your site here
  // For Vercel deployments, you can keep this generic; it is mainly used for sitemaps.
  url: 'https://physical-ai-humanoid-robotics.vercel.app',
  // On Vercel (and most hosts serving at domain root), use baseUrl '/'
  baseUrl: '/',

  // GitHub pages deployment config. Not needed for Vercel, but harmless.
  organizationName: 'Panaversity', // Usually your GitHub org/user name.
  projectName: 'Physical-AI-And-Humanoid-Robotics', // Usually your repo name.

  onBrokenLinks: 'throw',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  // Custom fields
  customFields: {
    ragChatbotApiUrl: process.env.RAG_CHATBOT_API_URL || 'http://localhost:8000',
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
        },
        blog: {
          showReadingTime: true,
          feedOptions: {
            type: ['rss', 'atom'],
            xslt: true,
          },
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
          // Useful options to enforce blogging best practices
          onInlineTags: 'warn',
          onInlineAuthors: 'warn',
          onUntruncatedBlogPosts: 'warn',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  plugins: [
    // Plugin to inject the chatbot script with proper API URL
    function injectChatbotPlugin() {
      return {
        name: 'inject-chatbot',
        injectHtmlTags() {
          return {
            postBodyTags: [
              // Set the API URL as a script to make it available globally
              {
                tagName: 'script',
                innerHTML: `
                  window.RAG_CHATBOT_API_URL = "${
                    process.env.RAG_CHATBOT_API_URL || 'http://localhost:8000'
                  }";
                `,
              },
              // Load the chatbot UI after the API URL is set
              {
                tagName: 'script',
                attributes: {
                  src: '/rag-chatbot.js',
                  async: true,
                },
              }
            ],
          };
        },
      };
    },
  ],

  themeConfig: {
    // Replace with your project's social card
    image: 'img/docusaurus-social-card.jpg',
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'Advanced Robotics & AI',
      logo: {
        alt: 'Advanced Robotics & AI Logo',
        src: 'img/logo-professional.svg',
      },
      items: [
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Company',
          items: [
            {
              label: 'About Us',
              to: '/about',
            },
            {
              label: 'Contact',
              to: '/contact',
            },
          ],
        },
        {
          title: 'Legal',
          items: [
            {
              label: 'Privacy Policy',
              to: '/privacy',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Advanced Robotics & AI. All rights reserved.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
