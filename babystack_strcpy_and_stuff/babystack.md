#babystack writeup 
- trước tiên chương trình gồm có các lỗi như bufferoverflow

![image](https://github.com/antkss/writeUP/assets/88892713/0f7db4f9-1a60-4e8a-ad1f-5a47dc829f86)


![image](https://github.com/antkss/writeUP/assets/88892713/966335ba-ba24-4b08-953b-0c27991fef60)


mảng userinput và mảng src_copy cùng nằm 1 chỗ trên stack nhưng hàm copy chỉ cho nhập vào src_copy 63 byte đến dest_copy
nhưng nếu dựa vào mảng userinput bên hàm password em thấy rằng nó nhập đc nhiều hơn là 128byte,
63byte thì không đủ để tràn đến saved rip của main, mà chỉ tràn đến cái password vì địa chỉ nó copy vô nằm ở trên main

![image](https://github.com/antkss/writeUP/assets/88892713/c1787878-48bd-4554-a27b-9e4d766a6f57)



nên em sẽ sử dụng hàm password để nhập truớc 128byte để đến dược rip, nhưng đến đc rip thì nó sẽ lấp mất cái password nằm ở vùng trong main nên em sẽ bị đè nên em cần bruteforce password để bảo tồn và bruteforce địa chỉ libc thông qua hàm strcmp

đầu tiên để brute force đc 16bytes password và cả địa chỉ em cần lấp 16bytes tính từ byte password cuối cùng xuống rbp, vì nếu không lấp lại thì strcmp nó sẽ chỉ so sánh các byte sau null, để lấp đc em chỉ cần nhập 16byte vào biến options ở main vì biến options có địa chỉ ngay sau password 

![image](https://github.com/antkss/writeUP/assets/88892713/70c886f9-69ac-4b69-b725-e7a7e0f27f94)




