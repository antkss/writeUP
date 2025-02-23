#include <stdio.h>
int main(){
long int buff[10];
read(0,buff,32);
printf("this is the result: %u", strtoul(buff,NULL,0));

	return 0;
}
