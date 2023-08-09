// scanner.h

#ifndef SCANNER_H
#define SCANNER_H

#include <stdbool.h>

typedef struct _scanner {
    char* name;
    void* handle;
    bool (*scan_file)(char*);
} scanner_t;

void* load_scanner(char* path);
scanner_t* init_scanner(void* handle, char* scanner_name);
void free_scanner(scanner_t* scanner);
void files_in_dir(char* directory, char** inputs, int* cnt);
void process_file(char* path, scanner_t** scanners, int num_scanners);
bool scan_file_heuristic(char* path); // This line added to header file

#endif