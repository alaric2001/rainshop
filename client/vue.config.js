// vue.config.js
// publicPath diisi dari env:
//   - build lokal (webapp/)  : '' (root)
//   - deploy GitHub Pages    : '/rainshop/'
module.exports = {
    publicPath: process.env.VUE_APP_PUBLIC_PATH || '',
    outputDir: 'dist'
}
