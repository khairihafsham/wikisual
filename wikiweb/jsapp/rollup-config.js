import rollup      from 'rollup'
import nodeResolve from 'rollup-plugin-node-resolve'
import commonjs    from 'rollup-plugin-commonjs';
import uglify      from 'rollup-plugin-uglify'

export default {
  entry: 'dist/app/main-aot.js',
  dest: 'dist/build.js', // output a single application bundle
  sourceMap: true,
  sourceMapFile: 'dist/build.js.map',
  format: 'iife',
  plugins: [
      nodeResolve({jsnext: true, module: true}),
      commonjs({
        include: 'node_modules/**',
        namedExports: {
          'node_modules/angular2-chartjs/dist/index.js': ['ChartModule']
        }
      }),
      uglify()
  ],
  onwarn: function ( message ) {
    if (/keyword is equivalent to/.test(message)) {
      return;
    }
    console.error( message );
  }
}
