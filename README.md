# PYCE

`pyce` is a library to work with encrypted Python bytecode.  It adds
functionality to a Python runtime by extending the way the builtin keyword
`import` works.  Currently, it assumes that convergent encryption will be used,
but the library can be extended.  For example, functionality could be added to
decrypt files via [Hashicorp's Vault](https://www.vaultproject.io/) (which also
supports convergent encryption as a mode of operation).

`pyce` enables the creation of a Trusted Computing Python environment by
ensuring each deployed file is precisely what the developer intended by
enforcing end-to-end encryption.  Execution halts if even a single bit of an
imported Python file is modified.

## How do I use it?

First, you'll want to encrypt a module or package.  **Note: this is a
destructive action.**  Do not run this on a codebase that is not saved
elsewhere.  This can recursively operate on folders, and supports exclusion
lists (to not encrypt certain files).

`pyce` expects files to be pre-compiled Python bytecode, using a command
similar to `python3 -mcompileall -b` where `-b` does an in place compilation.

```python
from pyce import encrypt_path
encrypt_path('pyce/hello.pyc')
[('pyce/hello.pyce', '443df1d5f9914d13ed27950dd81aa2dd9d3b708be416c388f3226ad398d71a14')]
```

Second, register your keys and try importing from the encrypted module or
package:

```python
from pyce import PYCEPathFinder
PYCEPathFinder.KEYS = {'pyce/hello.pyce' : '443df1d5f9914d13ed27950dd81aa2dd9d3b708be416c388f3226ad398d71a14'}

import sys
sys.meta_path.insert(0, PYCEPathFinder)
from pyce.hello import hello
hello()
```

Key distribution is outside the scope of this project.  You will need to
maintain keys typically by using a networked key server such as [Hashicorp's
Vault](https://www.vaultproject.io/).  You could pass keys by environment
variable, `stdin`, or some other mechanism.

Typically, you will leave (exclude) a stub file that is designed to just hook
Python's import path parsers, setup the keys, and then execute your code.


## What can I do with it?

**File Integrity Monitoring:** You could protect your production code running
on application servers by adding in automatic cryptographic checks of imports.

**Licensing:** You could publish encrypted modules to PyPI and only release
decryption keys to certain organizations, people, or others!  You could publish
such modules anywhere!

**At-rest Code Protection:** You could just protect code at rest by integrating
on-the-fly decryption with an IDE or other software.  This would be more of a
DIY project at this point in time, but `pyce` gives you all the building blocks
you need!

## License

All of this code is released under the [Apache v2.0
License](https://www.apache.org/licenses/LICENSE-2.0).
