const path = require('path');

function resolve (dir) {
  return path.join(__dirname, '..', dir)
};

const ExtractTextPlugin = require('extract-text-webpack-plugin');

module.exports = {
  entry: {
      app: './src/main.js'
  },
  output: {
    path: resolve('./dist'),
    publicPath: 'dist/',
    filename: 'dist.js'
  },
  resolve: {
    extensions: ['.js', '.json', '.scss', '.html'],
    alias: {
      '@': resolve('src'),
      'styles': resolve('src/assets/styles'),
      'scss-loader': 'sass-loader'
    }
  },
  module: {
    loaders: [
      {
        test: /\.js$/,
        loader: 'babel-loader',
        include: [resolve('src')]
      },
      {
        test: /\.s[a|c]ss$/,
        loader: ExtractTextPlugin.extract({
          fallback: 'style-loader',
          use: 'css-loader!sass-loader'
        })
      },
      {
        test: /\.css$/,
        loader: ExtractTextPlugin.extract({
          fallback: 'style-loader',
          use: 'css-loader'
        })
      },
      { 
        test: /\.html$/, 
        loader: 'raw-loader'
      },
      {
        test: /\.(png|jpe|jpg|woff|woff2|eot|ttf|svg)(\?.*$|$)/,
        loader: 'url-loader'
      },
      { 
        test: /\.(ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/, 
        loader: 'file-loader'
      }
    ]
  },
  plugins: [
    new ExtractTextPlugin('dist.css'),
  ]
};