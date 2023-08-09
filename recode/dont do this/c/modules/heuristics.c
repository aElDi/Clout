// heuristics.c

#include <stdbool.h>
#include <regex.h>
#include <stdio.h>

#include "scanner.h"

bool scan_file_heuristic(char* path) {
    // Check filename for suspicious patterns
    const char* pattern_filename = "(lock)|(key)|(decrypt)(or)?(.encrypted)?$";
    regex_t regex_filename;
    if (regcomp(&regex_filename, pattern_filename, REG_EXTENDED | REG_ICASE) != 0) {
        fprintf(stderr, "Could not compile regex %s\n", pattern_filename);
        return false;
    }
    if (regexec(&regex_filename, path, 0, NULL, 0) == 0) {
        regfree(&regex_filename);
        return true;
    }

    // Check file contents for suspicious patterns
    const char* pattern_contents = ".*(send bitcoin|pay up|ransom).*";
    regex_t regex_contents;
    if (regcomp(&regex_contents, pattern_contents, REG_EXTENDED | REG_ICASE) != 0) {
        fprintf(stderr, "Could not compile regex %s\n", pattern_contents);
        regfree(&regex_filename);
        return false;
    }
    FILE* fp = fopen(path, "r");
    if (fp) {
        char line[256];
        while (fgets(line, sizeof(line), fp)) {
            if (regexec(&regex_contents, line, 0, NULL, 0) == 0) {
                fclose(fp);
                regfree(&regex_filename);
                regfree(&regex_contents);
                return true;
            }
        }
        fclose(fp);
    }

    regfree(&regex_filename);
    regfree(&regex_contents);
    return false;
}