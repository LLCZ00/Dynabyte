Basic Usage
===========

Callback Functions
------------------
The heart of Dynabyte, operations are performed on bytes from files or arrays by passing them through a user-defined callback function.

They must fit the following signature:

.. py:function:: callback_func(byte: int, offset: int)

   Return byte, altered or otherwise

*Callback functions can be defined like regular functions or as lambdas.*

Example: De-obfuscating a string
--------------------------------
>>> import dynabyte
>>> decrypt = dynabyte.loadarray("\osb`pnarq-`a_v{t")
>>> decrypt.run(lambda byte, offset : (byte + 3) ^ 0x10)
>>> decrypt.printbytes(format="string")
Obfuscated string

Example: Encrypting a binary file w/ key 
----------------------------------------
>>> import dynabyte
>>> key = dynabyte.getbytes("bada BING!")
>>> def encrypt(byte, offset):
        i = offset % len(key)
        return (byte ^ key[i]) + 0xc
>>> dynabyte.loadfile(r"C:\Users\IEUser\suspicious.bin").run(encrypt, count=2)
>>> dynabyte.printbytes(key, format="C")
unsigned char byte_array[] = { 0x62, 0x61, 0x64, ... };