
# write up baby ..
```c
   printf("\nYour pram has been created! Give it a name: ");
    //buffer overflow! user can pop shell directly from here
    gets(buf);
    printf("\nNew pram %s of size %s has been created!\n", buf, size);
    return 0;
```
- có buff 
```c
int sub_15210123() {
    execve("/bin/sh", 0, 0);
}

```
- và hàm chạy shell

tính offset và ghi đè là ok :
