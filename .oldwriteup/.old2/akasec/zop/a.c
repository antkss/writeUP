#include <stdio.h>
#include "pkzip.h"
int main(){
    int file = open("./lmaodfd", O_WRONLY | O_CREAT, 0644);
    printf("lmao, %d",file);
    return 0;
}
