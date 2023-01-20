Core
=====

Classes and functions providing the core functionality of Dynabyte


Built-in Operations
-------------------
The functions can be used directly, or as methods from *Array* and *File* objects (with the exception of *RotateLeft* and *RotateRight*).

.. autofunction:: dynabyte.operations.XOR

.. autofunction:: dynabyte.operations.SUB

.. autofunction:: dynabyte.operations.ADD

.. autofunction:: dynabyte.operations.ROL

.. autofunction:: dynabyte.operations.ROR

.. autofunction:: dynabyte.operations.RC4

.. autofunction:: dynabyte.operations.AESEncrypt

.. autofunction:: dynabyte.operations.AESDecrypt

.. autofunction:: dynabyte.operations.reverse

.. autofunction:: dynabyte.operations.pad

.. autofunction:: dynabyte.operations.RotateLeft

.. autofunction:: dynabyte.operations.RotateRight


Classes
-------
DynabyteBase
^^^^^^^^^^^^^
Base class for dynabyte.core.Array and dynabyte.core.File, providing methods for using the aforementioned built-in operations. The *XOR*, *ADD*, *SUB*, *ROL*, and *ROR* methods can also be called with their respective binary operators (^, +, -, <<, >>).

.. autofunction:: dynabyte.core.DynabyteBase.XOR

.. autofunction:: dynabyte.core.DynabyteBase.SUB

.. autofunction:: dynabyte.core.DynabyteBase.ADD

.. autofunction:: dynabyte.core.DynabyteBase.ROL

.. autofunction:: dynabyte.core.DynabyteBase.ROR

.. autofunction:: dynabyte.core.DynabyteBase.RC4

.. autofunction:: dynabyte.core.DynabyteBase.AESEncrypt

.. autofunction:: dynabyte.core.DynabyteBase.AESDecrypt

.. autofunction:: dynabyte.core.DynabyteBase.reverse

.. autofunction:: dynabyte.core.DynabyteBase.b64encode

.. autofunction:: dynabyte.core.DynabyteBase.b64decode

.. autofunction:: dynabyte.core.DynabyteBase.pad

.. autofunction:: dynabyte.core.DynabyteBase.strip

Array
^^^^^
Array objects are iterable, and accept string, integer, byte, bytearray, list and other dynabyte.core.Array objects as input. List-type objects can contain a combination of any other valid input type. See Basic Usage section for details on printing/formating.

.. autofunction:: dynabyte.core.Array

.. autofunction:: dynabyte.core.Array.fromfile

.. autofunction:: dynabyte.core.Array.writefile

.. autofunction:: dynabyte.core.Array.run

.. autofunction:: dynabyte.core.Array.gethash

.. autofunction:: dynabyte.core.Array.insert

.. autofunction:: dynabyte.core.Array.append

.. autofunction:: dynabyte.core.Array.extend

File
^^^^
.. autofunction:: dynabyte.core.File

.. autofunction:: dynabyte.core.File.run

.. autofunction:: dynabyte.core.File.getbytes

.. autofunction:: dynabyte.core.File.getsize

.. autofunction:: dynabyte.core.File.gethash

.. autofunction:: dynabyte.core.File.delete


Utility Functions
-----------------

Dynabyte's helper/utility functions


.. autofunction:: dynabyte.utils.getbytearray

.. autofunction:: dynabyte.utils.bprint

.. autofunction:: dynabyte.utils.random_key

.. autofunction:: dynabyte.utils.comparefilebytes
