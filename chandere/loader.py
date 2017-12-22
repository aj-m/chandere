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

"""Interface to Chandere's dynamic module loader, for deciding which
website and action modules should be loaded at runtime.
"""

import importlib
import os
import types

from chandere.errors import ChandereError


def _script_path_to_module_name(path: str) -> str:
    """Strips any preceding path junk and the ".py" extention, if it
    exists, forming a valid module name.
    """
    s = path[path.rindex("/") + 1:]
    if s.endswith(".py"):
        return s[:-3]
    return s


def _list_submodules(package: str) -> types.GeneratorType:
    """Lists all submodules contained in a package, raising a ChandereError
    if the package could not be located.
    """
    try:
        module = importlib.import_module("chandere.{}".format(package))
        package_path = module.__path__[0]
        for filename in os.listdir(package_path):
            if filename.endswith(".py") and filename != "__init__.py":
                yield filename[:-3]
    except (AttributeError, IndexError):
        raise ChandereError("Could not locate '{}' package.".format(package))


def list_actions() -> types.GeneratorType:
    """Lists the names of all scraping actions."""
    return _list_submodules("actions")


def list_scrapers() -> types.GeneratorType:
    """Lists the names of all website scraping modules."""
    return _list_submodules("websites")


def load_action(action: str) -> types.ModuleType:
    """Returns the module for the given action."""
    try:
        return importlib.import_module("chandere.actions.{}".format(action))
    except ModuleNotFoundError:
        raise ChandereError("No such action, '{}'.".format(action))


def load_scraper(website: str) -> types.ModuleType:
    """Returns the scraper module for the given website."""
    try:
        return importlib.import_module("chandere.websites.{}".format(website))
    except ModuleNotFoundError:
        raise ChandereError("No such website, '{}'.".format(website))


def load_custom_action(path: str) -> types.ModuleType:
    """Loads and returns the action module at the given path."""
    try:
        name = _script_path_to_module_name(path)
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except FileNotFoundError:
        raise ChandereError("No such file '{}'.".format(path))


def load_custom_scraper(path: str) -> types.ModuleType:
    """Loads and returns the scraper module at the given path."""
    try:
        name = _script_path_to_module_name(path)
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except FileNotFoundError:
        raise ChandereError("No such file '{}'.".format(path))
