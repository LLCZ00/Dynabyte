# Dynabyte
### _Simplifying Byte Operations_
Dynabyte is a python module and CLI tool designed to streamline the process of de-obfuscating data, allowing you to perform bit-wise operations on strings or files with as little code as possible.
## Basic Usage
Dynabyte can be used as a command line tool, or imported as a module for finer control over data and operations.
### CLI
```
usage: dynabyte [-h] [-s INPUT] [-x INPUT] [-f INPUT] [-o OUTPUT] [--xor KEY] [--xor-hex KEY] [--order {xor,ops}]
                [--delim SEP] [--style {c,list,int}]
                [ops ...]
positional arguments:
  ops                   Additional operations to be performed on each input byte, executed from left to right (xor,
                        add, sub, rol, ror). All values interpreted as hex.
options:
  -h, --help            show this help message and exit
  -s INPUT, --string INPUT
                        Input string to perform operations on.
  -x INPUT, --hex-in INPUT
                        Input hex (comma seperated) to perform operations on.
  -f INPUT, --file INPUT
                        Input file to perform operation on.
  -o OUTPUT, --output OUTPUT
                        Output file.
  --xor KEY             Quick XOR; XOR input against given key (string).
  --xor-hex KEY         Quick XOR; XOR input against given key (comma seperated hex).
  --order {xor,ops}     Declare if Quick XOR or additional ops are executed first, if both options are being used.
                        (Default: xor)
  --delim SEP           Set output hex delimiter. (Default: ',')
  --style {c,list,int}  Set style to print output bytes. (Default: Comma deliminated hex)
Examples:
        dynabyte --string plaintext xor 56 sub 12
        dynabyte -f sus.bin -o sus.exe --xor 'password' add 0x12
        dynabyte --hex 0x1b,0x52,0xa,0x18,0x44,0x16,0x19,0x57 --xor k3y
```
Encoding/decoding a string:
```
$ dynabyte -s pa$$w0rd! --xor "mr.pib" sub 5 ror 3
Callback function:
lambda byte, offset: utils.RotateRight(((byte ^ key[offset % 6]) - 5), 3)
Output bytes:
0x3,0xc1,0xa0,0xe9,0x23,0xa9,0x43,0x22,0x41
Output string:
(Could not decode)
```
Any number of additional operations (*xor*, *add*, *sub*, *ror*, *rol*) can be added to the end of the command, to be performed on each byte sequentially from left to right. So to decode the string you just reverse the previous operations:
```
$ dynabyte --hex 0x3,0xc1,0xa0,0xe9,0x23,0xa9,0x43,0x22,0x41 --order ops --xor "mr.pib" rol 3 add 5
Callback function:
lambda byte, offset: ((utils.RotateLeft(byte, 3)) + 5) ^ key[offset % 6]
Output bytes:
0x70,0x61,0x24,0x24,0x77,0x30,0x72,0x64,0x21
Output string:
pa$$w0rd!
```
A dynabyte callback function (see below) is dynamically generated to perform the command, and can be acceptably copy/pasted into script using the dynabyte module, if one were so incline.
### Module
See [*documentation*](https://dynabyte.readthedocs.io/en/latest/)

Obfuscating and de-obfuscating a string:
```py
import dynabyte

obf_string = dynabyte.Array("Pas$$w0rd!")
obf_string.ROL(0x15).XOR("key").ADD(0xA) # Rotate left 0x15 bytes, xor against "key", add 0xA
print(obf_string) # "0x6b, 0x53, 0x21, 0xf9, 0xeb, 0xa1, 0x77, 0x35, 0xff, 0x59"

obf_string.SUB(0xA).XOR("key").ROR(0x15) # Perform operations in reverse
print(obf_string) # "Pas$$w0rd!"
```
This example can also be accomplished using typical binary operators:
```py
from dynabyte import Array

encoded_str = ((Array("Pas$$w0rd!") << 0x15) ^ "key") + 0xA	
decoded_str = ((Array(encoded_str) - 0xA) ^ "key") >> 0x15

print(encoded_str.format("list")) # "byte_array = [0x6b, 0x53, 0x21, 0xf9, 0xeb, 0xa1, 0x77, 0x35, 0xff, 0x59]"
print(decoded_str) # "Pas$$w0rd!"
```
Built-in operation methods (*XOR*, *ADD*, *SUB*, *ROL*, *ROR*) can be used on both files and strings, the order of execution being left to right. 

The built-in operations can also be used directly, without creating a *dynabyte* File or Array instance:
```py
from dynabyte.ops import *

string = "shmebulock"
encoded = XOR(SUB(ROL(string, 3), 12), 0xC)
decoded = ROR(ADD(XOR(encoded, 0xC), 12), 3)

print(encoded) # b'\x83;S\x13\x0b\x93[c\x03C'
print(decoded.decode()) # "shmebulock"
```
The functions in *dynabyte.ops* return the bytes of the processed input, unlike the dynabyte objects which return their own instance.

Custom callback functions can be used to execute operations with the *run()* method. This is generally more efficient for longer operations, and is recommended for files. Using callback functions also gives you access to the "global" offset of a particular byte, as well as the option to write the results to a new file.

Callback Signature:
```py
def callback(byte: bytes, offset: int) -> bytes:
    return byte
```
Encrypting/decrypting a file: 
```py
import dynabyte

key = b"bada BING!"
callback = lambda byte, offset: (byte ^ key[offset % len(key)]) + 0xc # Callbacks can be lambdas or regular functions
myfile = dynabyte.File(r"C:\Users\IEUser\suspicious.bin")
# Run file through callback function twice, encrypting file
myfile.run(callback, count=2) 
# Decrypt file by reversing the operations, output to file
myfile.run(lambda byte, offset: (byte - 0xc) ^ key[offset % len(key)], count=2, output="sus_copy.bin") 
```
## Installation

Install from PyPI
```
pip install dynabyte
```
## Known Issues & TODO
- Processing speed of larger files could possibly be improved. Things to try:
    - Migrating all file IO and byte processing into Cython
    - Switching to numpy arrays (instead of bytearrays) and integrating them with Cython
    - Rewriting file IO functionality in C and wrapping them
- Add support for common encryption schemes (AES) and alternative encodings (Base64)
- Remove utils.RotateLeft and utils.RotateRight, find workaround for this in arg parsing for CLI tool
