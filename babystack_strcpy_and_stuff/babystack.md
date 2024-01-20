#babystack writeup 
- trước tiên chương trình gồm có các lỗi như bufferoverflow

![image](https://github.com/antkss/writeUP/assets/88892713/0f7db4f9-1a60-4e8a-ad1f-5a47dc829f86)


![image](https://github.com/antkss/writeUP/assets/88892713/966335ba-ba24-4b08-953b-0c27991fef60)


mảng userinput và mảng src_copy cùng nằm 1 chỗ trên stack nhưng hàm copy chỉ cho nhập vào src_copy 63 byte đến dest_copy
nhưng nếu dựa vào mảng userinput bên hàm password em thấy rằng nó nhập đc nhiều hơn là 128byte,
63byte thì không đủ để tràn đến saved rip của main, mà chỉ tràn đến cái password vì địa chỉ nó copy vô nằm ở trên main

![image](https://github.com/antkss/writeUP/assets/88892713/de568cee-7463-4eee-aca8-4e496157dc46)


nên em sẽ sử dụng hàm password để nhập truớc 128byte để đến dược rip, nhưng đến đc rip thì nó sẽ lấp mất cái password nằm ở vùng trong main nên em sẽ bị đè nên em cần bruteforce password để bảo tồn và bruteforce địa chỉ libc 

đầu tiên để brute force đc 16bytes password và cả địa chỉ em cần lấp 16bytes tính từ byte password cuối cùng xuống rbp, vì nếu không lấp lại thì strcmp nó sẽ chỉ so sánh các byte sau null


