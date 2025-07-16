// tailwind.config.cjs
module.exports = {
    content: [
        './public/index.html',
        './src/**/*.{vue,js,ts,jsx,tsx}'
    ],
    theme: { extend: {} },
    plugins: [
        require('@tailwindcss/aspect-ratio'),
        require('daisyui'),
    ],
    daisyui: { themes: ['light', 'dark', 'cmyk'], defaultTheme: 'light' }
}
  