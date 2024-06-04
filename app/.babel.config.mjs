export default {
    presets: [
        '@babel/preset-env',
        // https://babeljs.io/docs/babel-preset-env#targets
        // ['@babel/preset-env', { targets: { node: 'current' } }],
        // '@babel/preset-react',
        ['@babel/preset-react', { runtime: 'automatic' }],
        '@babel/preset-typescript',
    ],
    plugins: [
        ['module-resolver', { root: ['./src'] }],
        ['@babel/transform-runtime', { corejs: 3 }],
    ],
};
