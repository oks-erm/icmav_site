// vue.config.js
/** @type {import('@vue/cli-service').ProjectOptions} */
module.exports = {
    // any Vue CLI options you need, e.g.:
    publicPath: '/',
    css: {
        loaderOptions: {
            postcss: {
                // pass our PostCSS config file explicitly
                postcssOptions: {
                    config: './postcss.config.js'
                }
            }
        }
      }
}
  