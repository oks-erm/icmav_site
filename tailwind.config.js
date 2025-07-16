// tailwind.config.js
module.exports = {
    content: [
        './public/index.html',
        './src/**/*.{vue,js,ts,jsx,tsx}',
    ],
    theme: { extend: {} },
    plugins: [require('daisyui')],
    daisyui: { themes: ['light', 'dark', 'cmyk'], defaultTheme: 'light' }
}
  