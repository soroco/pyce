#!/bin/bash
#   Copyright 2017-19 Soroco Americas Private Limited
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

if [ -n "${PYTHON+x}" ]
then
    printf "${GRAY}Using Python: ${PYTHON}\n\n"
else
    PYTHON=python3
fi

printf "${LIGHT_GRAY}--- Step 0: Inspect Python Source ---${YELLOW}\n"
printf "${LIGHT_GRAY}> pygmentize -f terminal pyce/hello.py${RESET}\n"
pygmentize -f terminal pyce/hello.py
read

printf "${LIGHT_GRAY}--- Step 1: Make tmpdir, copy Python Source to tmpdir ---${YELLOW}\n"
TMPDIR=`mktemp -d`
cp pyce/hello.py $TMPDIR/
printf "${LIGHT_GRAY}> ls ${TMPDIR}${GRAY}\n"
ls $TMPDIR
read

printf "${LIGHT_GRAY}--- Step 2: Compile Python Source to Bytecode ---${YELLOW}\n"
$PYTHON -m compileall -b ${TMPDIR}/hello.py
rm $TMPDIR/hello.py
printf "${LIGHT_GRAY}> ls ${TMPDIR}${GRAY}\n"
ls $TMPDIR
read
printf "${LIGHT_GRAY}> xxd ${TMPDIR}/hello.pyc${GRAY}\n"
xxd ${TMPDIR}/hello.pyc
read

printf "${LIGHT_GRAY}--- Step 3: Encrypt Python Bytecode ---${GRAY}\n"
KEYS=`$PYTHON -c "from pyce import encrypt_path; \
                  from os import chdir; \
                  chdir('${TMPDIR}'); \
                  print(encrypt_path('hello.pyc'), end='')"`
printf "${YELLOW}${KEYS}\n"
printf "${LIGHT_GRAY}> ls ${TMPDIR}${GRAY}\n"
ls $TMPDIR
read

printf "${LIGHT_GRAY}--- Step 4: Import and Execute Encrypted Python Bytecode ---\n"
printf "${LIGHT_GRAY}> ls ${TMPDIR}${GRAY}\n"
ls $TMPDIR
printf "${YELLOW}"
$PYTHON -c "import sys; \
            from os import chdir; \
            from pyce import PYCEPathFinder; \
            chdir('${TMPDIR}'); \
            PYCEPathFinder.KEYS=dict(${KEYS}); \
            sys.meta_path.insert(0, PYCEPathFinder); \
            import hello; \
            hello.hello()"
printf "${RESET}"
read

rm -rf $TMPDIR
