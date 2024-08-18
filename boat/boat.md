# write up boat
- bài boat là bài sẽ cho chạy nhiều chương trình con ẩn với cùng 1 binary, và chương trình chính là chương trình sẽ có interface ở ngoài để tương tác
- chương trình parent sẽ có quyền gửi cho các chương trình child những đoạn tin mã hóa với 1 format data nhất định và child cũng có thể spam tin nhắn như vậy, nhưng bug xảy ra khi ta có thể khai thác thông qua oob và buffer trong chương trình
```c
  bytes_recv = slot_size[(char)msg->data[4]];
  send_bin_ack(bin_msg->boat_id, bytes_recv);
```
- tại đây sau khi tin nhắn được gửi tới thì các hàm sẽ parse ra để lấy thông tin, tuy nhiên tại đây msg->data[4] không được oob nên khi vào đây ta có thể leak được thông tin vì sau khi bytes được recv ở đây  thì nó sẽ gửi đi trả lại cho người gửi nên khi gửi tin cho boat 1031 là ip thì boat 1031 sẽ gửi lại nội dung trong bytes_recv, và lúc này sẽ có địa chỉ bị leak
- đây chính là hàm parse tin nhắn
```c
void __cdecl process_msg(ais_frame_t *msg)
{
  int type; // edx
  int v2; // [esp-8h] [ebp-10h]

  type = msg->type;
  if ( type == 8 )
  {
    if ( g_logging && g_my_id == 1031 )
      dprintf(g_logging_fd, (int)"Received binary broadcast message\n", v2);
    process_BDC_MSG(msg);
  }
  else
  {
    if ( msg->type > 8u )
      goto LABEL_18;
    if ( type == 7 )
    {
      log_BIN_UNC_ack(msg);
      return;
    }
    if ( msg->type > 7u )
      goto LABEL_18;
    if ( type == 1 )
    {
      process_POS_REPORT(msg);
      return;
    }
    if ( type == 6 )
    {
      if ( g_logging && g_my_id == 1031 )
        dprintf(g_logging_fd, (int)"Received binary address message\n", v2);
      process_BIN_UNC(msg);
    }
    else
    {
LABEL_18:
      if ( g_logging )
      {
        if ( g_my_id == 1031 )
          dprintf(g_logging_fd, (int)"Unknown message type %d\n", msg->type);
      }
    }
  }
}
```
- sau khi có libc và có mọi thứ tiếp theo là overwrite thông qua buffer 
```
void __cdecl handle_AES_FI_MSG(AIS_BIN_UNC_t *msg)
{
  char static_msg[90]; // [esp+Eh] [ebp-6Ah] BYREF
  int decrypted_bytes; // [esp+68h] [ebp-10h]
  AES_MSG_t *aes_data; // [esp+6Ch] [ebp-Ch]

  aes_data = (AES_MSG_t *)msg->data;
  decrypted_bytes = decrypt(
                      (unsigned __int8 *)msg->data,
                      slot_size[msg->slot_size],
                      boats[0].key,
                      boats[0].iv,
                      (unsigned __int8 *)static_msg);
  if ( g_logging )
  {
    if ( g_my_id == 1031 )
      dprintf(g_logging_fd, (int)"Decrypted AES MSG: %s\n", (int)static_msg);
  }
}
```
- đây chính là hàm bị buffer do có thể sửa slot_size chính là lentext lúc decrypt
```
int __cdecl decrypt(
        unsigned __int8 *ciphertext,
        int ciphertext_len,
        unsigned __int8 *key,
        unsigned __int8 *iv,
        unsigned __int8 *plaintext)
{
  int v5; // eax
  int v7; // [esp+4h] [ebp-14h] BYREF
  int v8; // [esp+8h] [ebp-10h]
  int v9; // [esp+Ch] [ebp-Ch]

  v9 = EVP_CIPHER_CTX_new();
  if ( !v9 )
    handleErrors();
  v5 = EVP_aes_256_cbc();
  if ( EVP_DecryptInit_ex(v9, v5, 0, key, iv) != 1 )
    handleErrors();
  if ( EVP_DecryptUpdate(v9, plaintext, &v7, ciphertext, ciphertext_len) != 1 )
    puts("DEC UPDATE ERR");
  v8 = v7;
  if ( EVP_DecryptFinal_ex(v9, &plaintext[v7], &v7) != 1 )
    puts("DEC FINAL ERR");
  v8 += v7;
  EVP_CIPHER_CTX_free(v9);
  return v8;
}
```
- vậy là chỉ cần truyền gói tin vào là có thể buffer được rip, nhưng vấn đề tin gửi vào là tin mã hóa nên ta cũng phải mã hóa nó theo kiểu EVP cipher
- hàm mã hóa cũng có thể có sẵn
- nhưng mà gói tin bắt được sử dụng key và iv của boat 1031 mã hóa nên để gửi đi được thì phải có key, iv
- sử dụng lại việc leak libc để leak được key và iv
- rồi tiếp theo mã hóa lại và gửi đi, khi giải mã ra hàm sẽ bị tràn và rip sẽ được setup
```assembly
00:0000│ esp 0xf75ff2b0 —▸ 0x5655c184 (boats+100) ◂— 'socat OPENSSL-LISTEN:4443,cert=bind.pem,verify=0'
01:0004│     0xf75ff2b4 —▸ 0xf7622f08 ◂— pop ebx
02:0008│     0xf75ff2b8 —▸ 0x5655bff4 (_GLOBAL_OFFSET_TABLE_) ◂— 0x6ee0
03:000c│     0xf75ff2bc —▸ 0x565562d0 (system@plt) ◂— jmp dword ptr [ebx + 0b4h]
04:0010│     0xf75ff2c0 —▸ 0x5655c184 (boats+100) ◂— 'socat OPENSSL-LISTEN:4443,cert=bind.pem,verify=0'
```
- setup thì sẽ setup thông qua reverse shell để lấy được shell  
