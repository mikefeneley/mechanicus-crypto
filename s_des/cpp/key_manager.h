#ifndef _KEY_MANAGER
#define _KEY_MANAGER

#include <sys/stat.h>
#include <iostream>
#include <unistd.h>
#include <string>
#include <iostream>
#include <fstream>
#include <time.h>
#include <stdlib.h>

typedef struct _full_key
{
    bool bits[9];
} full_key;

typedef struct _it_key 
{
    bool bits[8];
} it_key;


void get_key(const std::string &name, full_key * key);
void get_iteration_key(full_key *full, it_key *it, int iteration);

#endif
