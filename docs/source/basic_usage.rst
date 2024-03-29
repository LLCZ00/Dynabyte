Basic Usage
===========

Classes and Built-in Operations
-------------------------------
Dynabyte provides the *File* and *Array* classes, which share a number of built-in methods for performing operations on arrays/strings/bytes/integers or files, respectively. These built-in methods can also be used individually as standalone functions. Details on all built-in operations can be found in the Core/Classes section of the documentation.

.. code-block:: python

	import dynabyte

	obf_string = dynabyte.Array("Be veeeery quiet, I'm huntin rabbits")

	obf_string.RC4("PassW0rd!") # Operations are executed from left to right when chained
	obf_string.ROR(7)
	obf_string.XOR(["xor", 0xAB, 0x2, 'k', 'e', 'y']) # List inputs can be a mix of any valid input type
	obf_string.SUB(0x1A)
	print(obf_string) # "(Jumbled up string that I can't paste here)"

	# Perform previous operations in reverse (executed left to right)
	obf_string.ADD(0x1A).XOR(["xor", 0xAB, 0x2, 'k', 'e', 'y']).ROL(7).RC4("PassW0rd!") 
	print(obf_string) # "Be veeeery quiet, I'm huntin rabbits"


Typical binary operators can be used in place of *XOR*, *ADD*, *SUB*, *ROL*, and *ROR*:


.. code-block:: python

	from dynabyte import Array

	encoded_str = ((Array("Pas$$w0rd!").RC4("rc4_key") ^ "xor_key") >> 3) - 0xB
	decoded_str = (((Array(encoded_str) + 0xB) << 3) ^ "xor_key").RC4("rc4_key") # Array can accept other dynabyte Arrays

	print(list(encoded_str)) # "[129, 163, 101, 60, 61, 55, 241, 196, 46, 61]"
	print(decoded_str) # "Pas$$w0rd!"


As shown in the previous example, Array objects will decode their data from bytes to a string when printed or passed to str(). They're also iterable, and can be converted using bytes() or list() functions. For copy/pasting convenience, Arrays can be passed to the format() function to return a Python list, C-style array, or string of raw delimited values. File objects simply return their filepath when printed.


.. code-block:: python

	from dynabyte import Array

	mystr = Array("Jambalaya", encoding="UTF-16LE") # Set alternate encoding

	print(mystr) # 'Jambalaya'
	print(format(mystr, "list")) # 'byte_array = [0x4a, 0x0, 0x61, ... 0x0, 0x61, 0x0]'
	print(format(mystr, "c")) # 'unsigned char byte_array[] = { 0x4a, 0x0, 0x61, ... 0x0, 0x61, 0x0 };'

	mystr.delim = " " # Default: ", "
	mystr.hex = False # Print values as base10 instead of base16
	print(format(mystr)) # '74 0 97 0 109 0 98 0 97 0 108 0 97 0 121 0 97 0'


The built-in operations can also be used directly on string, integer, byte, and bytearray objects without creating an *Array* instance. The standalone functions return bytes objects, and are slighly more efficient than calling the methods an an *Array* object (possibly at the cost of some readability).


.. code-block:: python

	from dynabyte.operations import *

	string = "shmebulock"
	encoded = XOR(SUB(ROL(string, 3), 12), 0xC)
	decoded = ROR(ADD(XOR(encoded, 0xC), 12), 3)

	print(encoded) # b'\x83;S\x13\x0b\x93[c\x03C'
	print(decoded.decode()) # "shmebulock"


Reference the Core/Classes section of the documentation for more information on the built-in functions, as well as methods unique to *Array* and *File* objects.

	
Callback Functions
------------------
Using the *run()* method, callback functions can be used to execute custom operations on the data of *Array* and *File* objects. This is generally more efficient for longer operations, and is recommended for files. There are two "types" of callback functions, *full* and *offset*.


FullCallback signature:

.. py:function:: FullCallback(data: bytes) -> bytes

   Return data


FullCallback functions (the default type) accept and return all the input data (in bytes) at once, giving the function complete control over the whole data set. File objects read data from the input file, and subsequently pass it to the callback function, in chunks determined by the buffersize, so be aware of that if working with files greater than 8192 bytes. The buffersize can adjusted as needed when initializing the *File* object, or *getbytes()* can be called to create an *Array* object with the file's data.


OffsetCallback signature:

.. py:function:: OffsetCallback(byte: int, offset: int) -> int

   Return byte

OffsetCallback functions accept and return one byte at a time, and provides the byte's within the entirety of the data. Offset callback functions are given to a wrapper class which handles converting and 'normalizing' the bytes, which sometimes need to be "AND 0xff'd" to avoid encoding/decoding errors. Pass cb_type='offset' to *run()* to indicate an OffsetCallback.


Encrypting/decrypting a file using an offset callback function:

.. code-block:: python

	import dynabyte

	myfile = dynabyte.File(r"C:\Users\IEUser\suspicious.bin")
	
	key = b"bada BING!"
	callback = lambda byte, offset: (byte ^ key[offset % len(key)]) + 0xc # Callbacks can be lambdas or regular functions
	
	# Run file through callback function twice, encrypting file
	myfile.run(callback, cb_type='offset', count=2) # Run data through callback twice
	
	# Decrypt file by reversing the operations, output to file
	myfile.run(lambda byte, offset: (byte - 0xc) ^ key[offset % len(key)], count=2, cb_type='offset', output="sus_copy.bin")



	
