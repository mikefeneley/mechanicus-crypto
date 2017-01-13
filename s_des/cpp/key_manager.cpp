#include "key_manager.h"

/*
 * Returns the users private key for encryption/decryption.
 * If a key does not already exist, a new one is created and 
 * stored 
 */
void get_key(const std::string &name, full_key *key)
{
    short tmp_key = -1;
    std::ifstream f(name.c_str());
    if(f.good())
    {
        std::string key_string;
        f >> tmp_key;
    } else {
        srand(time(NULL));
        tmp_key = rand() % 512;
        std::ofstream f(name.c_str());
        f << tmp_key;
    }
    
    int pos = 0;

    while(tmp_key > 0)  {
    
        bool remainder = tmp_key % 2;
        tmp_key /=2;
        std::cout << remainder << "\n"; 
        key->bits[pos] = remainder; 
        pos++;
    }
    return;
}

void get_iteration_key(full_key *full, it_key *it, int iteration)
{
    iteration = iteration % 9;

    for(int i = 0; i < 8; i++)
    {
        int index = (iteration + i) % 8;
        
        it->bits[i] = full->bits[index];    
    }

    for(int i = 0; i < 8; i++)
    {
        std::cout << it->bits[i];
    }
}
