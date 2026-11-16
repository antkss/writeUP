#include <unistd.h>
#include <stdio.h>
#include <sys/ptrace.h>
#include <unistd.h>
#include <sys/wait.h>
#include <stdlib.h>
#include <fcntl.h>
#include <pthread.h>
#include <errno.h>

void* threadHandler(void* _unused) {
  for (;;) {
    usleep(100);
    for (int fd = 3; fd < 7; fd += 1) {
      char content[1024] = { 0 };
      int bytesRead = read(fd, content, sizeof content);
      if (bytesRead <= 0) {
        continue;
      }
      printf("%s\n", content);
    }
  }

  return NULL;
}

void threadThing() {
  pid_t pid = fork();

  int isChild = pid == 0;

  if (isChild) {
    pthread_t thread;
    pthread_create(&thread, NULL, threadHandler, NULL);
    char* args[] = { "/bin/sudo", "-s", NULL };
    execvp(args[0], args);
  } else {
    waitpid(pid, NULL, 0);
  }
}

int main() {
  threadThing();
}
