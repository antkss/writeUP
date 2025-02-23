# write up yapping
- bài này sử dụng vòng lặp for để read vào stack, nhưng mà đồng thời đi hơi quá nên nó overwrite được cái i trong vòng lặp for nên có thể sửa i để nó nhảy xuống saved rip, vì chỉ có 1 lần cuối cùng để ghi nên ta sẽ nhảy lên saved rip của hàm read hiện tại để có thể ghi vì hàm read nằm trên so với cái biến buff được read, nên ta có thể rop được nhiều hơn 
```c
00401236  4801c6             add     rsi {buff}, rax
```
- đây là lý do vì sao i có thể âm
- bài có hàm đọc flag tuy nhiên nó sẽ check biến user phải là admin thì nó mới cho đọc, còn mặc định là guest
- em sẽ sử dụng cái này để có thể ghi vào biến user
- với cái này nó có thể sửa được biến user j
```python3
   0x000000000040122e <+62>:	lea    rsi,[rbp-0x70]
   0x0000000000401232 <+66>:	movsxd rax,DWORD PTR [rbp-0x4]
   0x0000000000401236 <+70>:	add    rsi,rax
   0x0000000000401239 <+73>:	xor    edi,edi
   0x000000000040123b <+75>:	mov    edx,0x8
   0x0000000000401240 <+80>:	call   0x4010e0 <read_>
   0x0000000000401245 <+85>:	mov    edi,0x1
   0x000000000040124a <+90>:	lea    rsi,[rip+0xdbf]        # 0x402010 <ascii_art>
   0x0000000000401251 <+97>:	mov    edx,0x16f
   0x0000000000401256 <+102>:	call   0x4010b0 <write_>
   0x000000000040125b <+107>:	add    rsp,0x70
   0x000000000040125f <+111>:	pop    rbp
   0x0000000000401260 <+112>:	ret
```
- thông qua việc thay đổi địa chỉ rbp vào read vào nơi chỉ định
- tuy nhiên lúc return thì nó return vô 1 chỗ dưới cùng nên lần rop đầu tiên phải rop lại hàm vuln để mở rộng địa bàn, khi return thì sẽ return vào đúng chỗ mình có thể ghi đầu tiên 
- run để đọc flag
```shell
                                                                                        _ 
     |_   _. _|_    o  _    |_  ._ _         _. ._  ._  o ._   _      _. |_   _     _|_  )
\/\/ | | (_|  |_    | _>    |_) | (_)    \/ (_| |_) |_) | | | (_|    (_| |_) (_) |_| |_ o 
                                         /      |   |          _|                         

AKASEC{just_a_fake_flag}
AKASEC{just_a_fake_flag}
AKASEC{just_a_fake_flag}
$  
```
