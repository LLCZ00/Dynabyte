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
dynabyte.core

- Classes providing the core functionality of Dynabyte
"""

import dynabyte.utils as utils


def load(
    input: "Input array (str, bytearray, list, or bytes) or file path",
    file: "Specify string as a filepath" = False):
    """Return instance of DynabyteArray or DynabyteFile"""
    if file:
        return DynabyteFile(input)
    return DynabyteArray(input)


class OpMixIn:
    """Mixin class for built-in bit-wise operation methods
    """
    buffersize = 8192
        
    def run(self, callback, *, output=None, count=1):
        """Execute operations defined in a callback function upon data. Gives access to offset.
        
        Must be overriden by subclass
        
        :param callback: Callback function: func(byte, offset) -> byte
        :param output: Output file path (optional)
        :type output: str
        :param count: Number of times to run array though callback function
        :type count: int
        """
        raise NotImplementedError
    
    def XOR(self, value=0, *, count=1):
        """XOR each byte of the current instance against 'value', 'count' times
        
        Providing a value of any type other than int will result in it being used as a key
        
        :param value: Value to XOR array against (int, str, list, bytes, or bytearray)
        :param count: Number of times to XOR array against value
        :type count: int
        """
        if type(value) is int:
            return self.run(callback=lambda x, y: x ^ value, count=count)
        else:
            key = utils.getbytearray(value)
            return self.run(callback=lambda x, y: x ^ key[y % len(key)], count=count)
        
    def SUB(self, value=0, *, count=1):
        """Subtract 'value' from each byte of the current instance, 'count' times
         
        :param value: Value to subtract from each byte of array
        :type value: int
        :param count: Number of times to subtract value from array
        :type count: int
        """
        return self.run(callback=lambda x, y: x - value, count=count)
        
    def ADD(self, value=0, *, count=1):
        """"Add 'value' to each byte of the current instance, 'count' times
        
        :param value: Value to add to each byte of array
        :type value: int
        :param count: Number of times to add value to array
        :type count: int
        """
        return self.run(callback=lambda x, y: x + value, count=count)
        
    def ROL(self, value=0, *, count=1):
        """Circular rotate shift left each byte of the current instance by 'value' bits, 'count' times
        
        :param value: Number of places to shift array
        :type value: int
        :param count: Number of times to run ROL
        :type count: int
        """
        return self.run(callback=lambda x, y: utils.RotateLeft(x, value), count=count)
        
    def ROR(self, value=0, *, count=1):
        """Circular rotate shift right each byte of the current instance by 'value' bits, 'count' times
        
        :param value: Number of places to shift array
        :type value: int
        :param count: Number of times to run ROR
        :type count: int
        """
        return self.run(callback=lambda x, y: utils.RotateRight(x, value), count=count)    


class DynabyteArray(OpMixIn):
    """Dynabyte class for interacting with arrays"""
    def __init__(self, input):
        self.array = utils.getbytearray(input)
    
    def __str__(self):
        return self.format()
    
    def format(self, style="string", delim= ", "):
        """Return string of instance's array data in given format.
        
        C-style array, Python list, delimited hex values,
        or string (default) formats.
        
        :param style: C, Python, string, or 'raw' (None) array format
        :type style: str
        :param delim: Delimiter between hex values (Default: ', ')
        :type delim: str        
        :rtype: str 
        """       
        try:
            style = style.lower()
        except AttributeError:
            pass
            
        data = delim.join(hex(byte) for byte in self.array)    
        if style == "c":
            data = f"unsigned char byte_array[] = {{ {data} }};"
        elif style == "list":
            data = f"byte_array = [{data}]"
        elif style == "string":
            try:
                data = self.array.decode()
            except:
                pass        
        return data
                
    def run(self, callback, *, output=None, count=1):
        """Execute operations defined in a callback function upon data. 
        
        Gives access to offset.
        
        :param callback: Callback function: func(byte, offset) -> byte
        :param output: Output file path (optional)
        :type output: str
        :param count: Number of times to run array though callback function
        :type count: int
        """
        for _ in range(count):
            callback_function = DynabyteCallback(callback)
            self.array = callback_function(self.array)
        if output:
            with open(output, 'wb') as file:
                file.write(self.array)
        self.array = bytearray(self.array)
        return self
        

class DynabyteFile(OpMixIn):
    """Dynabyte class for interacting with files"""
    def __init__(self, input):
        self.path = input
        
    def getsize(self, verbose: bool = False) -> int:
        """Return size of current DynabyteFile instance file in bytes"""
        return utils.getfilesize(self.path, verbose)

    def gethash(self, hash: str = "sha256", verbose: bool = False) -> str:
        """Return hash of current DynabyteFile instance file (Default: SHA256)"""
        return utils.getfilehash(self.path, hash, verbose)
        
    def delete(self):
        """Delete input file"""
        return utils.deletefile(self.path)
        
    def run(
        self,
        callback: "Callback function: func(byte, offset) -> byte",
        *,
        output: "Optional output file path" = None,
        count: "Number of times to run array though callback function" = 1) -> object:
        """Execute operations defined in a callback function upon data. Gives access to offset.
        Returns self, or instance created from output file"""
        
        input = self.path # Running count > 1 and outputting a file at the same time breaks if I don't do this
        for _ in range(count):
            callback_function = DynabyteCallback(callback)
            with DynabyteFileManager(input, output, self.buffersize) as file_manager:
                for chunk in file_manager: 
                    file_manager.write(callback_function(chunk))
            if output:
                input = output # On the 2nd cycle it'll continue reading from the original (not up to date) file
                output = None
        return self
    

class DynabyteFileManager:
    """Context manager for file objects, can be iterated over to retrieve buffer of file bytes.
    Handles the input/output of one or two files.
    If no output path is given, the input will be overwritten
    """
    start_position = 0    
    def __init__(self, input: str, output: str, buffersize: int): 
        self.input_file = input
        self.output_file = output
        self.buffersize = buffersize
        self.last_position = self.start_position      

    def write(self, chunk: bytes) -> None:
        """Write bytes to file"""
        self.writer.seek(self.last_position)
        self.writer.write(chunk)

    def __enter__(self):
        if self.output_file is None:
            self.reader = self.writer = open(self.input_file, "rb+")  # reader/writer will use the same file handle if no output given
        else:
            self.reader = open(self.input_file, "rb")
            self.writer = open(self.output_file, "wb")
        return self

    def __exit__(self, type, val, traceback):
        self.reader.close()
        self.writer.close()
           
    def __iter__(self):
        return self

    def __next__(self) -> bytes:
        self.last_position = self.reader.tell() 
        chunk = self.reader.read(self.buffersize)
        if self.reader is None or chunk == b"":
            raise StopIteration
        else:
            return chunk


class DynabyteCallback:
    """Callback function handler, runs bytes through given function."""
    def __init__(self, function):
        self.callback = function
        self.global_offset = 0
        
    def __call__(self, chunk: bytes) -> bytes:
        """Returns bytes after being processed through callback function"""
        chunk_length = len(chunk)
        buffer = bytearray(chunk_length)
        for chunk_offset, byte in enumerate(chunk):
            buffer[chunk_offset] = (self.callback(byte, self.global_offset) & 0xff)
            self.global_offset += 1
        return bytes(buffer)
        

if __name__ == "__main__":
    pass
