#
# Copyright (C) 2022 LLCZ00
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.  
#

""" 
dynabyte.utils

- Dynabytes utility/helper functions. 
- Also useful for general file IO.
"""

import os, hashlib


def RotateLeft(x, n):
    """Circular rotate shift x left by n bits"""
    return ((x << n % 8) & 255) | ((x & 255) >> (8 - (n % 8)))


def RotateRight(x, n):
    """Circular rotate shift x right by n bits"""
    return ((x & 255) >> (n % 8)) | (x << (8 - (n % 8)) & 255)
    

def printbytes( 
    input: bytearray,
    style: "C, list, string, or None (default)" = None,
    delim: str = ", ",
    end: str = "\n") -> None:
    """Print array of current instance in C-style array, Python list, or hex value (default) formats"""

    array_string = delim.join(hex(byte) for byte in input)
    try:
        style = style.lower()
    except AttributeError:
        pass
    
    if style == "c":
        print(f"unsigned char byte_array[] = {{ {array_string} }};", end=end)
    elif style == "list":
        print(f"byte_array = [{array_string}]", end=end)
    elif style == "string":
        try:
            print(input.decode(), end=end)
        except UnicodeDecodeError:
            print(f"(Could not decode)", end=end)
    else:
        print(array_string, end=end)
        

def getbytearray(input: "str, list, bytes, or bytearray") -> bytearray:
    """Return bytearray from string, list, or bytes objects"""
    if type(input) is str:
        return bytearray([ord(c) for c in input])
    elif type(input) is bytearray:
        return input
    elif type(input) is list or type(input) is bytes:
        return bytearray(input)
    else:
        raise TypeError(input)


def getfilebytes(path: str, buffer: int = -1) -> bytes:
    """Return all bytes from file. Beware hella large files"""
    data = None
    try:
        with open(filepath, "rb") as fileobj:
            data = file.read(buffer)
    except FileNotFoundError:
        pass
    return data      


def getfilesize(path: str, verbose: bool = False) -> int:
    """Return size (int) of given file in bytes"""
    size = os.stat(path).st_size
    if verbose:
        print(f"{os.path.basename(path)}: {size:,} bytes")
    return size


def getfilehash(path, hash: str = "sha256", verbose: bool = False) -> str:
    """Return hash (str) of given file (Default: SHA256)"""
    hash_obj = hashlib.new(hash)
    try:
        with open(path, "rb") as reader:
            chunk = reader.read(8192)
            while chunk:
                hash_obj.update(chunk)
                chunk = reader.read(8192)
    except FileNotFoundError:
        if verbose:
            print(f"File not found: '{path}'")
        return None
        
    if verbose:
        print(f"{os.path.basename(path)} - {hash}: {hash_obj.hexdigest()}")
    return hash_obj.hexdigest()


def comparefilehashes(*paths, hash: str = "sha256", verbose: bool = False):
    """Compare hashes of 2 or more files (Default: SHA256)"""
    hashes = []
    for path in paths:
        hashes.append(getfilehash(path, hash, verbose))
        
    match = all(x == hash[0] for x in hashes)
    if not match and verbose:
        print("Hashes do not match")
    elif match and verbose:
        print("Hashes match")
        
    return match
    

def comparefilebytes(filepath1: str, filepath2: str, verbose: bool = True) -> bool:
    """Compare the bytes of the two given files.     
    If verbose==True (default) results will be printed to the screen.
    Return: True = no error, False = errors found"""
    name1 = os.path.basename(filepath1)
    name2 = os.path.basename(filepath2)
    deviants = []
    offset = 0
    with open(filepath1, "rb") as file1, open(filepath2, "rb") as file2:
        chunk1 = file1.read(8192)
        chunk2 = file2.read(8192)
        while chunk1 and chunk2:
            for byte1, byte2 in zip(chunk1, chunk2):
                if byte1 != byte2:
                    deviants.append(f"Offset {hex(offset)}: {hex(byte1)} -> {hex(byte2)}")
                offset += 1
            chunk1 = file1.read(8192)
            chunk2 = file2.read(8192)
    if deviants:
        if verbose:
            print(f"{len(deviants)} errors found.")
        return deviants
    if verbose:
        print(f"No discrepancies found between {name1} and {name2}")
    return None
        

def deletefile(filepath: str) -> None:
    """Delete file at given path"""
    if os.path.exists(filepath):
        os.remove(filepath)

def delete_output(function):
    """Deletes the filepath returned by whatever function it decorates"""
    def wrapper(*args, **kwargs):
        deleteFile(function(*args, **kwargs))
    return wrapper


if __name__ == "__main__":
    pass
