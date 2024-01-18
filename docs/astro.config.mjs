import { defineConfig } from 'astro/config'
import starlight from '@astrojs/starlight'
import rehypeKatex from 'rehype-katex'
import remarkMath from 'remark-math'
import tailwind from '@astrojs/tailwind'

const BASE_PATH = 'lora-meshtastic'

// https://astro.build/config
export default defineConfig({
  base: BASE_PATH,
  site: `https://htwdd-rn.github.io/${BASE_PATH}/`,
  redirects: {
    '/': `/${BASE_PATH}/einfuehrung/projektbeschreibung/`,
  },
  trailingSlash: 'always',
  markdown: {
    remarkPlugins: [remarkMath],
    rehypePlugins: [rehypeKatex],
  },
  integrations: [
    starlight({
      locales: {
        root: {
          lang: 'de-DE',
          label: 'Deutsch',
        },
      },
      customCss: ['./src/tailwind.css', 'katex/dist/katex.min.css'],
      title: 'LoRa Meshtastic',
      editLink: {
        baseUrl: 'https://github.com/HTWDD-RN/lora-meshtastic/edit/main/docs/',
      },
      social: {
        github: 'https://github.com/HTWDD-RN/lora-meshtastic',
      },
      lastUpdated: true,
      sidebar: [
        {
          label: 'Einführung',
          autogenerate: {
            directory: 'einfuehrung',
          },
        },
        {
          label: 'Anwendung',
          autogenerate: {
            directory: 'anwendung',
          },
        },
        {
          label: 'FAQ',
          autogenerate: {
            directory: 'faq',
          },
        },
        {
          label: 'Ergebnisse',
          autogenerate: {
            directory: 'ergebnisse',
          },
        },
      ],
    }),
    tailwind({
      applyBaseStyles: false,
    }),
  ],
})
