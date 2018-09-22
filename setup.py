#   Copyright 2017-18 Soroco Americas Private Limited
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
#   Purpose: Make this library publishable to PyPI.  This file is a modified
#   version of
#   https://raw.githubusercontent.com/pypa/sampleproject/master/setup.py.
"""
This library implements the Soroco PYCE format for encrypting Python bytecode
files, and loading them dynamically at runtime by changing the way that the
`import` builtin works.
"""


from codecs import open
from os import path
from setuptools import setup, find_packages


from pyce import __version__


# Get the long description from the README file
HERE = path.abspath(path.dirname(__file__))
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

setup(
    author='Soroco Americas Private Limited',  # Optional
    author_email='opensource@soroco.com',  # Optional
    classifiers=[  # Optional
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Security :: Cryptography',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Operating System :: Microsoft :: Windows :: Windows Server 2008',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.7',
    ],
    description='Execute encrypted Python bytecode.',  # Required
    install_requires=['cryptography==2.3.1'],  # Optional
    keywords='cryptography encryption import pyce',  # Optional
    license='Apache Software License Version 2.0',  # Optional
    long_description=LONG_DESCRIPTION,  # Optional
    long_description_content_type="text/markdown",  # Optional
    maintainer='Soroco Americas Private Limited',  # Optional
    maintainer_email='opensource@soroco.com',  # Optional
    name='pyce',  # Required
    platforms=['Windows 10', 'Windows Server 2008', 'Windows Server 2012',
               'Linux'],  # Optional
    packages=find_packages(exclude=[]),  # Required
    python_requires='>=3.7, <3.8',
    url='https://github.com/soroco/pyce',  # Optional
    version=__version__,  # Required
)
