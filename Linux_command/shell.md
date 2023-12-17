### Write up linux command

Mở binary lên bằng ida thấy rằng biến command đc thực thi bởi system()



 ![image](https://github.com/antkss/writeUP/assets/88892713/863a33da-b7ec-4621-93c0-ede3b530d775)



mà ta có thể nhập dữ liệu cho command thông qua
 
 
 ![image](https://github.com/antkss/writeUP/assets/88892713/58140b36-b596-4fa2-ace2-7c12a46e910c)


mà thấy rằng 


![image](https://github.com/antkss/writeUP/assets/88892713/b9e0e50c-fcbe-4e1d-968a-0a38516a80fd)
tức là chỉ có 22 ký tự được đưa vào biến command trong tổng số 32 ký tự, 22 kí tự đó chính là câu lệnh 
    
  ![image](https://github.com/antkss/writeUP/assets/88892713/65b0c350-1fcb-494b-a86d-d90d0ae536c6)


vì có tận 32 được nhập vào, tức là e sẽ phải để 22 ký tự trước đó là chữ gì đó để khi chương trình chạy, câu lệnh có 22 ký tự trên
sẽ đè lên và tiếp theo sẽ là chuỗi ký tự mà chúng ta mong muốn, e sẽ chọn chỗi &&sh đằng sau để nó thực thi shell để truy cập vào hệ thống
  
   
 ![image](https://github.com/antkss/writeUP/assets/88892713/e0226290-57b6-415b-9a30-3fce7079807b)
![image](https://github.com/antkss/writeUP/assets/88892713/4b6706db-bbe8-4cac-b622-a1218376cfcd)


khi chạy script thì shell được thực thi


![image](https://github.com/antkss/writeUP/assets/88892713/4b027d20-55f3-461d-8dbd-baf8dcd3b2a2)



