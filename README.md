# Dynabyte
### _Simplifying Simple Byte Operations_
Dynabyte is a python module designed to streamline the process of de-obfuscating strings and files, allowing you to perform bit-wise operations on large amounts of data with as little code as possible.
## Basic Usage
See [*documentation*](https://google.com)

De-obfuscating a string:
```py
import dynabyte

decrypt = dynabyte.loadarray("\osb`pnarq-`a_v{t")
decrypt.run(lambda byte, offset : (byte + 3) ^ 0x10) # Callback function to perform on each byte
decrypt.printbytes(format="string") # Output: "Obfuscated string"
```
Encrypting a binary file w/ key 
```py
import dynabyte

key = dynabyte.getbytes("bada BING!")
def encrypt(byte, offset): # Callbacks can be lambdas or regular functions
    i = offset % len(key)
    return (byte ^ key[i]) + 0xc
dynabyte.loadfile(r"C:\Users\IEUser\suspicious.bin").run(encrypt, count=2) # Run file through encryption function twice
dynabyte.printbytes(key, format="C") # Output: "unsigned char byte_array[] = { 0x62, 0x61, 0x64, ... };"
```
## Installation

Install from PyPI
```
pip install dynabyte
```
## I/O Speed
Naturally, since dynabyte passes each byte through a callback function, the delay starts to become noticeable around 5MB or so. As of v1.0.0, dynabyte's base speed is around 4.4MB(mebibytes) per second. This is the speed of simply passing the bytes through a "No-op" function that just returns an unaltered byte. More operations, of course, result in lower speeds. 

Benchmark of 5MB file:
```
NOP:                 1.06s -> 4.43 MB/s
Add,Sub:             1.12s -> 4.19 MB/s
XOR:                 1.22s -> 3.85 MB/s
XOR/Sub,Add:         1.28s -> 3.67 MB/s
ROR,ROL              2.17s -> 2.17 MB/s
Sub,Add/ROL,ROR:     2.27s -> 2.07 MB/s
XOR/ROR,ROL:         2.34s -> 2.01 MB/s
XOR/ROR,ROL,Add,Sub: 2.40s -> 1.96 MB/s
```

However this is all usually inconsquential when working with data typically found during malware analysis, i.e. strings and extracted files/shellcode. If there happens to be a 50MB XOR'd file embedded within a malware sample, 12 seconds isn't really that bad of a wait.
## Known Issues & TODO
- Processing speed of larger files could possibly be improved. Things to try:
    - Migrating all file IO and byte processing into Cython
    - Switching to numpy arrays (instead of bytearrays) and integrating them with Cython
    - Rewriting file IO functionality in C and wrapping them
- Add support for common encryption schemes (AES) and alternative encodings (Base64)
