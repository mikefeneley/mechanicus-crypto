#include <iostream>
#include <cstdlib> 
#include <ctime>
int main(int argc, char * argv[])
{
    srand((unsigned)time(0));
    int i = rand();
    
    std::cout << i << "\n\n";
    
    
    if(argc < 2)
    {
        std::cout << "Not enough args";
    }
    
    for(int i = 0; i < argc; i++)
    {
        std::cout << argv[i];
    }
}
