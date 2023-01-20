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
Tests for the functions in dynabyte.operations
"""
import unittest
import dynabyte.operations as ops
from dynabyte.utils import getbytearray


class TestOperations(unittest.TestCase):
    def setUp(self):
        self.inputs = ["This is a string", b"bytes string",
                        123, [0x58, 0x59, 0x5A], ["mix", 12, 'of', b"stuff"],
                        bytes([1,2,3])]
    
    def test_rotate_byte(self):
        for byte in range(256):
            for rotation in range(8):
                rol_byte = ops.RotateLeft(byte, rotation)
                self.assertEqual(byte, ops.RotateRight(rol_byte, rotation))
            
    def test_rotate_array(self):
        for data in self.inputs:
            const_data = getbytearray(data)
            for rotation in range(8):
                rol_array = ops.ROL(data, rotation)
                self.assertEqual(const_data, ops.ROR(rol_array, rotation))
                
    def test_xor(self):
        for data in self.inputs:
            const_data = getbytearray(data)
            for key in range(256):
                xor_array = ops.XOR(data, key)
                self.assertEqual(const_data, ops.XOR(xor_array, key))
        
    def test_xor_key(self):
        xor_keys = [1, [0x15, "key", 13], bytes([9,8,7,6]), "XORKEY!"]
        for data in self.inputs:
            const_data = getbytearray(data)
            for xor_key in xor_keys:
                xor_array = ops.XOR(data, xor_key)
                self.assertEqual(const_data, ops.XOR(xor_array, xor_key))
        
    def test_sub_add(self):
        for data in self.inputs:
            const_data = getbytearray(data)
            for value in range(256):
                add_array = ops.ADD(data, value)
                self.assertEqual(const_data, ops.SUB(add_array, value))
   
    def test_rc4(self):
        rc4_keys = [1, [0x15, "key", 13], bytes([9,8,7,6]), "RC4#KEY!"]
        for data in self.inputs:
            const_data = getbytearray(data)
            for rc4_key in rc4_keys:
                rc4_array = ops.RC4(data, rc4_key)
                self.assertEqual(const_data, ops.RC4(rc4_array, rc4_key))
        
    def test_reverse(self):
        for data in self.inputs:
            const_data = getbytearray(data)
            reversed_array = ops.reverse(data)
            self.assertEqual(const_data, ops.reverse(reversed_array))
        
    def test_pad(self):
        for data in self.inputs:
            const_data = getbytearray(data)
            for size in range(1, 10):
                padded = ops.pad(data, 0, len(const_data)+size)
                self.assertEqual(len(const_data)+size, len(padded))
                
    
    
    
if __name__ == "__main__":
    unittest.main()
