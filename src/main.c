#include <windows.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char* argv[]) {
    if (argc < 3) {
        return 1;
    }

    if (strcmp(argv[1], "display") == 0) {
        if (strcmp(argv[2], "off") == 0) {
            SetDisplayConfig(0, NULL, 0, NULL, SDC_APPLY | SDC_TOPOLOGY_EXTERNAL);
        } else if (strcmp(argv[2], "on") == 0) {
            SetDisplayConfig(0, NULL, 0, NULL, SDC_APPLY | SDC_TOPOLOGY_INTERNAL);
        } else {
            return 1;
        }
    } else {
        return 1;
    }

    return 0;
}
