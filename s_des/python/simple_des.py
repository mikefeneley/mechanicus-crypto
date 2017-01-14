from key_manager import KeyManager
from ctypes import c_bool
from ctypes import c_char
from ctypes import c_int
from copy import copy


class SimpleDES:

    def __init__(self):
        self.block_template = c_bool * 12
        self.rounds = 5

    def encrypt_file(self, inp="unencrypted.txt", output="encrypted.txt"):
        block_holder = self.build_block_list(inp)
        encrypted_block = self.encrypt_block_list(block_holder, self.rounds)
        self.write_block_list(encrypted_block, output)

    def decrypt_file(self, inp="encrypted.txt", output="unencrypted.txt"):
        block_holder = self.build_block_list(inp)
        decrypted_block_list = self.decrypt_block_list(
            block_holder, self.rounds)
        self.write_block_list(decrypted_block_list, output)

    def build_block_list(self, filename):
        block = self.block_template()
        block_holder = []
        with open(filename, 'rb') as f:
            counter = 0
            while True:
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
                            block = self.block_template()
                            counter = 0
        return block_holder

    def write_block_list(self, block_list, filename):

        with open(filename, 'wb') as f:
            counter = 0
            char = 0
            for block in block_list:
                for bit in block:

                    char = char | (bit << counter)
                    counter += 1
                    if(counter == 8):
                        counter = 0
                        f.write(chr(char))
                        char = 0

    def encrypt_block_list(self, block_list, iterations):

        for idx, block in enumerate(block_list):
            block_list[idx] = self.encrypt_block(block, rounds=iterations)
        return block_list

    def encrypt_block(self, block, rounds):

        L = block[0:6]
        R = block[6:12]
        key_man = KeyManager()
        key_man.get_binary_key()

        for i in range(0, rounds):
            print("\n")
            print("ENCRYPT ROUND:", i)
            subkey = key_man.get_binary_subkey(i)
            print("L: ", L, "R: ", R)
            exp = self.expansion(R)
            print("Exp: ", exp[:])
            exp_subkey_xor = []
            for i in range(0, 8):
                val = exp[i] ^ subkey[i]
                exp_subkey_xor.append(val)
            print("Subkey", subkey[:])
            print("KEY XOR: ", exp_subkey_xor[:])

            s1_in = exp_subkey_xor[0:4]
            s2_in = exp_subkey_xor[4:8]

            s1_out = self.s1_lookup(s1_in)
            s2_out = self.s2_lookup(s2_in)
            s_out = s1_out + s2_out

            print("S1_IN:", s1_in, "S1_OUT", s1_out)
            print("S2_IN", s2_in, "S2_OUT", s2_out)
            print("S_OUT", s_out)
            new_r = []
            for i in range(0, 6):
                val = s_out[i] ^ L[i]
                new_r.append(val)

            new_l = R
            print(new_l, new_r)
            L = R
            R = new_r

        new_block = R + L
        print("FINAL", new_block)
        return new_block

    def decrypt_block_list(self, block_list, iterations):
        for idx, block in enumerate(block_list):
            block_list[idx] = self.decrypt_block(block, rounds=iterations)
        return block_list

    def decrypt_block(self, block, rounds):

        L = block[0:6]
        R = block[6:12]
        key_man = KeyManager()
        key_man.get_binary_key()

        for i in range(rounds, 0, -1):
            print ("I", i)
            print("\n")
            print("DECRYPT ROUND:", i)
            subkey = key_man.get_binary_subkey(i - 1)
            print("L: ", L, "R: ", R)
            exp = self.expansion(R)
            print("Exp: ", exp[:])
            exp_subkey_xor = []
            for i in range(0, 8):
                val = exp[i] ^ subkey[i]
                exp_subkey_xor.append(val)
            print("Subkey", subkey[:])
            print("KEY XOR: ", exp_subkey_xor[:])

            s1_in = exp_subkey_xor[0:4]
            s2_in = exp_subkey_xor[4:8]

            s1_out = self.s1_lookup(s1_in)
            s2_out = self.s2_lookup(s2_in)
            s_out = s1_out + s2_out

            print("S1_IN:", s1_in, "S1_OUT", s1_out)
            print("S2_IN", s2_in, "S2_OUT", s2_out)
            print("S_OUT", s_out)
            new_r = []
            for i in range(0, 6):
                val = s_out[i] ^ L[i]
                new_r.append(val)

            new_l = R
            print(new_l, new_r)
            L = R
            R = new_r

        new_block = R + L
        print("FINAL", new_block)
        return new_block

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
        index = 8 * s1_in[0] + 4 * s1_in[1] + 2 * s1_in[2] + 1 * s1_in[3]
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

        val = s1[index]
        return val

    def s2_lookup(self, s2_in):
        index = 8 * s2_in[0] + 4 * s2_in[1] + 2 * s2_in[2] + 1 * s2_in[3]

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
    DES.decrypt_file()
