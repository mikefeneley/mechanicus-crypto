#include "simple_des.h"
#include "key_manager.h"
#include <iostream>
#include <iostream>

int encrypt(const std::string filename)
{

    std::streampos size;
    char * memblock;  
    std::ifstream file(filename, std::ios::in);
     
    size = file.tellg();
    memblock = new char[size];
    
    file.seekg(0, std::ios::beg);
    file.read(memblock, 12);
    std::cout << memblock; 
}


int transform(short data, short key)
{

}


int main()
{

    std::string filename = "This";
    encrypt(filename); 
}
