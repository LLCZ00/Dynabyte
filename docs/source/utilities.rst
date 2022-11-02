Utility Functions
=================

Dynabyte's helper/utility functions (also useful for general file/byte IO)

Bytes/Arrays
------------
.. autofunction:: dynabyte.printbytes(input: bytearray, style: "C, list, string, or None (default)" = None, delim: str = ", ", end: str = "\n")

.. autofunction:: dynabyte.getbytearray(input: "str, list, bytes, or bytearray")

.. autofunction:: dynabyte.getfilebytes(path: str, buffer: int = -1)

Files
------
.. autofunction:: dynabyte.getfilesize(path: str, verbose: bool = False)

.. autofunction:: dynabyte.getfilehash(path, hash: str = "sha256", verbose: bool = False)

.. autofunction:: dynabyte.comparefilehashes(*paths, hash: str = "sha256", verbose: bool = False)

.. autofunction:: dynabyte.comparefilebytes(filepath1: str, filepath2: str, verbose: bool = True)

.. autofunction:: dynabyte.deletefile(filepath: str)

.. autofunction:: dynabyte.delete_output(function)

Bit-wise Operations
-------------------
.. autofunction:: dynabyte.RotateLeft(x: int, n: int)

.. autofunction:: dynabyte.RotateRight(x: int, n: int)
