// vue.config.cjs
const path = require('path')

module.exports = {
    publicPath: process.env.NODE_ENV === 'production'
        ? '/icmav_site/'
        : '/',

    css: {
        loaderOptions: {
            postcss: {
                postcssOptions: {
                    plugins: [
                        require('@tailwindcss/postcss')(),  // Tailwind v4 plugin
                        require('autoprefixer')(),          // vendor prefixes
                    ]
                }
            }
        }
    }
}
