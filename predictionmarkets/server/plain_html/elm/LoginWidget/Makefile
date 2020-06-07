all: dist/LoginWidget.js

run: dist/LoginWidget.js
	python example-server.py --open-browser

dist/LoginWidget.js: src/LoginWidget.elm
	elm make "$<" --output="$@"
