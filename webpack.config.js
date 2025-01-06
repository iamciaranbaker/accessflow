const path = require("path");

module.exports = {
    entry: "./access_flow/static/js/index.js",
    output: {
        filename: "accessflow.js",
        path: path.resolve(__dirname, "./access_flow/static/js")
    },
    mode: "development" // Use 'production' for minification
};