#   Copyright 2016-19 Soroco Americas Private Limited
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
#   Purpose: This module enables the loading of encrypted Python stored in the
#            Soroco format (.pyce).
"""
This defines the Soroco import machinery to import .pyce formatted Python
files.  Such files are defined as an AES-256 convergently encrypted Python
files with a SHA-512 HMAC.

You can enable the Python format for your interpreter by doing the following:

>>> from pyce import add_import_hook
>>> add_import_hook()

If you had encrypted Python code, you would want to then pass the keys for
encryption/decryption to the add_import_hook call, with the appropriate format.
"""


from pyce._crypto import encrypt_path, HMACFailureException
from pyce._imports import PYCEPathFinder, PYCEFileLoader, add_import_hook


__all__ = [
    'add_import_hook', 'encrypt_path', 'HMACFailureException',
    'PYCEPathFinder'
]

__version__ = '2.0.0'
