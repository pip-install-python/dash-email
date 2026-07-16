const path = require('path');

const packagejson = require('./package.json');

const dashLibraryName = packagejson.name.replace(/-/g, '_');

module.exports = function (env, argv) {
    const mode = (argv && argv.mode) || 'production';
    const entry = [path.join(__dirname, 'src/lib/index.js')];

    const output = {
        path: path.join(__dirname, dashLibraryName),
        filename: `${dashLibraryName}.min.js`,
        library: dashLibraryName,
        libraryTarget: 'window',
    };

    const externals = {
        react: 'React',
        'react-dom': 'ReactDOM',
        'plotly.js': 'Plotly',
        'prop-types': 'PropTypes',
    };

    return {
        mode,
        entry,
        output,
        externals,
        module: {
            rules: [
                {
                    test: /\.jsx?$/,
                    exclude: /node_modules/,
                    use: {
                        loader: 'babel-loader',
                    },
                },
                {
                    test: /\.css$/,
                    use: ['style-loader', 'css-loader'],
                },
            ],
        },
        resolve: {
            extensions: ['.js', '.jsx'],
        },
        devtool: mode === 'development' ? 'source-map' : false,
    };
};