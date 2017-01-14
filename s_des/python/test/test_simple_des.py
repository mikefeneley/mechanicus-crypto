import sys
import unittest
from ctypes import c_bool
sys.path.append("../")

from simple_des import SimpleDES

class TestSimpleDES(unittest.TestCase):
    def setUp(self):
        self.des = SimpleDES()
        self.key_tempalte = c_bool * 9 
        self.subkey_template = c_bool * 8
        self.block_template = c_bool * 12

        self.subkey = self.subkey_template() 
    def tearDown(self):
        pass

    def test_encrypt_block(self):
        
        self.block = self.block_template()
        self.subkey = self.subkey_template()        
        self.block[0] = True
        self.block[1] = False
        self.block[2] = False
        self.block[3] = False
        self.block[4] = True
        self.block[5] = False
        self.block[6] = True
        self.block[7] = True
        self.block[8] = False
        self.block[9] = True
        self.block[10] = False
        self.block[11] = True

        self.subkey[0] = True
        self.subkey[1] = True
        self.subkey[2] = True 
        self.subkey[3] = False
        self.subkey[4] = False
        self.subkey[5] = False
        self.subkey[6] = True
        self.subkey[7] = True

        self.block = self.des.encrypt_block(self.block, 8)
        self.subkey[0] = True
        self.subkey[1] = True
        self.subkey[2] = False 
        self.subkey[3] = False
        self.subkey[4] = False
        self.subkey[5] = True
        self.subkey[6] = True
        self.subkey[7] = True
        print(self.block) 
        self.block = self.des.decrypt_block(self.block, 8)
    

if __name__ == '__main__':
    unittest.main()
