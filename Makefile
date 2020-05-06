all:

test: mypy pytest

mypy: $(shell find . -name '*.py' -o -name '*.pyi')
	mypy .

pytest: $(shell find . -name '*.py')
	pytest .
