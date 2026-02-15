/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {
          light: '#3b82f6', // blue-500
          dark: '#2563eb', // blue-600
        },
        background: {
          light: '#f3f4f6', // gray-100
          dark: '#1f2937', // gray-800
        },
        surface: {
            light: '#ffffff',
            dark: '#111827', // gray-900
        }
      }
    },
  },
  plugins: [],
}
