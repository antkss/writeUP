#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <dlfcn.h>
char buff[0x500];
int main()
{
    printf("libc: %p\n",stdout);
    printf("stack: %p\n",__builtin_frame_address(0));
    printf("hello there\n");
    // read(0,buff,0x500);
    // stdout = (FILE*)buff;
    fwrite(buff,100,1,stdout);
    // puts(buff);
    return 0;
}
