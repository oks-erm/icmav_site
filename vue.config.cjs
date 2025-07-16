// vue.config.cjs
const path = require('path')

module.exports = {
    publicPath: '/',

    css: {
        loaderOptions: {
            postcss: {
                postcssOptions: {
                    plugins: [
                        require('@tailwindcss/postcss')(), 
                        require('autoprefixer')(),  
                    ]
                }
            }
        }
    }
}
