import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./lib/**/*.{js,ts,jsx,tsx,mdx}"
  ],
  theme: {
    extend: {
      colors: {
        cocoa: "#3f2a23",
        coral: "#f97373",
        melon: "#fb923c",
        mint: "#5eead4",
        plum: "#8b5cf6"
      },
      boxShadow: {
        soft: "0 18px 50px rgba(127, 73, 52, 0.14)"
      }
    }
  },
  plugins: []
};

export default config;
