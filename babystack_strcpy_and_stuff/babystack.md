# babystack writeup 
- trước tiên chương trình gồm có lỗi bufferoverflow do strcpy gây nên 

![image](https://github.com/antkss/writeUP/assets/88892713/0f7db4f9-1a60-4e8a-ad1f-5a47dc829f86)


![image](https://github.com/antkss/writeUP/assets/88892713/966335ba-ba24-4b08-953b-0c27991fef60)


mảng userinput và mảng src_copy cùng nằm 1 chỗ trên stack nhưng hàm copy chỉ cho nhập vào src_copy 63 byte đến dest_copy
nhưng nếu dựa vào mảng userinput bên hàm password em thấy rằng nó nhập đc nhiều hơn là 128byte,
63byte thì không đủ để tràn đến saved rip của main, mà chỉ tràn đến cái password vì địa chỉ nó copy vô nằm ở trên main

![image](https://github.com/antkss/writeUP/assets/88892713/c1787878-48bd-4554-a27b-9e4d766a6f57)



nên em sẽ sử dụng hàm password để nhập truớc 128byte để đến dược rip, nhưng đến đc rip thì nó sẽ lấp mất cái password nằm ở vùng trong main nên em sẽ bị đè nên em cần bruteforce password để bảo tồn và bruteforce địa chỉ libc thông qua hàm strcmp

đầu tiên để brute force đc 16bytes password và cả địa chỉ em cần lấp 16bytes tính từ byte password cuối cùng xuống rbp, vì nếu không lấp lại thì strcmp nó sẽ chỉ so sánh các byte sau null, để lấp đc em chỉ cần nhập 16byte vào biến options ở main vì biến options có địa chỉ ngay sau password 

![image](https://github.com/antkss/writeUP/assets/88892713/70c886f9-69ac-4b69-b725-e7a7e0f27f94)


sau khi lấp xong thì em sẽ bruteforce bằng cách tạo vòng lập python so sánh từng ký tự từ 1 -> 256 vì để tránh byte null, nếu so sánh ký tự thứ 1 thành công thì chuyển sang ký tự thứ 2, để so sánh đc như vậy ta phải thêm null đằng sau ký tự cần so sánh và cộng dồn đến khi đến null byte. 


![image](https://github.com/antkss/writeUP/assets/88892713/bb4853a8-4f70-4760-8e65-0bee1fee6266)


- Vậy khi brutefore thì em sẽ nhận được chuỗi như sau:


  ![image](https://github.com/antkss/writeUP/assets/88892713/a9a3004d-6754-4932-aa11-f321d69e1327)

- Sau khi bruteforce được tất cả các ký tự ra và xử lý các thứ thì em sẽ có được địa chỉ cũng như password 

- Tiếp theo là tìm địa chỉ base libc và tìm offset của pop_rdi, /bin/sh và libc_system rồi tính địa chỉ của nó:

![image](https://github.com/antkss/writeUP/assets/88892713/83d14ae6-b68b-48c1-8c40-6e8ec4a320b3)


- Sau khi tính xong ta tìm cách ghi vào saved rip bằng cách sử dụng hàm password và copy, vì địa chỉ có chứa null byte nên không thể copy qua hết đc nên em sẽ nhập lần lượt, nhưng mà trước tiên phải đảm bảo mật khẩu khi bỏ vào đúng với trên stack và phải đảm bảo mật khẩu không bị chèn mất thì em cần phải tính toán sao cho mật khẩu khi copy qua nằm đúng chỗ và đảm bảo những gì copy ko có chứa null byte

- Đầu tiên em sẽ nhập địa chỉ đầu: em thấy nếu nhập xong copy như thông thường thì không đc vì e dùng quá 127bytes, vì vậy em sẽ tách địa chỉ ra thành 3 phần để copy phần 1 là 4byte và 2 phần còn lại mỗi phần 1 byte

 ![image](https://github.com/antkss/writeUP/assets/88892713/48b7bded-67c2-41e0-9142-7a8133a70194)


![image](https://github.com/antkss/writeUP/assets/88892713/91c84f49-3894-4d1e-8a5c-00503a3497f0)


- sau khi tách xong e sẽ ghi lần lượt từng phần vào thông qua script, sẽ có 3 lần ghi vào, payload gồm có: password + nullbyte + 0x29byte (offset để tới biến password) + padding(nơi cần ghi địa chỉ) + địa chỉ
- ở đây em sẽ ghi 4bytes cuối trước nên padding của em là b'a'* 0x18  + b'a'*8 +b'aaaaaaaaaa' (em để vậy do em lười rút gọn =))))  và các phần sau của địa chỉ padding sẽ ít hơn 1 byte  
![image](https://github.com/antkss/writeUP/assets/88892713/ebe9c87d-f849-482b-8777-d62bbfaa9294)

- tiếp theo là /bin/sh và cuối cùng là pop_rdi, với 2 địa chỉ sau sẽ có dính byte của địa chỉ trước là mấy cái chữ A vì địa chỉ trước cần tràn nhiều hơn, khi bị đính chữ a địa chỉ sẽ thành không hợp lệ 

![image](https://github.com/antkss/writeUP/assets/88892713/b66be9bc-d415-4c22-97bf-1fc779cda8c1)


- Nên để xóa chữ a em tận dụng NULL byte ở cuối khi nó copy để xóa cái ký tự trước đó bằng cách đẩy dữ liệu copy lên 1 byte xong rồi mới copy cái cần copy

![image](https://github.com/antkss/writeUP/assets/88892713/88e810d6-743b-4ac5-bb20-7d1751e56686)


- vậy là em có thể chạy và thực thi shell 1 cách trơn tru


  ![image](https://github.com/antkss/writeUP/assets/88892713/8495d017-75f2-4224-8da8-5e50ef95603b)



