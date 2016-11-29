ngc:
	node_modules/.bin/ngc -p tsconfig-aot.json

rollup:
	node_modules/.bin/rollup -c rollup-config.js

aot-build: ngc rollup

build:
	npm run tsc
