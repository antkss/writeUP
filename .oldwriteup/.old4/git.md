# write up git 
- mô tả về bài như sau: bài sẽ cho ta nhập command, các command sẽ sử dụng github api để quản lý repos trong github
- bug sẽ nằm chủ yếu ở hàm changedir và hàm readfile, 2 hàm này được call khi sử dụng command cd và command cat
### changedir 
- bug của hàm ở chỗ khi ta changedir, chương trình sẽ chứa đường dẫn ta cd, đường dẫn sẽ được cộng dồn khi ta cd nhiều lần, nếu ta cd 1 đường dẫn ngắn thì không sao, nhưng nếu cd quá nhiều thì sẽ gây ra buffer overflow vì việc cộng dồn đó
```c
        REPODIR[strlens(REPODIR)] = '/';
        v2 = strlens(REPODIR);
        strcpy(&REPODIR[v2], command);
```
- đường dẫn được chứa trong REPODIR, là biến global, khi cd lại lần nữa thì đường dẫn cũ vẫn còn nên chương trình sẽ tính len của đường dẫn cũ đã được cộng dồn và sau đó sẽ lấy địa chỉ ghi là địa chỉ tại index =len đó, nếu cd nhiều lần 1 đường dẫn hoặc làm cho đường dẫn truyền vào có độ dài lớn thì chương trình sẽ bị buffer sau khi sprintf để concat đường dẫn vào url của api
```c
   sprintf(s, "/repos/%s/contents%s", &REPONAME, REPODIR);
```
- đường dẫn có thể là đường dẫn không tồn tại vì không có check trước đó
### readfile
- ngoài ra việc leak thì hơi gacha, nhưng mà bug thì có thể thấy rằng ở hàm readfile khi chạy lệnh cat, hàm sẽ gửi request tới api thông qua curl và return về nội dung,
- 
```c
int __fastcall readfile(const char *command)
{
  char s[672]; // [rsp+10h] [rbp-2C0h] BYREF
  jsons *structa; // [rsp+2B0h] [rbp-20h]
  char **curl_return; // [rsp+2B8h] [rbp-18h]
  jsons *child; // [rsp+2C0h] [rbp-10h]
  char *valuestring; // [rsp+2C8h] [rbp-8h]

  if ( !LOBYTE(TOKEN[0]) )
    return puts("Token is null");
  if ( !LOBYTE(REPONAME[0]) )
    return puts("Repo name is null");
  snprintf(s, 672uLL, "/repos/%s/contents%s/%s", (const char *)REPONAME, (const char *)REPODIR, command);
  curl_return = (char **)curl_git(s);
  if ( !*curl_return )
    return puts("Request timeout");
  structa = (jsons *)cJSON_Parse(*curl_return);
  if ( (unsigned int)cJSON_IsArray(structa) || !strcmp(structa->child->string, "message") )
    return puts("Invalid file");
  child = structa->child;
  do
  {
    if ( !strcmp(child->string, "download_url") )
      valuestring = strdup(child->valuestring);
    child = child->next;
  }
  while ( child );
  curl_return = (char **)curl((__int64)valuestring);
  puts(*curl_return);
  return cJSON_Delete();
}
```
- tuy nhiên khi trả về nội dung thì nội dung sẽ không thêm null bytes ở cuối và bỏ vào vùng heap, do đó địa chỉ có thể sẽ bị leak từ đó
- khi gửi request đi thì curl sẽ trả về từ curl-callback, ở dưới vùng heap sẽ có những chunk có kích thước lớn mà trước đó các hàm trong các thư viện sử dụng sẽ để lại các địa chỉ arena, do đó khi vào hàm curl-callback thì địa chỉ sẽ nằm ở các chunk khác nhau ở dưới, do đó để leak đc thì cần phải realloc 1 kích thước sao cho nó chạm tới 1 địa chỉ cũ nào đó ở trên vùng heap
