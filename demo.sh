#!/bin/bash
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
#   Purpose: Test the PYCE library.


LIGHT_GRAY='\033[0;37m'
YELLOW='\033[1;33m'
GRAY='\033[1;30m'
RESET='\033[0m'

if [[ -v "PYTHON" ]]
then
    printf "${GRAY}Using Python: ${PYTHON}\n"
else
    PYTHON=python3
fi

printf "${LIGHT_GRAY}--- Step 1: Compile Python Source to Bytecode ---${YELLOW}\n"
rm -rf pyce/__pycache__
$PYTHON -m compileall -b pyce/hello.py
rm pyce/hello.py
printf "${LIGHT_GRAY}> ls pyce${GRAY}\n"
ls pyce
read

printf "${LIGHT_GRAY}--- Step 2: Encrypt Python Bytecode ---${GRAY}\n"
KEYS=`$PYTHON -c 'from pyce import encrypt_path; \
                  print(encrypt_path("pyce/hello.pyc"), end="")'`
printf "${YELLOW}${KEYS}\n"
printf "${LIGHT_GRAY}> ls pyce${GRAY}\n"
ls pyce
printf "${LIGHT_GRAY}> ls pyce/__pycache__${GRAY}\n"
ls pyce/__pycache__
read

printf "${LIGHT_GRAY}--- Step 3: Import and Execute Encrypted Python Bytecode ---\n"
printf "${LIGHT_GRAY}> ls pyce${GRAY}\n"
ls pyce
printf "${LIGHT_GRAY}> ls pyce/__pycache__${GRAY}\n"
ls pyce/__pycache__
printf "${YELLOW}"
$PYTHON -c "from pyce import PYCEPathFinder; \
            import sys; \
            PYCEPathFinder.KEYS=dict(${KEYS}); \
            sys.meta_path.insert(0, PYCEPathFinder); \
            from pyce import hello; \
            hello.hello()"
printf "${RESET}"
read

rm pyce/hello.pyce
git checkout pyce/hello.py
