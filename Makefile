# Copyright (C) 2017 Jakob Kreuze, All Rights Reserved.
#
# This file is part of Chandere.
#
# Chandere is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# Chandere is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with Chandere. If not, see <http://www.gnu.org/licenses/>.

DOCPATH = docs

$(DOCPATH)/chandere.1: $(DOCPATH)/chandere.1.md
	pandoc $(DOCPATH)/chandere.1.md -s -t man > $(DOCPATH)/chandere.1

$(DOCPATH)/chandere.1.gz: $(DOCPATH)/chandere.1
	gzip -k $(DOCPATH)/chandere.1

doc: $(DOCPATH)/chandere.1.gz

test:
	python -m pytest -v $(find tests | grep -e .py^)

.PHONY: test doc
