Basic Usage
===========

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
>>> decrypt = dynabyte.load("\osb`pnarq-`a_v{t")
>>> decrypt.run(lambda byte, offset : (byte + 3) ^ 0x10)
>>> decrypt.printbytes(format="string")
Obfuscated string

Built-In Operations
-------------------
Built-in operation methods (*XOR*, *ADD*, *SUB*, *ROL*, *ROR*) can be used on both files and strings, the order of execution being left to right. 
*XOR* can also used to encode/decode against a key

Example: Encrypting a binary file w/ key 
----------------------------------------
>>> import dynabyte as db
>>> def encrypt(byte, offset):
        i = offset % len(key)
        return (byte ^ key[i]) + 0xc
>>> dfile = db.load(r"C:\Users\IEUser\suspicious.bin")
>>> dfile.XOR("Bada BING!").ADD(0xc)
