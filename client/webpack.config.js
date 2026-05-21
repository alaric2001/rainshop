
module.exports = {
    optimization: {
        splitChunks: {
            chunks: 'all'
        }
    },
    output: {
        filename: '[name].bundle.js',
        chunkFilename: '[name].bundle.js',
        path: path.resolve(__dirname, 'dist')
    }    
};
