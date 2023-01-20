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
Tests the methods in dynabyte.core.Array
"""
import unittest
import os
from dynabyte.core import Array
from dynabyte.utils import getbytearray

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

class TestArray(unittest.TestCase):
    def setUp(self):
        self.input_data = ["Be veeeery quiet,", 0x45, 0x2, 0x0, 'I', b"I'm huntin rabbits"]
        self.const_data = getbytearray(self.input_data)
                        
    def test_template(self):
        pass
        
    def test_operations(self):
        myarray = Array(self.input_data)
        # Encode
        myarray.pad("PAD", 32)
        myarray.RC4("PassW0rd!")
        myarray.reverse()
        myarray.XOR([0xDE, 0xAD, 0xBE, 0xEF])
        myarray.ROR(7)
        myarray.SUB(0x1A)
        
        # Decode
        myarray.ADD(0x1A).ROL(7).XOR([0xDE, 0xAD, 0xBE, 0xEF]).reverse().RC4("PassW0rd!").strip("PAD")
        
        self.assertEqual(self.const_data, myarray)
    
    def test_binary_operators(self):     
        encoded_str = ((Array(self.input_data).RC4("PassW0rd!") ^ "another_key") >> 7) - 0x1A
        decoded_str = (((Array(encoded_str) + 0x1A) << 7) ^ "another_key").RC4("PassW0rd!")       
        self.assertEqual(self.const_data, decoded_str)
        
    def test_write_read_file(self):
        myarray = Array(self.input_data)
        rw_file = os.path.join(DATA_DIR, "test_rw.txt")
        
        self.assertIsNotNone(myarray.writefile(rw_file))
        self.assertEqual(myarray, Array.fromfile(rw_file))
    
    

if __name__ == "__main__":
    unittest.main()
