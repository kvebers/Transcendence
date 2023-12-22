/** @type {import('tailwindcss').Config} */
module.exports = {
  mode: "jit",
  purge: ["./src/**/*.{js,jsx,ts,tsx}", "./public/index.html"],
  content: ["./src/**/*.{js,jsx,ts,tsx}", "./public/index.html"],
  theme: {
    extend: {
      fontSize: {
        "1.5xl": "1.275rem",
      },
      fontFamily: {
        nosifer: ["Nosifer", "cursive"],
      },
    },
  },
  plugins: [],
  corePlugins: {
    preflight: true,
    container: true,
  },
};