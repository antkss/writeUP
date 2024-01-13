# write up shakyvault bank

- Để làm được bài này em cần phải leak địa chỉ từ option 2 và write vào stack bằng option 1

## leak địa chỉ 
- em thấy rằng biến idx được khai báo là char, còn idx_in được khai báo là unsigned int, mà char có dấu phần dương max là 127 vậy thì khi nó qua 128 nó thành số âm, vậy lỗi integer overflow đã có tác dụng

![image](https://github.com/antkss/writeUP/assets/88892713/c3a50a00-4028-4d9c-8d5c-2313b4657400)


- qua quan sát thì có thêm cái lỗi format string nữa thông qua việc in mảng char s[128]

  ![image](https://github.com/antkss/writeUP/assets/88892713/73aad85a-4ed9-4696-a8e5-a882020f8bc2)
- đây là vùng mảng char s và mảng total nằm sát nhau trên stack

![image](https://github.com/antkss/writeUP/assets/88892713/389eabba-9f33-41e4-866c-ac7a3842f8d6)

- vậy bây giờ em sẽ dùng option 2 thông qua việc bị integer overflow để ghi format string vào 1 phần tử nào đó trong s khi chương trình quay về trạng thái ban đầu nó sẽ in ra mảng char s và cả địa chỉ leak nữa

- em chọn đại 1 phần tử trong char, đếm ngược lên từ phần tử 0 của total là 0x00007ffd5c270fb0
thì em chọn phần tử thứ 3 

![image](https://github.com/antkss/writeUP/assets/88892713/aa73ee63-3990-4bc5-a1fa-e02bf6b03748)

- số 253 khi đổi sang char có dấu sẽ là -3
- sau đó em xóa hết phần tử ở chỗ đó của mảng char s bằng cách chọn option 2

![image](https://github.com/antkss/writeUP/assets/88892713/955817fb-4842-4212-a574-df318f12ed71)

- thông qua cái này thì ta có thể thấy nó sẽ lấy total[-3] = total[-3] - money

![image](https://github.com/antkss/writeUP/assets/88892713/88873e0e-e948-44fa-9ab5-f16f894bea9e)

- và total[x] = total[x] + money với x là phần tử thứ x của mảng total (em ko hiểu sao ida nó dịch ngáo rồi =))), nếu code chạy kiểu này chắc tiền vẫn giữ nguyên)

![image](https://github.com/antkss/writeUP/assets/88892713/ec3ae259-5384-469b-ab42-84afa7de8469)

- bằng cách ghi thử thì em thấy nó ghi được vào đúng chỗ
- from:  sẽ là 253 khi nó gán cho idx thì nó sẽ thành -3, vậy nó sẽ lấy dữ liệu từ total[-3]
- to: sẽ là 1 phần tử nào đấy để nó chuyển sang (em đặt bừa)
- Money: em chuyển  '--------' sang integer rồi bỏ vào đây 

![image](https://github.com/antkss/writeUP/assets/88892713/62d73c76-7d50-41ca-bb27-0fe33584b055)


- sau khi thực thi code chuyển tiền xong thì nó thành null

![image](https://github.com/antkss/writeUP/assets/88892713/a9343fdd-cb21-443d-8a83-a10d021cd25b)

- tiếp theo là ghi format string vào


![image](https://github.com/antkss/writeUP/assets/88892713/d71995fb-f098-449a-8797-7f956d767c60)

- from: em đặt chỗ nào mà khi chuyển từ hex sang integer nó có đủ cho em ghi cái format string
chỗ -1 vẫn còn nguyên hàng '-' nên em lấy luôn, vậy idx_in là 255
- to: chắc chắn là 253 rồi
- Money: em sẽ tính xem cần bao nhiêu %p để tới được cái canary
em sẽ đặt break point ngay chỗ printf nó vừa in ra cái format string

![image](https://github.com/antkss/writeUP/assets/88892713/b6af7778-2589-45d0-a7bf-02107d4a1105)

dùng công thức này để tính (địa chỉ trỏ đến dữ liệu cần leak - $rsp tại thời điểm đó )/8 +6 vì format string in ra dữ liệu từ 6 thanh ghi arguments rồi mới đến stack

![image](https://github.com/antkss/writeUP/assets/88892713/a623c6fc-869e-4ee4-bab1-369e45a5b6e7)

vậy format string cần ghi là %283$p\0\0

sau đó em sẽ chuyển nó thành số để ghi vào 

![image](https://github.com/antkss/writeUP/assets/88892713/143215ed-c235-4dea-981d-6bd943848e90)

- tương tự với việc leak địa chỉ, em sẽ leak địa chỉ libc_start_call_main

![image](https://github.com/antkss/writeUP/assets/88892713/4576d3a7-d13d-48c0-b01f-9bd00bf041a1)

- em làm thêm 1 bước leak nữa
- đầu tiên xóa cái %283$p đi xong gắn cái này vào

![image](https://github.com/antkss/writeUP/assets/88892713/52fd4031-5303-4f92-b466-02426d29bc4f)
- vậy là leak được rồi


![image](https://github.com/antkss/writeUP/assets/88892713/b800c989-919f-4622-b42e-ef87639df827)


- tính toán libc_base rồi offset của các thứ cần thiết để tạo shell là xong 


![image](https://github.com/antkss/writeUP/assets/88892713/bf808adb-8ae6-4a73-9fd3-37aac0e1d54f)


## ghi địa chỉ 

- em sẽ chọn option 2 và bắt đầu ghi dữ liệu, mảng total có kích thước từng này nhưng không có biện pháp kiểm soát nên nó tràn

![image](https://github.com/antkss/writeUP/assets/88892713/490b43dc-d59b-477a-8221-8d07f1b1cf9d)

em có thể đặt nó nhiều hơn thế

- đầu tiên em sẽ chọn option 1
- sau đó em sẽ chọn số phần tử là 263 vì em ghi shell bắt đầu từ return là 260 phần tử cộng thêm chuỗi pop_rdi, địa chỉ /bin/sh và system là thêm 3 phần tử nữa, phần tử thứ 260 em để nó là địa chỉ return để cộng rsp lên 8 lúc nó thực thi sao cho đến lúc thực thi system $rsp chia hết cho 16 canary thì em ghi ở phần tử thứ 258, vậy script sẽ là

![image](https://github.com/antkss/writeUP/assets/88892713/8601b86b-5be5-4b3a-9999-c0153bdedd49)


- vậy sau khi ghi xong thì

![image](https://github.com/antkss/writeUP/assets/88892713/311089f9-15df-4c2e-9512-eb5946014599)

- thoát chương trình bằng option 3 thì mọi thứ sau rbp sẽ được thực thi 
