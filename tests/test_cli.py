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

from chandere.cli import reorder_args, wrap


def test_reorder_args():
    assert reorder_args(["-w", "abc", "-h"]) == ["-w", "abc", "-h"]
    assert reorder_args(["-h", "-w", "abc"]) == ["-w", "abc", "-h"]
    assert reorder_args(["-h", "-h", "-w", "abc"]) == ["-w", "abc", "-h", "-h"]


@hypothesis.given(st.text())
def test_wrap(text: str):
    for line in wrap(text).split("\n"):
        assert len(line) < 80
