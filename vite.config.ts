import { defineConfig } from 'vite';
import { VitePluginNode } from 'vite-plugin-node';
import path from 'path';

export default defineConfig({
  plugins: [
    ...VitePluginNode({
      adapter: 'node',
      appPath: './src/cli.ts',
      exportName: 'main',
      tsCompiler: 'esbuild'
    })
  ],
  build: {
    outDir: 'dist',
    target: 'node18',
    rollupOptions: {
      input: {
        main: path.resolve(__dirname, 'src/main.ts'),
        cli: path.resolve(__dirname, 'src/cli.ts')
      },
      output: {
        entryFileNames: '[name].js',
        format: 'esm'
      },
      external: [
        'fs',
        'path',
        'pdfkit',
        'axios',
        'moment'
      ]
    }
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src')
    }
  }
});