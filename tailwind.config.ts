import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        dark: {
          900: '#0a0a0f',
          800: '#111118',
          700: '#1a1a24',
          600: '#252532',
        },
        accent: {
          primary: '#6366f1',
          secondary: '#a855f7',
          success: '#22c55e',
          warning: '#f59e0b',
        },
      },
    },
  },
  plugins: [],
}
export default config
