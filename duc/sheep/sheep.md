# write up sheep 
- vì bài có oob nên có thể leak địa chỉ từ đây
```c
 void view_sheep(game_t* game) {
    int idx = read_int("index> ");
    if(idx >= SHEEP_MAX || game->sheep[idx] == NULL) {
        puts("That sheep doesn't exist!");
        return;
    }

    printf("Sheep %d\n", idx);
    printf("\tWPS: %ld\n", game->sheep[idx]->wps);
    printf("\tValue: %ld\n", game->sheep[idx]->value);
}
```
- vì bài chỉ có thể ghi thông qua chỗ này nên ta chỉ có thể leak libc bằng cách fake chunk
```c
    if(game->wool <= upgrade_type * 10) {
        puts("You can't afford that yet!");
        return;
    }

    if(upgrade_type == 1) {
        game->sheep[idx]->wps += 1;
    } else if(upgrade_type == 2) {
        game->sheep[idx]->wps *= 2;
    }

    game->sheep[idx]->value += upgrade_type * 9;
    game->wool -= upgrade_type * 10;
```
- 
- e sẽ fake 3 chunk 1 chunk đầu size 0x420 2 chunk tiếp theo là 0x20
- sau đó ghi địa chỉ chunk đầu vào fd rồi malloc rồi free nó để nó xuống unsorted bin
- rồi sau đó dùng oob để leak libc
- có thể ghi như dữ liệu mong muốn như sau:
  ```python
    mangle = protect(value,address)
    for i in range(64):
        upgrade(idx,2)
        if (mangle>>(64-i-1))&1:
            upgrade(idx,1)
  ```
  - sau vì thế cùng với cách này e có thể leak cả stack, và mọi thứ
  - sau đó có thể ghi ở mọi nơi
  
