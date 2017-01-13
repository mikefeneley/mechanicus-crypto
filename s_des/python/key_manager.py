import random
import os
from ctypes import c_short
from ctypes import c_bool

class KeyManager:

    def __init__(self):
        self.key_filename = "key.txt"
    
    def get_key(self):
        if os.path.exists(self.key_filename):
            key_file = open(self.key_filename, 'r')
            self.key = int(key_file.read())
            self.key = self.key  
        else:
            self.key = random.randint(0, 511)
            key_file = open(self.key_filename, 'w')
            key_file.write(self.key)
    
    def get_binary_key(self):
        self.get_key()
        self.binary_key_class = c_bool * 9 
        self.binary_key = self.binary_key_class()
        
        key = self.key
        counter = 0
        while(key > 0):
            remainder = key % 2
            key = key / 2
            self.binary_key[counter] = remainder
            counter += 1
        return self.binary_key    
    def get_binary_subkey(self, iteration):
        self.get_binary_key()
        iteration = iteration % 9 
        
        self.binary_subkey_class = c_bool * 8
        self.binary_subkey = self.binary_subkey_class()
       
        #print(self.key, "KEY", iteration, "ITERATION")
        
        for i in range(0, 8):
            index = (i + iteration) % 9
            self.binary_subkey[i] = self.binary_key[index]
        #print(self.key, "KEY", self.binary_key[:], "BINARY", iteration, "ITERATION", self.binary_subkey[:])
        return self.binary_subkey

if __name__ == '__main__':
    manager = KeyManager()
    manager.get_key()
    manager.get_binary_key()
    manager.get_binary_subkey(0)
    manager.get_binary_subkey(1)
    manager.get_binary_subkey(2)
