Utility Functions
=================

Dynabyte's helper/utility functions (also useful for general file/byte IO)

Bytes/Arrays
------------
.. autofunction:: dynabyte.printbytes(input_data: bytearray, format: "C, list, string, or None (default)" = None, delim: str = ", ")

.. autofunction:: dynabyte.getbytearray(input_data: "str, list, bytes, or bytearray")

.. autofunction:: dynabyte.getbytes(input_string: str, file: bool = False)

Files
------
.. autofunction:: dynabyte.getsize(path, Print: bool = False)

.. autofunction:: dynabyte.gethash(path, hash: str = "md5", Print: bool = False)

.. autofunction:: dynabyte.comparefilebytes(filepath1: str, filepath2: str, verbose: bool = True)

.. autofunction:: dynabyte.deletefile(filepath: str)

.. autofunction:: dynabyte.delete_output(function)

Bit-wise Operations
-------------------
.. autofunction:: dynabyte.RotateLeft(x: int, n: int)

.. autofunction:: dynabyte.RotateRight(x: int, n: int)
