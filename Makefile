DOCPATH := docs
PYTHONPATH := .

NUITKAFLAGS := --show-progress --remove-output

.PHONY: test doc


# Executable compilation
executable:
	nuitka $(NUITKAFLAGS) --recurse-all chandere2/__main__.py
	mv __main__.exe chandere2


# Script compilation
script:
	python compile.py chandere2.py


# Manpage compression
doc: $(DOCPATH)/chandere2.1.gz
$(DOCPATH)/chandere2.1.gz: $(DOCPATH)/chandere2.1
	gzip -k $(DOCPATH)/chandere2.1


# Tests
test:
	python -m pytest -v tests/test_*.py
