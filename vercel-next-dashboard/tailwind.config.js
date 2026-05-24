/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/**/*.{js,ts,jsx,tsx}", "./components/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        graphite: "#0f1318",
        steel: "#171d24",
        cyan: "#62c5d7",
        amber: "#f2b84b",
        alert: "#e45d5d",
        muted: "#8d98a7",
      },
    },
  },
  plugins: [],
};
