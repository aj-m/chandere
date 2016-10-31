DOCPATH = docs

.PHONY: test doc

# Tests
test:
	PYTHONPATH=. python -m pytest -v tests/test_*.py


# Manpage compression
doc: $(DOCPATH)/chandere2.1.gz
$(DOCPATH)/chandere2.1.gz: $(DOCPATH)/chandere2.1
	gzip -k $(DOCPATH)/chandere2.1
