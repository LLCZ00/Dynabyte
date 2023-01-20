#
# Copyright (C) 2023 LLCZ00
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
Tests for the functions in dynabyte.utils
"""
import unittest
from dynabyte import utils

# utils.getbytearray()

class TestUtilities(unittest.TestCase):
    
    def test_getbytearray_bytearray(self):
        barray = bytearray([1,2,3,4,5,6,7,8,9])
        self.assertEqual(utils.getbytearray(barray), barray)
        
    def test_getbytearray_str(self):
        string = "Test String 321 #@!"
        barray = bytearray(string.encode())
        self.assertEqual(utils.getbytearray(string), barray)
        
    def test_getbytearray_bytes(self):
        bytes_object = bytes([0x45, 0x1, 0x36, 0xAC, 255])
        barray = bytearray(bytes_object)
        self.assertEqual(utils.getbytearray(bytes_object), barray)
        
    def test_getbytearray_int(self):
        number = 14
        barray = bytearray([number])
        self.assertEqual(utils.getbytearray(number), barray)
        
    def test_getbytearray_none(self):
        self.assertEqual(utils.getbytearray(None), bytearray([]))
        
    def test_getbytearray_list(self):
        mylist = [12, "string", [0xff, 'c'], b"bytes"]
        barray = bytearray([0xc, 0x73, 0x74, 0x72, 0x69, 0x6e, 0x67, 0xff, 0x63, 0x62, 0x79, 0x74, 0x65, 0x73])
        self.assertEqual(utils.getbytearray(mylist), barray)
        
    def test_random_key(self):
        key = utils.random_key(length=5)
        self.assertEqual(len(key), 5)


if __name__ == "__main__":
    unittest.main()
