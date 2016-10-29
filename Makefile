DOCPATH = docs

.PHONY: test man rmman doc

# Tests
test:
	PYTHONPATH=. pytest -v tests/test_*.py


# Manpage compression
doc: $(DOCPATH)/chandere2.1.gz
$(DOCPATH)/chandere2.1.gz: $(DOCPATH)/chandere2.1
	gzip -k $(DOCPATH)/chandere2.1
