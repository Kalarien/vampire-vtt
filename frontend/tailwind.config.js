/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Vampire Gothic Theme
        blood: {
          50: '#fef2f2',
          100: '#fee2e2',
          200: '#fecaca',
          300: '#fca5a5',
          400: '#f87171',
          500: '#dc2626',
          600: '#b91c1c',
          700: '#991b1b',
          800: '#7f1d1d',
          900: '#450a0a',
        },
        midnight: {
          50: '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          400: '#94a3b8',
          500: '#64748b',
          600: '#475569',
          700: '#334155',
          800: '#1e293b',
          900: '#0f172a',
          950: '#020617',
        },
        bone: {
          50: '#fefdfb',
          100: '#fdf8f0',
          200: '#f9eedc',
          300: '#f3dfc0',
          400: '#e8c898',
          500: '#d4a574',
          600: '#b8845c',
          700: '#9a6a4a',
          800: '#7d5540',
          900: '#664738',
        },
      },
      fontFamily: {
        gothic: ['Cinzel', 'serif'],
        body: ['Crimson Text', 'Georgia', 'serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'parchment': "url('/textures/parchment.png')",
      },
      boxShadow: {
        'blood': '0 0 15px rgba(220, 38, 38, 0.3)',
        'blood-lg': '0 0 30px rgba(220, 38, 38, 0.4)',
        'inner-blood': 'inset 0 0 15px rgba(220, 38, 38, 0.2)',
      },
      animation: {
        'pulse-blood': 'pulse-blood 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'drip': 'drip 3s ease-in-out infinite',
        'flicker': 'flicker 4s linear infinite',
      },
      keyframes: {
        'pulse-blood': {
          '0%, 100%': { boxShadow: '0 0 15px rgba(220, 38, 38, 0.3)' },
          '50%': { boxShadow: '0 0 25px rgba(220, 38, 38, 0.6)' },
        },
        'drip': {
          '0%': { transform: 'translateY(-100%)', opacity: '0' },
          '20%': { opacity: '1' },
          '100%': { transform: 'translateY(100%)', opacity: '0' },
        },
        'flicker': {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.8' },
          '75%': { opacity: '0.9' },
        },
      },
    },
  },
  plugins: [],
}
