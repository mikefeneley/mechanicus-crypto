#ifndef _SIMPLE_DES
#define _SIMPLE_DES

#include "key_manager.h"

typedef struct _block {
        bool bits[12];
} block;

int key_transform(block *block_array, it_key *it);
void s1_lookup(bool *s1_in, bool *s1_out);
void s2_lookup(bool *s2_in, bool *s2_out);

#endif
