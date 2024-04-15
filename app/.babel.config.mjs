export default {
    presets: ["@babel/preset-env", "@babel/preset-react"],
    plugins: [
        ["module-resolver", { root: ["./src"] }],
        ["@babel/transform-runtime", { corejs: 3 }]
    ]
}
