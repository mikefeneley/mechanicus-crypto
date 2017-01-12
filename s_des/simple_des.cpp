#include "simple_des.h"
#include "key_manager.h"
#include <iostream>
#include <vector>


int print_blocks(block *block_array, int num_blocks)
{

    int k = 0;
    for(int i = 0; i < num_blocks; i++)
    {
        
        for(int j = 0; j < 12; j++)
        {
            if(k % 8 == 0) {
                std::cout << " ";
            }
            std::cout << block_array[i].bits[j];
            k++;
        }
    }   
}


int encrypt(const std::string filename, full_key *full)
{

    std::streampos size;
    std::ifstream file(filename, std::ios::binary);
        
    file.seekg(0, file.end);
    int length = file.tellg();
    file.seekg(0, file.beg);


    int num_bits = length * 8;
    int num_blocks = num_bits / 12;

    if(num_bits % 12) {
        num_blocks++;
    }

    block *block_array = new block[num_blocks];


    char data;
    int cur_block = 0;
    int cur_bit = 0;
    while(file.read(&data, 1)) {
        for(int i = 0; i < 8; i++)
        {
//            std::cout << "I:" << i << " Data >> i :" << (data >> i) << " ((data >> i) & 1): " << ((data >> i) & 1) << "\n";
            bool bit_val = ((data >> i) & 1);        
            block_array[cur_block].bits[cur_bit] = bit_val;
            
            if(++cur_bit == 12) {
                cur_bit = 0;
                cur_block++;
            } 
        }
    }
    
    int num_iterations = 1;
    for(int i = 0; i < num_iterations; i++)
    {
    
        it_key it;
        get_iteration_key(full, &it, i);
        key_transform(block_array, &it);    
        
     }
    

}


int key_transform(block *block_array, it_key *it)
{


    bool R[6];

    for(int i = 0; i < 6; i++)
    {
        R[i] = block_array[0].bits[i+6];
    }

   
    bool Holder[8];
    Holder[0] = R[0];
    Holder[1] = R[1];
    Holder[2] = R[3];
    Holder[3] = R[2];
    Holder[4] = R[3];
    Holder[5] = R[2];
    Holder[6] = R[4];
    Holder[7] = R[5];

    for(int i = 0; i < 8; i++)
    {
        Holder[i]  = Holder[i] ^ it->bits[i];
    }
   
    bool s1_input[4];
    bool s2_input[4]; 

    for(int i = 0; i < 3; i++)
    {
        s1_input[i] = Holder[i];
        s2_input[i] = Holder[i + 4];
    }
     
    return 0;
}

int main()
{

    const std::string key_filename = "key.txt";
    full_key key;
    get_key(key_filename, &key);
    encrypt(key_filename, &key); 
}
