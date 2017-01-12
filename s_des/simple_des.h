#include "key_manager.h"

typedef struct _block {
        bool bits[12];
} block;


int key_transform(block *block_array, it_key *it);

