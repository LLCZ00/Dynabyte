Core
=====

Classes and functions providing the core functionality of Dynabyte

Classes
-------

OperatorMixIn
^^^^^^^^^^^^^
Base class for dynabyte.Array and dynabyte.File, provides methods for using bit-wise operations. It also overrides their respective 'magic methods' so they can be used with simple binary operators (^, + , -, etc.)

.. autofunction:: dynabyte.core.OperatorMixIn

.. autofunction:: dynabyte.core.OperatorMixIn.XOR

.. autofunction:: dynabyte.core.OperatorMixIn.SUB

.. autofunction:: dynabyte.core.OperatorMixIn.ADD

.. autofunction:: dynabyte.core.OperatorMixIn.ROL

.. autofunction:: dynabyte.core.OperatorMixIn.ROR

Array
^^^^^
.. autofunction:: dynabyte.core.Array

.. autofunction:: dynabyte.core.Array.run

.. autofunction:: dynabyte.core.Array.format

.. autofunction:: dynabyte.core.Array.bytes

File
^^^^
.. autofunction:: dynabyte.core.File

.. autofunction:: dynabyte.core.File.run

.. autofunction:: dynabyte.core.File.getfilebytes

.. autofunction:: dynabyte.core.File.getsize

.. autofunction:: dynabyte.core.File.gethash

.. autofunction:: dynabyte.core.File.delete


Built-in Operations
-------------------
These functions do not belong to any dynabyte classes, and simply return the byte representation of their results

.. autofunction:: dynabyte.ops.XOR

.. autofunction:: dynabyte.ops.SUB

.. autofunction:: dynabyte.ops.ADD

.. autofunction:: dynabyte.ops.ROL

.. autofunction:: dynabyte.ops.ROR
