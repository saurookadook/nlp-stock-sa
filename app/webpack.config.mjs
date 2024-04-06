// Generated using webpack-cli https://github.com/webpack/webpack-cli

// const path = require('path');
// const HtmlWebpackPlugin = require('html-webpack-plugin');
// const WorkboxWebpackPlugin = require('workbox-webpack-plugin');

import path from 'path';
import HtmlWebpackPlugin from 'html-webpack-plugin';
import WebpackAssetsManifest from 'webpack-assets-manifest';
import WorkboxWebpackPlugin from 'workbox-webpack-plugin';

// const isProduction = process.env.NODE_ENV == 'production';

const __dirname = path.resolve();

const buildConfig = (env, argv) => ({
    context: __dirname,
    devtool: 'inline-source-map',
    entry: {
        home: [
            '@babel/polyfill',
            path.resolve(__dirname, 'src/client/home/entry.ts')
        ],
        login: [
            '@babel/polyfill',
            path.resolve(__dirname, 'src/client/login/entry.ts')
        ],
    },
    output: {
        // path: path.resolve(__dirname, 'dist'),
        // filename: 'bundle.js',
        path: path.resolve(__dirname, 'public'),
        filename: '[name]-[chunkhash].min.js',
    },
    devServer: {
        open: true,
        host: 'localhost',
        static: {
            directory: path.resolve(__dirname, 'dist'),
        },
    },
    module: {
        rules: [
            // NOTE: maybe need different rules for client and server?
            {
                test: /\.(ts|tsx)$/i,
                exclude: ['/node_modules/'],
                loader: 'ts-loader',
            },
            {
                test: /\.(eot|svg|ttf|woff|woff2|png|jpg|gif)$/i,
                type: 'asset',
            },

            // Add your rules for custom modules here
            // Learn more about loaders from https://webpack.js.org/loaders/
        ],
    },
    // optimization: {
    //     splitChunks: {
    //         commonVendors: {
    //             test: /^.*node_modules[\/\\](?!).*$/,
    //             name: 'nlpssaVendor',
    //             chunks: 'initial'
    //         },
    //         commons: {
    //             test: /[\/\\]src\/common[\/\\]/,
    //             name: 'nlpssaCommon',
    //             chunks: 'initial',
    //             enforce: true,
    //         }
    //     },
    //     minimizer: argv.mode === 'production' ? [new TerserPlugin()] : []
    // },
    // Add your plugins here
    // Learn more about plugins from https://webpack.js.org/configuration/plugins/
    plugins: getPlugins(argv.mode),
    resolve: {
        alias: {
            common: path.resolve(__dirname, 'src/common'),
        },
        extensions: ['.js', '.jsx', '.ts', '.tsx'],
        modules: [path.resolve(__dirname, 'src'), 'node_modules'],
    },
});

function getPlugins(mode) {
    const commonPlugins = [
        new HtmlWebpackPlugin({
            template: path.resolve(__dirname, 'index.html'),
        }),
        new WebpackAssetsManifest({})
    ]

    return mode === 'production'
        ? [
            ...commonPlugins,
            new WorkboxWebpackPlugin.GenerateSW()
        ] : [
            ...commonPlugins
        ]
}

export default (env, argv) => {
    const config = buildConfig(env, argv);

    // if (isProduction) {
    //     config.mode = 'production';
    //     config.plugins.push(new WorkboxWebpackPlugin.GenerateSW());
    // } else {
    //     config.mode = 'development';
    // }

    return config;
};