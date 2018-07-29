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
#   Purpose: Provide convergent encryption primitives for use in a larger
#            trusted computing system.
"""
This file implements convergent encryption logic for use in a deduplicating
storage system.  It is designed to be used in tandem with an import loader in
Python that can load encrypted files.

Example use:

>>> from pyce.crypto import encrypt_path, decryptf
>>> path, key = encrypt_path('pyce/hello.pyc')[0]
>>> print(decryptf(path, key))
"""


from hashlib import sha256 as srchash
from hmac import compare_digest
from hmac import new as hmac
from os import rename, walk
from os.path import dirname, isfile, join, splitext
from typing import List, Optional, Set, Tuple

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers.algorithms import AES as CIPHER
from cryptography.hazmat.primitives.ciphers.modes import CTR as MODE

BACKEND = default_backend()
ENC_EXT = {'.pyc'}
HMAC_HS = 'sha512'


class HMACFailureException(Exception):
    """This class represents a failure in verifying the HMAC of a file."""

    def __init__(self, message: str) -> None:
        """
        Instantiate an HMACFailureException

        Args:
            message: Error message

        Returns:
            None
        """
        self.message = message
        super().__init__(message)


def encrypt_path(path: str, extensions: Set[str] = ENC_EXT, exclusions:
                 Optional[Set[str]] = None) -> List[Tuple[str, str]]:
    """
    This function convergently encrypts the file at path.  If path is a
    directory, it recursively encrypts all files in the directory which have
    matching extensions.  After encryption, it appends an HMAC, and renames
    the file to have a '.pyce' extension.

    It is close to: AES_256_CTR_HMAC_SHA_512

    Args:
        path: path to convergently encrypt (file or directory)
        extensions: the file extensions that should be encrypted
        exclusions: files that should not be encrypted

    Returns:
        List of all paths and their encryption key
    """
    if exclusions is None:
        exclusions = set()

    manifest = []

    walker = walk(path) if not isfile(path) else [('', None, [path])]

    for root, _, files in walker:
        for fname in files:
            _, ext = splitext(fname)

            if ext not in extensions:
                continue

            absolute_path = join(root, fname)

            # Skip absolute paths
            if absolute_path in exclusions or root in exclusions:
                continue

            # Skip requested folders
            dirn = dirname(root)
            skip = False
            while dirn and dirn != '/' and not dirn.endswith(':\\'):
                if dirn in exclusions:
                    skip = True
                    break
                dirn = dirname(dirn)

            if skip:
                continue

            with open(absolute_path, 'rb+') as openf:
                # read
                data = openf.read()

                # hash
                hashv = srchash(data)
                key = hashv.digest()

                # encrypt
                cipher = Cipher(CIPHER(key), MODE(key[0:16]), backend=BACKEND)
                encryptor = cipher.encryptor()
                ciphertext = encryptor.update(data)

                # write out
                openf.seek(0)
                openf.write(ciphertext)

                # append HMAC
                openf.write(hmac(key, ciphertext, HMAC_HS).digest())

            new_absolute_path, ext = splitext(absolute_path)
            new_absolute_path += ext + 'e'
            rename(absolute_path, new_absolute_path)
            manifest.append((new_absolute_path, hashv.hexdigest()))

    return manifest


def __verify_hmac(data: bytes, ohmac: bytes, key: bytes) -> bool:
    """
    This function verifies that a provided HMAC matches a computed HMAC for
    the data given a key.

    Args:
        data: the data to HMAC and verify
        ohmac: the original HMAC, normally appended to the data
        key: the key to HMAC with for verification

    Returns:
        a boolean value denoting whether or not the HMAC's match
    """
    return compare_digest(ohmac, hmac(key, data, HMAC_HS).digest())


def decrypt(data: bytes, key: str) -> bytes:
    """
    This function takes in a list of ciphertext bytes, verifies their appended
    HMAC, and returns a corresponding list of plaintext bytes.  If there is a
    problem verifying HMAC, this function raises HMACFailureException.

    Args:
        data: the ciphertext to verify and decrypt
        key: the key to verify the HMAC with and decrypt

    Returns:
        The decrypted plaintext bytes for the file

    Raises:
        HMACFailureException if HMAC verification fails
    """
    data, ohmac = data[:-64], data[-64:]
    bkey = int(key, 16).to_bytes(32, 'big')

    # verify
    if not __verify_hmac(data, ohmac, bkey):
        raise HMACFailureException('HMAC verification has failed.')

    # decrypt into plaintext
    decryptor = Cipher(CIPHER(bkey), mode=MODE(bkey[0:16]),
                       backend=BACKEND).decryptor()
    data = decryptor.update(data) + decryptor.finalize()

    return data


def decryptf(path: str, key: str) -> bytes:
    """
    This function takes a path and a key and returns the decrypted data.  It
    also verifies the contents of the file via an HMAC.  If there is a problem
    verifying HMAC, this function raises HMACFailureException.

    Args:
        path: the path to the file to decrypt
        key: the key to verify the HMAC

    Returns:
        The decrypted plaintext bytes for the file

    Raises:
        HMACFailureException if HMAC verification fails
    """
    data = b''

    with open(path, 'rb') as fd:
        data = fd.read()

        try:
            data = decrypt(data, key)
        except HMACFailureException as error:
            error.message = 'File {} failed HMAC verification.'.format(path)
            raise error

    return data
