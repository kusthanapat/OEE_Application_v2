/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html", // สำคัญ!
    "./static/**/*.{js,css}", // ถ้ามี JS ที่ใช้ Tailwind classes
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
