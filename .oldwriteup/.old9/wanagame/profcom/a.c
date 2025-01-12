#include <unistd.h>
#include <fcntl.h>
#include <stdio.h>
#include <string.h>

int main() {
    const char *data = "Hello, pwrite64 to stdout!\n";
    size_t data_len = strlen(data);
    off64_t offset = 10; // Offset will be ignored for standard output

    ssize_t written = pwrite64(STDOUT_FILENO, data, data_len, offset);
    if (written == -1) {
        perror("pwrite64");
        return 1;
    }

    printf("Wrote %zd bytes to stdout\n", written);
    return 0;
}
