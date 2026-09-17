/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        ar: ["var(--font-ar)", "sans-serif"],
        en: ["var(--font-en)", "sans-serif"],
      },
    },
  },
  plugins: [],
};