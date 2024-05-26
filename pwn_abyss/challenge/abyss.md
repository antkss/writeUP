# write up 
- vì khi read không thêm null byte khi nhập nên nếu nhập full biến buf thì biến buf sẽ nối với user và gây ra buff vì biến user sẽ được lấy từ biến buf qua các vòng lặp, vì thế nếu nối với user thì biến buf sẽ được kéo dài và cuối cùng overwrite được biến i
- vì biến i nằm cuối 
- thay đổi biến i thì nơi ghi dữ liệu của vòng lặp cũng đổi 
- chỉ cần thay đổi i trỏ vào đúng saved rip là có thể chuyển hướng qua hàm khác, hàm cần chuyển hướng là hàm read flag
```c
    char pass[MAX_ARG_SIZE] = {0};
    char user[MAX_ARG_SIZE] = {0};
    char buf[MAX_ARG_SIZE];
    int i;

    memset(buf, '\0', sizeof(buf));
    if (read(0, buf, sizeof(buf)) < 0)
        return;

    if (strncmp(buf, "USER ", 5))
        return;

    i = 5;
    while (buf[i] != '\0')
    {
        user[i - 5] = buf[i];
        i++;
    }
    user[i - 5] = '\0';

    memset(buf, '\0', sizeof(buf));
    if (read(0, buf, sizeof(buf)) < 0)
        return;

    if (strncmp(buf, "PASS ", 5))
        return;

    i = 5;
    while (buf[i] != '\0')
    {
        pass[i - 5] = buf[i];
        i++;
    }
    pass[i - 5] = '\0';

    if (!strcmp(VALID_USER, user) && !strcmp(VALID_PASS, pass))
    {
        logged_in = 1;
        puts("Successful login");
    }
}
```
