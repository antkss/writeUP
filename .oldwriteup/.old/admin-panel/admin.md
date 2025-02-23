# write up admin-panel
- với bài này dựa theo source code thì em có thể thấy rằng bài có buff khi scanf password
```c

	char username[16];
	char password[24];
	char status[24] = "Login Successful!\n";

	puts("Secure Login:");
	puts("Enter username of length 16:");
	scanf("%16s", username);
	puts("Enter password of length 24:");
	scanf("%44s", password);
```
và sau khi overwrite được status thì em có thể thông qua 
```c
strcpy(status, "Login failed!\n");
```
để dùng format string 
```c
	printf(status);
```
chính vì vậy có thể leak địa chỉ và canary, sau khi hoàn thành thì em có thể thông qua buff
```c
	int choice = 0;
	char report[64];
```
```c
scanf("%128s", report);
```

để overwrite save rip, sau khi chạy script thì có thể lấy được shell
