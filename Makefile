DOCPATH := docs
PYTHONPATH := .

.PHONY: test doc


# Manpage compression
doc: $(DOCPATH)/chandere2.1.gz
$(DOCPATH)/chandere2.1.gz: $(DOCPATH)/chandere2.1
	gzip -k $(DOCPATH)/chandere2.1


# Tests
test:
	python -m pytest -v tests/test_*.py
