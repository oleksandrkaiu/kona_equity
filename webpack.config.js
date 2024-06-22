const path = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const { CleanWebpackPlugin } = require("clean-webpack-plugin");
const OptimizeCssAssetWebpackPlugin = require("optimize-css-assets-webpack-plugin");
const TerserWebpackPlugin = require("terser-webpack-plugin");

const isDev = process.env.NODE_ENV === "development";
const isProd = !isDev;

const config = {
  entry: {
    main: ["@babel/polyfill", "@backend_django_v2/main.js"],
  },
  output: {
    path: path.resolve(
      __dirname,
      "backend_django_v2/static/backend_django_v2/prepared"
    ),
    filename: "[name].js",
  },
  resolve: {
    extensions: [".js", ".jsx"],
    alias: {
      "@backend_django_v2": path.resolve(__dirname, "backend_django_v2/src"),
      "@": path.resolve(__dirname),
    },
  },
  devtool: isDev ? "eval" : false,
  optimization: {
    minimizer: isProd
      ? [new OptimizeCssAssetWebpackPlugin(), new TerserWebpackPlugin()]
      : [],
  },
  performance: {
    hints: false,
  },
  plugins: [
    new CleanWebpackPlugin(),
    new MiniCssExtractPlugin({
      filename: "[name].css",
    }),
  ],
  module: {
    rules: [
      {
        test: /\.s[ac]ss$/i,
        use: [
          {
            loader: MiniCssExtractPlugin.loader,
            options: {
              publicPath: "",
            },
          },
          "css-loader",
          "sass-loader",
        ],
      },
      {
        test: /\.css$/i,
        use: [
          {
            loader: MiniCssExtractPlugin.loader,
            options: {
              publicPath: "",
            },
          },
          "css-loader",
        ],
      },
      {
        test: /\.(png|woff|woff2|eot|ttf|svg)$/,
        use: {
          loader: "url-loader?limit=100000",
          options: {
            limit: 8192,
            name: "assets/[hash].[ext]",
          },
        },
      },
      {
        test: /\.(png|jpe?g|gif)$/i,
        use: [
          {
            loader: "file-loader",
            options: {
              outputPath: "images",
            },
          },
        ],
      },
      {
        test: /\.js$/,
        exclude: /(node_modules|bower_components)/,
        use: {
          loader: "babel-loader",
          options: {
            presets: [["@babel/preset-env"]],
          },
        },
      },
    ],
  },
};

module.exports = config;
