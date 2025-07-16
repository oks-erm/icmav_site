// tailwind.config.cjs

/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        './public/index.html',
        './src/**/*.{vue,js,ts,jsx,tsx}'
    ],
    theme: {
        extend: {},
    },
    plugins: [
        require('daisyui'),
        require('@tailwindcss/aspect-ratio'),
    ],
    daisyui: {
        themes: ['light', 'dark', 'cmyk'],
    },
  };