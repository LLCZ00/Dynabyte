Core
=====

Classes and functions providing the core functionality of Dynabyte

Functions
---------
The main functions by which to interact with the classes

.. autofunction:: dynabyte.loadarray(input_data: "Input byte array (str, bytearray, list, or bytes)")

.. autofunction:: dynabyte.loadfile(path: "Input file path", output: "Optional output file path" = None, buffersize: int = 8192)

Classes
-------
DynabyteArray
^^^^^^^^^^^^^^^^^^^^^
.. autofunction:: dynabyte.core.DynabyteArray(inputarray: bytearray)

.. autofunction:: dynabyte.core.DynabyteArray.run(self, callback: "Callback function: func(byte, offset) -> byte", count: "Number of times to run array though callback function" = 1)

.. autofunction:: dynabyte.core.DynabyteArray.printbytes(self, format: "C, Python, string, or 'raw' array format" = None, delim: str = ", ")


DynabyteFile
^^^^^^^^^^^^^^^^^^^^^
.. autofunction:: dynabyte.core.DynabyteFile(path: str, output: str, buffersize: int)

.. autofunction:: dynabyte.core.DynabyteFile.run(self, callback: "Callback function: func(byte, offset) -> byte", *, output: "Optional output file path" = None, count: "Number of times to run array though callback function" = 1)

.. autofunction:: dynabyte.core.DynabyteFile.getsize(self, Print: bool = False)

.. autofunction:: dynabyte.core.DynabyteFile.gethash(self, hash: str = "md5", Print: bool = False)

.. autofunction:: dynabyte.core.DynabyteFile.comparetofile(self, filepath: str, verbose: bool = True)


DynabyteCallback
^^^^^^^^^^^^^^^^^^^^^
.. autofunction:: dynabyte.core.DynabyteCallback(function)

.. autofunction:: dynabyte.core.DynabyteCallback.__call__(self, chunk: bytes)

DynabyteFileHandler
^^^^^^^^^^^^^^^^^^^^^
.. autofunction:: dynabyte.core.DynabyteFileHandler(path: str, output: str, buffersize: int)

.. autofunction:: dynabyte.core.DynabyteFileHandler.write(chunk: bytes)