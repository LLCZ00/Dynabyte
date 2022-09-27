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
    input_data: bytearray,
    format: "C, list, string, or None (default)" = None,
    delim: str = ", ") -> None:
    """Print bytes or bytearray in C-style array, Python list, or default format"""

    array_string = delim.join(hex(byte) for byte in input_data)
    if format == "C":
        print("unsigned char byte_array[] = {{ {} }};".format(array_string))
    elif format == "list":
        print("byte_array = [{}]".format(array_string))
    elif format == "string":
        print(input_data.decode())
    else:
        print(array_string)
        

def getbytearray(input_data: "str, list, bytes, or bytearray") -> bytearray:
    """Return bytearray from string, list, or bytes objects"""
    if type(input_data) is str:
        return bytearray([ord(c) for c in input_data])
    elif type(input_data) is bytearray:
        return input_data
    elif type(input_data) is list or type(input_data) is bytes:
        return bytearray(input_data)
    else:
        raise TypeError(input_data)


def getbytes(input_string: str, file: bool = False) -> bytes:
    """Return bytes of string object or from file"""
    if file:
        data = None
        with open(filepath, "rb") as fileobj:
            data = file.read(buffer)
        return data
    return bytes([ord(c) for c in input_string])        


def getsize(path, Print: bool = False) -> int:
    """Return size (int) of given file in bytes"""
    size = os.stat(path).st_size
    if Print:
        print("{}: {:,} bytes".format(os.path.basename(path), size))
    return size


def gethash(path, hash: str = "md5", Print: bool = False) -> str:
    """Return hash (str) of given file (Default: MD5)"""
    hash_obj = hashlib.new(hash)
    with open(path, "rb") as reader:
        chunk = reader.read(8192)
        while chunk:
            hash_obj.update(chunk)
            chunk = reader.read(8192)
    if Print:
        print("{}: {}".format(hash, hash_obj.hexdigest()))
    return hash_obj.hexdigest()


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
                    deviants.append("Offset {}: {} -> {}".format(hex(offset), hex(byte1), hex(byte2)))
                offset += 1
            chunk1 = file1.read(8192)
            chunk2 = file2.read(8192)
    if len(deviants) == 0:
        if verbose:
            print("No discrepancies found between {} and {}".format(name1, name2))
        return True
    else:
        if verbose:
            print("Errors found:")
            for line in deviants:
                print(line)
        return False


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
