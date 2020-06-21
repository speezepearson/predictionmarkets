all:

test: mypy pytest

mypy: $(shell find . -name '*.py' -o -name '*.pyi')
	mypy .

pytest: $(shell find . -name '*.py')
	pytest .

elm:
	cd predictionmarkets/server/api/elm && make all
	cd predictionmarkets/server/fancy_web/elm && make all

protobuf: $(shell find protobuf -name '*.proto')
	protoc $$(find protobuf -name '*.proto') \
	  --python_out=predictionmarkets/server/api \
	  --mypy_out=predictionmarkets/server/api \
	  --elm_out=predictionmarkets/server/api/elm/protobuf/
