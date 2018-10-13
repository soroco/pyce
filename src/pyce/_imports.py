#   Copyright 2016-18 Soroco Americas Private Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
#   Primary Author: Wolfgang Richter <wolf@soroco.com>
#
#   Purpose: Implement the import machinery necessary for loading .pyce files.
"""
This provides the implementation of the import machinery necessary to load
PYCE-formatted, encrypted files.
"""


import sys
from importlib._bootstrap_external import (_compile_bytecode,
                                           _classify_pyc)
from importlib.machinery import (FileFinder, ModuleSpec, PathFinder,
                                 SourcelessFileLoader)
from os.path import normcase, relpath
from typing import Any, Dict, List, Optional, Tuple

from pyce._crypto import decrypt

# Globals
EXTENSIONS = ['.pyce']


class PYCEFileLoader(SourcelessFileLoader):
    """
    This class is responsible for decrypting and loading PYCE-formatted files.
    """

    def __init__(self, fullname: str, path: str) -> None:
        """
        Instantiate a PYCEFileLoader to be used for decrypting and loading
        PYCE-formatted files.

        Args:
            fullname: The name of the source file to load
            path: Path to the source file

        Returns:
            None
        """
        super().__init__(fullname, path)

    # Augmented from original Python 3.7 source:
    # https://github.com/python/cpython/blob/3.7/Lib/importlib/_bootstrap_external.py#L992
    def get_code(self, fullname: str) -> Any:
        """
        Decrypt, and interpret as Python bytecode into a module return.

        Args:
            fullname: The name of the module to decrypt and compile

        Returns:
            Compiled bytecode
        """
        path = self.get_filename(fullname)
        data = self.get_data(path)

        # It is important to normalize path case for platforms like Windows
        data = decrypt(data, PYCEPathFinder.KEYS[normcase(relpath(path))])

        # Call _classify_pyc to do basic validation of the pyc but ignore the
        # result. There's no source to check against.
        exc_details = {
            'name': fullname,
            'path': path,
        }
        _classify_pyc(data, fullname, exc_details)

        return _compile_bytecode(
            memoryview(data)[16:],
            name=fullname,
            bytecode_path=path,
        )


class PYCEFileFinder(FileFinder):
    """
    This is responsible for finding PYCE-formatted files as matches to
    import statements.
    """

    def __init__(self, path: str, *loader_details: Tuple[str]) -> None:
        """
        Add the PYCEFileLoader to the list of loaders so that .pyce files
        can be loaded

        Args:
            path: The path for the loader to search on
            *loader_details: Tuple where each element is a mapping of
                             a loader to extensions it can load

        Returns:
            None
        """
        loader_details += ([PYCEFileLoader, EXTENSIONS],)
        super().__init__(path, *loader_details)


class PYCEPathFinder(PathFinder):
    """
    This class goes through the paths Python knows about and tries to
    import PYCE-formatted files.
    """

    KEYS: Dict[str, str] = {}

    def __init__(self) -> None:
        """Instantiate a PYCEPathFinder

        Returns:
            None
        """
        super().__init__()

    @classmethod
    def find_spec(cls, fullname: str, path: Optional[List[str]] = None,
                  target: Optional[str] = None) -> Optional[ModuleSpec]:
        """
        This finds and returns a Python module based on the PYCE
        encrypted format.

        Args:
            fullname: The full import (i.e. os.path)
            path: A list of paths to search for the module
            target: Eventually unused argument passed to PathFinder.find_spec

        Returns:
            A Python module based on the PYCE format
        """
        if path is None:
            path = sys.path

        sorocospec = None

        for p in path:
            sorocospec = PYCEFileFinder(p).find_spec(fullname, target)

            if sorocospec is None:
                continue
            if sorocospec.origin is None:
                sorocospec = None
                break

            # This line is important for Python's internal libraries (like
            # warnings) to work.  Setting has_location to True can break
            # introspection because Python will assume the entire source code
            # is there, but it is encrypted
            sorocospec.has_location = False

            if sorocospec is not None:
                break
        return sorocospec
