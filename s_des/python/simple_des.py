from key_manager import KeyManager
from ctypes import c_bool
from ctypes import c_char
from ctypes import c_int
from copy import copy
class SimpleDES:

    def __init__(self):
        pass
    
    def encrypt_file(self, filename='encrypt.txt'):
        
        block_holder = []
        block_template = c_bool * 12
        block = block_template()
        with open(filename, 'rb') as f:
            counter = 0 
            while 1:
                byte_s = f.read(1)
                if not byte_s:
                    break
                else:
                    byte_s = c_int(ord(byte_s))
                
                    for i in range(0, 8):
                        val = c_bool(((byte_s.value >> i) & 1)) 
                        block[counter] = val

                        counter += 1
                        if(counter == 12):
                            block_holder.append(block)
                            block = block_template()
                            counter = 0 
        self.block_transform(block_holder)

    def block_transform(self, block_holder, iterations=1):
        
        key_man = KeyManager()
        key = key_man.get_binary_key()
        for i in range(0, iterations):

            for block in block_holder:
                print(block[:], "BLOCK")

                sub_key = key_man.get_binary_subkey(i)
                print(key[:], "KEY")
                print(sub_key[:], "SUB_KEY")
                self.transform(block, sub_key)
        
    def transform(self, block, subkey):
                
        L = block[0:6]
        R = block[6:12]
        print(L, R)
        exp = self.expansion(R)
        
        exp_subkey_xor = []
        for i in range(0, 8):
            val = exp[i] ^ subkey[i]
            exp_subkey_xor.append(val)
        
        s1_in = exp_subkey_xor[0:4]
        s2_in = exp_subkey_xor[4:8]
        
        s1_out = self.s1_lookup(s1_in)
        s2_out = self.s2_lookup(s2_in)
        s_out = s1_out + s2_out

        new_r = []
        for i in range(0, 6):
            val = s_out[i] ^ L[i]
            new_r.append(val)    
        new_l = R 
        
        new_block = new_l + new_r

    def expansion(self, block):
        expansion_temp = c_bool * 8
        expansion = expansion_temp()
        expansion[0] = block[0]
        expansion[1] = block[1]
        expansion[2] = block[3]
        expansion[3] = block[2]
        expansion[4] = block[3]
        expansion[5] = block[2]
        expansion[6] = block[4]
        expansion[7] = block[5]
        return expansion

    def s1_lookup(self, s1_in):
        index = 1 * s1_in[0] + 2 * s1_in[1] + 4 * s1_in[2] + 8 * s1_in[3]
       
        s1 = [
        [True, False, True],
        [False, True, False],
        [False, False, True],
        [True, True, False],
        [False, True, True],
        [True, False, False],
        [True, True, True],
        [False, False, False],
        [False, False, True],
        [True, False, False],
        [True, True, False],
        [False, True, False],
        [False, False, False],
        [True, True, True],
        [True, False, True],
        [False, True, True]
        ]
        return s1[index]
    
    def s2_lookup(self, s2_in):
        index = 1 * s2_in[0] + 2 * s2_in[1] + 4 * s2_in[2] + 8 * s2_in[3]

        s2 = [
        [True, False, False],
        [False, False, False],
        [True, True, False],        
        [True, False, True],
        [True, True, True],
        [False, False, True],
        [False, True, True],
        [False, True, False],
        [True, False, True],
        [False, True, True],
        [False, False, False],
        [True, True, True],
        [True, True, False],
        [False, True, False],
        [False, False, True],
        [True, False, False]
        ]

        return s2[index]

if __name__ == '__main__':
    DES = SimpleDES()
    DES.encrypt_file()
