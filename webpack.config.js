const path = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const TerserPlugin = require("terser-webpack-plugin");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");

module.exports = [
  // Configuration for regular files
  {
    entry: "./frontend/index.js",
    output: {
      path: path.resolve(__dirname, "./accessflow/static/js"),
      filename: "accessflow.js", // Regular JavaScript file
    },
    mode: "development", // Development mode for non-minified files
    module: {
      rules: [
        {
          test: /\.js$/,
          exclude: /node_modules/,
          use: "babel-loader",
        },
        {
          test: /\.css$/,
          use: [MiniCssExtractPlugin.loader, "css-loader"],
        },
      ],
    },
    plugins: [
      new MiniCssExtractPlugin({
        filename: "../css/accessflow.css", // Regular CSS file
      }),
    ],
  },
  // Configuration for minified files
  {
    entry: "./frontend/index.js",
    output: {
      path: path.resolve(__dirname, "./accessflow/static/js"),
      filename: "accessflow.min.js", // Minified JavaScript file
    },
    mode: "production", // Production mode for minification
    module: {
      rules: [
        {
          test: /\.js$/,
          exclude: /node_modules/,
          use: "babel-loader",
        },
        {
          test: /\.css$/,
          use: [MiniCssExtractPlugin.loader, "css-loader"],
        },
      ],
    },
    optimization: {
      minimize: true, // Enable minimization
      minimizer: [
        new TerserPlugin(), // Minify JavaScript
        new CssMinimizerPlugin(), // Minify CSS
      ],
    },
    plugins: [
      new MiniCssExtractPlugin({
        filename: "../css/accessflow.min.css", // Minified CSS file
      }),
    ],
  },
];
