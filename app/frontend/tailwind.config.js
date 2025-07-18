/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#4F46E5', // Indigo-600
          hover: '#4338CA',   // Indigo-700
        },
        secondary: {
          DEFAULT: '#6366f1', // Indigo-500
          hover: '#4f46e5',   // Indigo-600
        },
      },
    },
  },
  plugins: [],
}