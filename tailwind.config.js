/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./kalokohan/**/templates/**/*.html"],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
};
