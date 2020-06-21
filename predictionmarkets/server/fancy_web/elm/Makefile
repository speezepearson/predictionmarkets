all: $(shell find src -name '*.elm')
	for src in $^; do \
	  dest=$$(echo "$$src" | sed -e 's/\.elm$$//' -e 's/src/dist/' ); \
	  echo "src is: $$src" ; \
	  echo "dest is: $$dest" ; \
	  elm make "$$src" --output="$$dest.js" ; \
	  elm make "$$src" && if test -f index.html; then mv index.html "$$dest.html"; fi ; \
	done
