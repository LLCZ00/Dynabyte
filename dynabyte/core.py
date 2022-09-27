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

- Functions and classes providing the main functionality of Dynabyte
- Classes are meant to be initialized through loadfile and loadarray
"""

import dynabyte.utils as utils


def loadfile(
    path: "Input file path",
    output: "Optional output file path" = None,
    buffersize: int = 8192):
    """Return instance of DynabyteFile, for performing actions on files"""
    return DynabyteFile(path, output, buffersize)


def loadarray(input_data: "Input byte array (str, bytearray, list, or bytes)"):
    """Return instance of DynabyteArray, for performing actions on arrays (strings, bytes)."""
    return DynabyteArray(utils.getbytearray(input_data))


""" Core Dynabyte Classes """

class DynabyteArray:
    """Dynabyte class for interacting with arrays"""

    def __init__(self, inputarray: bytearray):
        self.array = inputarray
        
    def printbytes(
        self,
        format: "C, Python, string, or 'raw' array format" = None,
        delim: "Delimiter between values" = ", ") -> None:
        """Print array of current instance in C-style array, Python list, or default formats"""
        utils.printbytes(self.array, format, delim)
        
    def run(
        self,
        callback: "Callback function: func(byte, offset) -> byte",
        count: "Number of times to run array though callback function" = 1):
        """Method for executing operations (defined in callback function) upon array data"""

        for _ in range(count):
            callback_function = DynabyteCallback(callback)
            self.array = callback_function(self.array)
        self.array = bytearray(self.array)
        return self    


class DynabyteFile:
    """Dynabyte class for interacting with files"""
    def __init__(self, path: str, output: str, buffersize: int):
        self.path = path
        self.output_path = output
        self.buffersize = buffersize
        
    def comparetofile(self, filepath: str, verbose: bool = True) -> bool:
        """Compare bytes of current DynabyteFile instance file to those of the given file.        
        If verbose==True (default) results will be printed to the screen.
        Return: True = no error, False = errors found.
        """
        return utils.comparefilebytes(self.path, filepath, verbose)

    def getsize(self, Print: bool = False) -> int:
        """Return size of current DynabyteFile instance file in bytes"""
        return utils.getsize(self.path, Print)

    def gethash(self, hash: str = "md5", Print: bool = False) -> str:
        """Return hash of current DynabyteFile instance file (Default: MD5)"""
        return utils.gethash(self.path, hash, Print)
        
    def run(
        self,
        callback: "Callback function: func(byte, offset) -> byte",
        *,
        output: "Optional output file path" = None,
        count: "Number of times to run array though callback function" = 1) -> object:
        """Method for executing operations (defined in callback function) upon file data.
        Returns self, or instance created from output file"""

        if output is not None:
            self.output_path = output # Change output path if new one is given when calling run             
        written_path = None # To be assigned the filepath of whatever file gets written to (the input file or a new file)        
        
        for _ in range(count):
            callback_function = DynabyteCallback(callback) # DynabyteCallback class (cython_extensions/callback.pyx) handles chunks  
            with DynabyteFileHandler(self.path, self.output_path, self.buffersize) as file_manager:
                for chunk in file_manager: 
                    file_manager.write(callback_function(chunk))
                written_path = file_manager.outputpath
        if written_path == self.path:
            return self
        else:
            return DynabyteFile(written_path, None, buffersize=self.buffersize) # Return new instance if bytes written to new file


class DynabyteCallback:
    """Callback function handler, runs bytes through given function."""
    def __init__(self, function):
        self.offset = 0
        self.callback = function
        
    def __call__(self, chunk: bytes) -> bytes:
        """Returns bytes after being processed through callback function"""
        chunk_length = len(chunk)
        buffer = bytearray(chunk_length)
        for chunk_offset, byte in enumerate(chunk):
            buffer[chunk_offset] = (self.callback(byte, self.offset) & 0xff)
            self.offset += 1
        return bytes(buffer)
    

class DynabyteFileHandler:
    """Context manager for file objects, can be iterated over to retrieve buffer of file bytes.
    Handles the input/output of one or two files.
    If no output path is given, the input will be overwritten
    """
    start_position = 0
    
    def __init__(self, path: str, output: str, buffersize: int):  # 8kb by default
        self.path = path
        self.outputpath = output
        self.buffersize = buffersize
        self.last_position = self.start_position

    def write(self, chunk: bytes) -> None:
        """Write bytes to file"""
        self.writer.seek(self.last_position)
        self.writer.write(chunk)

    def __enter__(self):
        if self.outputpath is None:
            self.reader = self.writer = open(
                self.path, "rb+"
            )  # reader and writer will use the same file handle if no output given
            self.outputpath = self.path
        else:
            self.reader = open(self.path, "rb")
            self.writer = open(self.outputpath, "wb")
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


if __name__ == "__main__":
    pass
