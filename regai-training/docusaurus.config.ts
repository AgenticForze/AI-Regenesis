import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'RegAITraining',
  tagline: 'AI Foundations to Advanced Agentic AI — for Finance, Healthcare & Telecom',
  favicon: 'img/favicon.ico',

  future: {
    v4: true,
  },

  markdown: {
    mermaid: true,
  },
  themes: ['@docusaurus/theme-mermaid'],

  // TODO: replace with the org's real GitHub Pages URL before first deploy
  url: 'https://regai-training.github.io',
  baseUrl: '/regai-training/',

  organizationName: 'regai-training',
  projectName: 'regai-training',

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'throw',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          path: 'docs',
          routeBasePath: 'docs',
          sidebarPath: './sidebars.ts',
          editUrl: 'https://github.com/regai-training/regai-training/tree/main/',
          showLastUpdateTime: true,
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    image: 'img/social-card.jpg',
    colorMode: {
      defaultMode: 'light',
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'RegAITraining',
      logo: {
        alt: 'RegAITraining — altitude gauge logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'phaseSidebar',
          position: 'left',
          label: 'Curriculum',
        },
        {
          to: '/docs/orientation/0-2-learning-paths-personas',
          label: 'Learning Paths',
          position: 'left',
        },
        {
          to: '/docs/orientation/0-3-ai-roles-in-the-market',
          label: 'AI Roles Map',
          position: 'left',
        },
        {to: '/roadmap', label: 'Roadmap', position: 'left'},
        {to: '/changelog', label: 'Changelog', position: 'left'},
        {to: '/about', label: 'About', position: 'right'},
        {
          href: 'https://github.com/regai-training/regai-training',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Start Here',
          items: [
            {label: 'Welcome & How to Use This KMS', to: '/docs/orientation/0-1-welcome'},
            {label: 'Learning Paths & Personas', to: '/docs/orientation/0-2-learning-paths-personas'},
            {label: 'AI Roles in the Market', to: '/docs/orientation/0-3-ai-roles-in-the-market'},
          ],
        },
        {
          title: 'Flagship Phases',
          items: [
            {label: 'Phase 8 — Agent Foundations', to: '/docs/agents-foundations'},
            {label: 'Phase 10 — Agentic Architectures', to: '/docs/agentic-architectures'},
            {label: 'Phase 16 — Domain Deep Dives', to: '/docs/domain-deep-dives'},
          ],
        },
        {
          title: 'Contribute',
          items: [
            {label: 'About This Site', to: '/about'},
            {label: 'Roadmap', to: '/roadmap'},
            {label: 'Changelog', to: '/changelog'},
            {label: 'Contribution Guide', to: '/docs/capstones-and-contributing'},
            {label: 'GitHub', href: 'https://github.com/regai-training/regai-training'},
          ],
        },
      ],
      copyright: `© ${new Date().getFullYear()} RegAITraining. Built with Docusaurus. Content licensed CC BY-SA 4.0.`,
    },
    prism: {
      theme: prismThemes.oneLight,
      darkTheme: prismThemes.oneDark,
      additionalLanguages: ['python', 'bash', 'json', 'yaml'],
    },
    mermaid: {
      theme: {light: 'neutral', dark: 'dark'},
    },
    docs: {
      sidebar: {
        hideable: true,
        autoCollapseCategories: true,
      },
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
