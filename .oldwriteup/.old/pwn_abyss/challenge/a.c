#include <string.h>
#include <stdio.h>
#include <unistd.h>
int main(){
    char buff[512] = "hello\0";
    char buf[64] = "hello world\0";
    if(strcmp(buff,buf) == 0){
	printf("flag.txt\n");
    }
    return 0;
}
