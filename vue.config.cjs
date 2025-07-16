// vue.config.cjs
const path = require('path')

module.exports = {

    chainWebpack: config => {
        config
            .plugin('html')
            .tap(args => {
                args[0].title = 'ICMAV – Propósito para a vida'
                return args
            })
      },
      
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
