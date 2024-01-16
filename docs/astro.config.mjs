import { defineConfig } from 'astro/config'
import starlight from '@astrojs/starlight'
const BASE_PATH = 'lora-meshtastic'

// https://astro.build/config
export default defineConfig({
  base: BASE_PATH,
  site: `https://htwdd-rn.github.io/${BASE_PATH}/`,
  redirects: {
    '/': `/${BASE_PATH}/einfuehrung/projektbeschreibung/`,
  },
  trailingSlash: 'always',
  integrations: [
    starlight({
      locales: {
        root: {
          lang: 'de-DE',
          label: 'Deutsch',
        },
      },
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
  ],
})
