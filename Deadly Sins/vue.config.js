const webpack = require('webpack');
const environment = require('./build/environment');
const isProd = process.env.NODE_ENV === "production";

module.exports = {
  publicPath: isProd ? "/vue-argon-dashboard/" : "",
  configureWebpack: {
    // Set up all the aliases we use in our app.
    plugins: [
      new webpack.DefinePlugin({
        'process.env.STAGE': JSON.stringify(environment.stage),
        'process.env.LOCAL_URL': JSON.stringify(environment.localUrl)
      })

    ]
  },
  pwa: {
    name: 'Deadly Sins',
    themeColor: '#172b4d',
    msTileColor: '#172b4d',
    appleMobileWebAppCapable: 'yes',
    appleMobileWebAppStatusBarStyle: '#172b4d'
  },
  css: {
    // Enable CSS source maps.
    sourceMap: process.env.NODE_ENV !== 'production'
  }
};
