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

import hypothesis
import hypothesis.strategies as st

from chandere.output import _ansi_escape, _ansi_wrap


@hypothesis.given(st.text())
def test_ansi_escape(text: str):
    escape = _ansi_escape(text)
    assert escape.startswith("\033[")
    assert escape.endswith("m")


@hypothesis.given(st.text(), st.text())
def test_ansi_wrap(escape: str, text: str):
    assert _ansi_wrap(escape, text).endswith("\033[0m")
