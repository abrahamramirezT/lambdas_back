/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}', // Ensure Tailwind scans all necessary files
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
