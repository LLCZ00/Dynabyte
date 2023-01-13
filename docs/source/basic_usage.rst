Basic Usage
===========

Built-In Operations
-------------------
Built-in operation methods (*XOR*, *ADD*, *SUB*, *ROL*, *ROR*) can be used on both files and strings, the order of execution being left to right. 
*XOR* can also used to encode/decode against a key

Basic Operations
----------------
Using XOR(), one of dynabytes built-in bit-wise operation functions, you can quickly XOR data against a key or value. Input data and the value/key can be string, list, int, or bytes objects. Other built-in functions include *XOR*, *ADD*, *SUB*, *ROL*, and *ROR*, and all return bytes objects.

.. code-block:: python

	from dynabyte import XOR
	
	encoded_bytes = [0x35, 0x36, 0x72, 0x3a, 0x25, 0x26, 0x36, 0x45, 0x54, 0x56, 0x13, 0x2b, 0x3b, 0x20, 0x36, 0x25, 0x22]

	mystr = XOR(encoded_bytes, "XOR_KEY!123")

	print(mystr.decode()) # "my encoded string"


All built-in functions can be imported at once from dynabyte.ops:

.. code-block:: python

	from dynabyte.ops import *
	
	string = "shmebulock"
	encoded = XOR(SUB(ROL(string, 3), 12), 0xC)
	decoded = ROR(ADD(XOR(encoded, 0xC), 12), 3)
	
	print(encoded) # b'\x83;S\x13\x0b\x93[c\x03C'
	print(decoded.decode()) # "shmebulock"


Array and File Objects 
-----------------------
Dynabyte offers Array and File classes, which offer more streamlined control over input data and operations. Upon initialization, Array objects accept string, list, int, bytes, or other dynabyte Array objects. They have the same built-in bit-wise operation methods, which can be chained together in a single line (execution order being from left to right).

>>> import dynabyte as dyna
>>> dfile = dyna.File(r"C:\Users\IEUser\suspicious.bin")
>>> dfile.XOR("Bada BING!").ADD(0xc)


Dynabyte objects, when printed, attempt to decode data to UTF-8. The class attribute 'encoding' can be changed to whatever the situation demands. Acceptable encodings can be found at https://docs.python.org/3/library/codecs.html#standard-encodings. 

.. code-block:: python

	import dynabyte
	
	encoded_bytes = [0x4b, 0x8e, 0x48, 0x3f, 0xa, 0x5d, 0x37, 0x32, 0x33, 0x23, 0x7, 0x3a, 0x1, 0x5e, 0x30, 0x3f, 0x7, 0x3d, 0x64, 0x64, 0x56, 0x47, 0x53, 0x32, 0x23, 0x71, 0x59, 0x74, 0x5, 0x50, 0x7, 0x41, 0xa, 0x93, 0x62]
	key = "Xq%?k][2U#h:l^U?c=Dd%G'2Qq0tkP`A?l;" # Key initially generated with dyna.random_key()
	
	myarray = dynabyte.Array(encoded_bytes)
	myarray.encoding = "utf_16_le"
	myarray.XOR(key)
	
	print(myarray) # Errors when decoding malformed strings are ignored
	
	
Typical binary operators can also be used:

.. code-block:: python

	from dynabyte import Array

	encoded_str = ((Array("Pas$$w0rd!") << 0x15) ^ "key") + 0xA	
	decoded_str = ((Array(encoded_str) - 0xA) ^ "key") >> 0x15

	print(encoded_str.format("list")) # "byte_array = [0x6b, 0x53, 0x21, 0xf9, 0xeb, 0xa1, 0x77, 0x35, 0xff, 0x59]"
	print(decoded_str) # "Pas$$w0rd!"

	
Callback Functions
------------------
Custom callback functions can be used to execute operations with the *run()* method. This is generally more efficient for longer operations, and is recommended for files. Using callback functions also gives you access to the "global" offset of a particular byte, as well as the option to write the results to a new file.

They must fit the following signature:

.. py:function:: callback_func(byte: int, offset: int)

   Return byte, altered or otherwise

Callback lambdas are dynamically generated and shown when using the CLI tool.

*Callback functions can be defined like regular functions or as lambdas.*

De-obfuscating a string using a callback function:

>>> import dynabyte
>>> decrypt = dynabyte.Array("\osb`pnarq-`a_v{t")
>>> decrypt.run(lambda byte, offset : (byte + 3) ^ 0x10)
>>> decrypt
Obfuscated string

