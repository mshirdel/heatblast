var path = require("path");
var webpack = require("webpack");
var BundleTracker = require("webpack-bundle-tracker");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

const devMode = process.env.NODE_ENV !== "production";
// const devMode = true;

module.exports = {
  context: __dirname,

  entry: "./assets/js/index", // entry point of our app. assets/js/index.js should require other js modules and dependencies it needs

  output: {
    path: path.resolve("./assets/bundles/"),
    // filename: "[name]-[hash].js"
    filename: devMode ? "[name].js" : "[name]-[hash].js"
  },

  plugins: [
    new BundleTracker({ filename: "./webpack-stats.json" }),
    new webpack.ProvidePlugin({
      $: "jquery",
      jQuery: "jquery"
    }),
    new webpack.ProvidePlugin({
      persianDate: "persian-date/dist/persian-date.min.js"
    }),
    new MiniCssExtractPlugin({
      filename: devMode ? "[name].css" : "[name].[hash].css",
      chunkFilename: devMode ? "[id].css" : "[id].[hash].css"
    })
  ],

  module: {
    rules: [
      {
        test: /\.(sa|sc|c)ss$/,
        use: [
          {
            loader: MiniCssExtractPlugin.loader,
            options: {
              hmr: true //process.env.NODE_ENV === "development"
            }
          },
          "css-loader"
          //   "postcss-loader",
          //   "sass-loader"
        ]
      },
      {
        test: /\.(woff|woff2|eot|ttf|otf)$/,
        use: ["file-loader"]
      }
    ]
  }
};
