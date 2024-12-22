SRC = main.c
NAME = bytecode
CFLAGS = -no-pie -Wl,-z,relro,-z,now -g 

$(NAME): $(SRC)
	gcc $(CFLAGS) $(SRC) -o $(NAME)

clean :
	rm -rf $(NAME)
