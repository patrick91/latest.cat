module.exports = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: "class",
  theme: {
    fontFamily: {
      sans: "Neue Montreal, sans-serif",
      heading: "PP Woodland, serif",
    },
    extend: {
      colors: {
        dark: "#121212",
        green: "#B0FFB8",
        "spring-bud": "#a6fd00",
        pink: "#FFE6E6",
        cosmos: "#ffcbcc",
        gold: "#ffd200",
        yellow: "#F9EF05",
        corn: "#ffee87",
        mint: "#f8ffc2",
        blue: "#426af8",
        turquoise: "#00fee2",
        "dark-purple": "#341247",
        "dark-gray": "#2A2929",
      },
      boxShadow: {
        "drop-sm": "-1px 1px 0px #000000",
        drop: "-3px 6px 0px #000000",
      },
    },
  },
  plugins: [],
};
