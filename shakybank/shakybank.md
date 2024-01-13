#write up shakyvault bank

- Để làm được bài này em cần phải leak địa chỉ từ option 2 và write vào stack bằng option 1

## leak địa chỉ 
- em thấy rằng biến idx được khai báo là char, còn idx_in được khai báo là unsigned int, mà char có dấu phần dương max là 127 vậy thì khi nó qua 128 nó thành số âm, vậy lỗi integer overflow đã có tác dụng

![image](https://github.com/antkss/writeUP/assets/88892713/c3a50a00-4028-4d9c-8d5c-2313b4657400)


- qua quan sát thì có thêm cái lỗi format string nữa thông qua việc in mãng char s[128]

  ![image](https://github.com/antkss/writeUP/assets/88892713/73aad85a-4ed9-4696-a8e5-a882020f8bc2)
- đây là vùng mảng char s và mảng total nằm sát nhau trên stack

![image](https://github.com/antkss/writeUP/assets/88892713/389eabba-9f33-41e4-866c-ac7a3842f8d6)

- vậy bây giờ em sẽ dùng option 2 thông qua việc bị integer overflow để ghi format string vào 1 phần tử nào đó trong s khi chương trình quay về trạng thái ban đầu nó sẽ in ra mảng char s 

