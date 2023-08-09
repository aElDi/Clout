#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <sys/stat.h>
#include <windows.h>

typedef struct _scanner scanner_t;

struct _scanner
{
    char *name;
    HMODULE handle;
    char *(*scan_file)(char *);
};

void *load_scanner(char *path)
{
    HMODULE handle = LoadLibrary(path);
    if (handle == NULL)
    {
        fprintf(stderr, "LoadLibrary() failed: %d\n", GetLastError());
        exit(1);
    }
    return handle;
}

scanner_t *init_scanner(HMODULE handle, char *scanner_name)
{
    scanner_t *scanner = malloc(sizeof(scanner_t));
    scanner->name = strdup(scanner_name);
    scanner->handle = handle;
    scanner->scan_file = (char *(*)(char *))GetProcAddress(handle, "scan_file");
    if (scanner->scan_file == NULL)
    {
        fprintf(stderr, "GetProcAddress() failed: %d\n", GetLastError());
        exit(1);
    }
    return scanner;
}

void free_scanner(scanner_t *scanner)
{
    FreeLibrary(scanner->handle);
    free(scanner->name);
    free(scanner);
}

void files_in_dir(char *directory, char **inputs, int *cnt)
{
    struct dirent *entry;
    DIR *dir;
    char path[256];

    if ((dir = opendir(directory)) != NULL)
    {
        while ((entry = readdir(dir)) != NULL)
        {
            sprintf(path, "%s\\%s", directory, entry->d_name);

            DWORD attrs = GetFileAttributes(path);
            if (attrs == INVALID_FILE_ATTRIBUTES)
                continue;
            int is_directory = attrs & FILE_ATTRIBUTE_DIRECTORY;

            if (is_directory)
            {
                if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0)
                    continue;
                files_in_dir(path, inputs, cnt);
            }
            else
            {
                inputs[(*cnt)++] = strdup(path);
            }
        }
        closedir(dir);
    }
}

void process_file(char *path, scanner_t **scanners, int num_scanners)
{
    for (int i = 0; i < num_scanners; i++)
    {
        scanner_t *scanner = scanners[i];
        char *result = scanner->scan_file(path);
        if (result[0])
        {
            printf("[Virus detected] Path: %s, Scanner: %s, Data: %s\n", path, scanner->name, result + 1);
        }
    }
}

int main()
{
    const char *directory_str = "[Input] Enter directory to scan: ";
    char directory[256];
    printf("%s", directory_str);
    fgets(directory, 256, stdin);
    int n = strlen(directory) - 1;
    if (directory[n] == '\n')
        directory[n] = '\0';

    int max_files = 256;
    char **inputs = malloc(max_files * sizeof(char *));
    int num_files = 0;

    files_in_dir(directory, inputs, &num_files);

    printf("[Info] Scanners:\n");
    scanner_t **scanners = malloc(max_files * sizeof(scanner_t *));
    int num_scanners = 0;

    char dir_sc_path[256];
    sprintf(dir_sc_path, "%s\\modules", directory);
    DIR *dir_sc = opendir(dir_sc_path);
    struct dirent *entry_sc;
    while ((entry_sc = readdir(dir_sc)) != NULL)
    {
        char *name = entry_sc->d_name;
        int n = strlen(name) - 3;
        if (strcmp(name + n, ".dll") != 0)
            continue;
        char path_sc[256];
        sprintf(path_sc, "%s\\%s", dir_sc_path, name);
        void *handle = load_scanner(path_sc);
        scanner_t *scanner = init_scanner(handle, name);
        scanners[num_scanners++] = scanner;
        printf("[Info] Module imported: %s\n", scanner->name);
    }
    closedir(dir_sc);

    printf("\n");

    for (int i = 0; i < num_files; i++)
    {
        char *path = inputs[i];
        process_file(path, scanners, num_scanners);
        free(path);
    }

    for (int i = 0; i < num_scanners; i++)
    {
        free_scanner(scanners[i]);
    }
    free(scanners);
    free(inputs);

    return 0;

}