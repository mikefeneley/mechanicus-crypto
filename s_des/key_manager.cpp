#include "key_manager.h"


/*
 * Returns the users private key for encryption/decryption.
 * If a key does not already exist, a new one is created and 
 * stored 
 */
short get_key(const std::string & name)
{
    short key = -1;
    std::ifstream f(name.c_str());
    if(f.good())    
    {
        std::string key_string;
        f >> key;
    } else {
        srand(time(NULL));
        key = rand() % 512;
        std::ofstream f(name.c_str());
        f << key;
    }
    return key;
}
