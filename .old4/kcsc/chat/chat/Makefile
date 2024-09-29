all:
	gcc chat.c -o chat -lpthread
	gcc client.c -o client -lpthread -lncurses
	cp chat chat.bak
	patchelf --replace-needed libc.so.6 ./libc.so.6 chat
	patchelf --replace-needed libpthread.so.0 ./libpthread.so.0 chat
	patchelf --set-interpreter ld-linux-x86-64.so.2 chat

release: all
	cp chat.bak ../docker/share/chat
	mv chat.bak ../player/share/chat
	cp client ../player/share