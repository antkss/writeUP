all:
	gcc  -fno-stack-protector git.c -o git -lcurl -lcjson -Wno-format-truncation
	- rm git_patched libc.so.6
	pwninit

release: all
	cp git ../docker/share