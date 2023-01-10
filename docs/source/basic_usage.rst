Basic Usage
===========

Built-In Operations
-------------------
Built-in operation methods (*XOR*, *ADD*, *SUB*, *ROL*, *ROR*) can be used on both files and strings, the order of execution being left to right. 
*XOR* can also used to encode/decode against a key

Example: Encrypting a binary file w/ key 
----------------------------------------
>>> import dynabyte as dyna
>>> dfile = dyna.File(r"C:\Users\IEUser\suspicious.bin")
>>> dfile.XOR("Bada BING!").ADD(0xc)

The built-in functions from dynabyte.ops can be used to avoid creating a dynabyte object:

.. code-block:: python

	from dynabyte.ops import *
	
	string = "shmebulock"
	encoded = XOR(SUB(ROL(string, 3), 12), 0xC)
	decoded = ROR(ADD(XOR(encoded, 0xC), 12), 3)
	
	print(encoded) # b'\x83;S\x13\x0b\x93[c\x03C'
	print(decoded.decode()) # "shmebulock"
	
	
Callback Functions
------------------
Custom callback functions can be used to execute operations with the *run()* method. This is generally more efficient for longer operations, and is recommended for files. Using callback functions also gives you access to the "global" offset of a particular byte, as well as the option to write the results to a new file.

They must fit the following signature:

.. py:function:: callback_func(byte: int, offset: int)

   Return byte, altered or otherwise

Callback lambdas are dynamically generated and shown when using the CLI tool.

*Callback functions can be defined like regular functions or as lambdas.*

Example: De-obfuscating a string
--------------------------------
>>> import dynabyte
>>> decrypt = dynabyte.Array("\osb`pnarq-`a_v{t")
>>> decrypt.run(lambda byte, offset : (byte + 3) ^ 0x10)
>>> decrypt
Obfuscated string

