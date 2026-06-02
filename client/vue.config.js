// vue.config.js
module.exports = {
    // GitHub Pages: /rainshop/  |  Lokal: '' (root)
    publicPath: process.env.NODE_ENV === 'production' ? '/rainshop/' : '',
    outputDir: 'dist'
}
