### I. Giới thiệu

- Kỹ thuật `House of Botcake` khá giống kỹ thuật `double free` thông thường tuy nhiên ta sẽ đưa 1 chunk xuất hiện hai lần một cái ở `tcache` và một cái ở `unsorted bin` do đó sẽ gây ra lỗi `UAF` khi ta có thể `malloc` tùy ý với `unsorted bin`.
- Tuy nhiên để tránh lỗi `double free` ta sẽ gộp `chunk` cần free với `chunk` trước nó để `free` không nhận ra được.
- Ta sẽ lợi dụng giới hạn của `tcache` để đưa 1 chunk xuống `unsorted bin`.
- Kỹ thuật này được áp dụng với `tcache` và không thể `double free`

### II. dnote

- Chương trình cho ta `create`, `show`, `delete` một tên vào `notes` dưới dạng heap.

- Với kỹ thuật này đầu tiên ta sẽ setup các `chunk` để đưa xuống `unsorted bin`

- ```python
  for i in range(10):
      create(i, 0x80)
      
  for i in range(7):
      choice(3, i)
  ```

- ![image-20230315214316997](./assets/image-20230315214316997.png)

- Ta sẽ đưa `chunk` cần ở đây tôi chọn `chunk` thứ 8 sau đó thực hiện gộp `chunk` thứ 7 bằng cách `free` nó.

- ```python
  choice(3, 8)
  choice(3, 7)
  ```

- ![image-20230315214457344](./assets/image-20230315214457344.png)

- ![image-20230315214357212](./assets/image-20230315214357212.png)

- Để đưa `chunk` thứ 8 vào lại `tcache` ta cần lấy ra một `chunk`

- ```python
  create(1, 0x80)
  choice(3, 8)
  ```

- ![image-20230315214533239](./assets/image-20230315214533239.png)

- Do `libc` trong `unsorted bin` đang có null byte cuối nên ta sẽ `malloc` 1 chunk vượt quá size của `unsorted bin` để cập nhật lại `fd pointer`

- ![image-20230315214811596](./assets/image-20230315214811596.png)

- ```python
  create(1, 0x120)
  ```

- ![image-20230315214932611](./assets/image-20230315214932611.png)

- Sau khi leak libc và key xor, giờ ta có thể sử dụng lỗi `UAF` với `chunk` thứ 8 này.

- Ta sẽ thực hiện `malloc` 1 chunk với kích thước `0x98` và thay đổi giá trị bên trong `chunk` số 8, thực hiện `overwrite` `__free_hook` thành `system`

- ![image-20230315215219019](./assets/image-20230315215219019.png)

- ![image-20230315215253528](./assets/image-20230315215253528.png)

- ![image-20230315215314701](./assets/image-20230315215314701.png)