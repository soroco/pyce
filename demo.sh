#!/bin/bash

LIGHT_GRAY='\033[0;37m'
YELLOW='\033[1;33m'
GRAY='\033[1;30m'
RESET='\033[0m'

printf "${LIGHT_GRAY}--- Step 1: Compile Python Source to Bytecode ---${YELLOW}\n"
rm -rf pyce/__pycache__
python3 -m compileall -b pyce/hello.py
rm pyce/hello.py
printf "${LIGHT_GRAY}> ls pyce${GRAY}\n"
ls pyce
read

printf "${LIGHT_GRAY}--- Step 2: Encrypt Python Bytecode ---${GRAY}\n"
KEYS=`python3 -c 'from pyce import encrypt_path; \
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
python3 -c "from pyce import PYCEPathFinder; \
            import sys; \
            PYCEPathFinder.KEYS=dict(${KEYS}); \
            sys.meta_path.insert(0, PYCEPathFinder); \
            from pyce import hello; \
            hello.hello()"
printf "${RESET}"
read

rm pyce/hello.pyce
git checkout pyce/hello.py
