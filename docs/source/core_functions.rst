Core
=====

Classes and functions providing the core functionality of Dynabyte

Main Function
-------------
The main functions by which to interact with the classes

.. autofunction:: dynabyte.load(input: "Input array (str, bytearray, list, or bytes) or file path", file: "Specify string as a filepath" = False)


Classes
-------

BuiltIns
^^^^^^^^^^^^^^^^^^^^^

Base class, functions are inherited by DynabyteArray and DynabyteFile

.. autofunction:: dynabyte.core.BuiltIns.XOR(self, value: "int, str, list, bytes, or bytearray" = 0, *, count: int = 1)

.. autofunction:: dynabyte.core.BuiltIns.SUB(self, value: int = 0, *, count: int = 1)

.. autofunction:: dynabyte.core.BuiltIns.ADD(self, value: int = 0, *, count: int = 1)

.. autofunction:: dynabyte.core.BuiltIns.ROL(self, value: int = 0, *, count: int = 1)

.. autofunction:: dynabyte.core.BuiltIns.ROR(self, value: int = 0, *, count: int = 1)

DynabyteArray
^^^^^^^^^^^^^^^^^^^^^
.. autofunction:: dynabyte.core.DynabyteArray(input)

.. autofunction:: dynabyte.core.DynabyteArray.run(self, callback: "Callback function: func(byte, offset) -> byte", *, output: "Optional output file path" = None, count: "Number of times to run array though callback function" = 1)

.. autofunction:: dynabyte.core.DynabyteArray.getdata(self, format=None)

.. autofunction:: dynabyte.core.DynabyteArray.print(self, style: "C, Python, string, or 'raw' array format" = None, delim: "Delimiter between values" = ", ", end: str = "\n")

DynabyteFile
^^^^^^^^^^^^^^^^^^^^^
.. autofunction:: dynabyte.core.DynabyteFile(path: str, output: str, buffersize: int)

.. autofunction:: dynabyte.core.DynabyteFile.run(self, callback: "Callback function: func(byte, offset) -> byte", *, output: "Optional output file path" = None, count: "Number of times to run array though callback function" = 1)

.. autofunction:: dynabyte.core.DynabyteFile.getsize(self, verbose: bool = False)

.. autofunction:: dynabyte.core.DynabyteFile.gethash(self, hash: str = "sha256", verbose: bool = False)

.. autofunction:: dynabyte.core.DynabyteFile.delete(self)


DynabyteCallback
^^^^^^^^^^^^^^^^^^^^^
.. autofunction:: dynabyte.core.DynabyteCallback(function)

.. autofunction:: dynabyte.core.DynabyteCallback.__call__(self, chunk: bytes)

DynabyteFileManager
^^^^^^^^^^^^^^^^^^^^^
.. autofunction:: dynabyte.core.DynabyteFileManager(input: str, output: str, buffersize: int))

.. autofunction:: dynabyte.core.DynabyteFileManager.write(chunk: bytes)
