module.exports = defineConfig({

  devServer: {
    proxy: {
      '/api': {
        target:'http://localhost:8000',
        changeOrigin: true,
        pathRewrite: {
          '^/api': ''
        }
      },
      '/exim': {
        target: 'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey=ER48n7u4Bh2ttbS0XxeadIaJuvPKz9dY&data=AP01',
        changeOrigin: true,
        pathRewrite: {
          '^/exim': ''
        }
      }
    }
  }
  
});