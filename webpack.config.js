const path = require("path");

module.exports = {
    entry: "./accessflow/static/js/index.js",
    output: {
        filename: "accessflow.js",
        path: path.resolve(__dirname, "./accessflow/static/js")
    },
    mode: "development" // Use 'production' for minification
};