// https://github.com/seifzadeh/c-network-programming-best-snipts/blob/master/Handle%20multiple%20socket%20connections%20with%20fd_set%20and%20select%20on%20Linux

#include <stdio.h>
#include <string.h>   //strlen
#include <stdlib.h>
#include <errno.h>
#include <unistd.h>   //close
#include <arpa/inet.h>    //close
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <pthread.h>
#include <sys/time.h> //FD_SET, FD_ISSET, FD_ZERO macros
  
#define TRUE   1
#define FALSE  0
#define PORT 10000
 
char *greeting_msg = "KMA Chatroom v1.0\n";

struct name_struct
{
    char *name;
    unsigned int name_size;
    struct name_struct *next;
} *namelist;
struct chat_struct
{
    char *name;
    unsigned int name_size;
    char *message;
    unsigned int message_size;
    struct chat_struct *next;
} *chat;
struct client_struct
{
    int sock;
    struct chat_struct latest_chat;
};

int client_recv_count = 0;
unsigned int msg_length = 0;

struct name_struct* is_name_existed(char *name)
{
    struct name_struct *tmp_name;

    for ( tmp_name=namelist; tmp_name; tmp_name=tmp_name->next )
    {
        if (!strncmp(tmp_name->name, name, tmp_name->name_size))
            return tmp_name;
    }
    return NULL;
}

void handle_recv(struct client_struct *c)
{
    // char buffer[4096];
    char *name, *message;
    int sock, retvalue, size;
    struct chat_struct *tmp_chat;
    struct name_struct *tmp_name;

    sock = c->sock;
    c->sock = 0;
    if (size = recv(sock, &c->latest_chat.name_size, 4, 0), size == 0)
        goto failed;
    if (size = recv(sock, &c->latest_chat.message_size, 4, 0), size == 0)
        goto failed;
    if ( c->latest_chat.name_size<=0 || c->latest_chat.message_size<=0 )
        goto failed;
    name = alloca(c->latest_chat.name_size + 1);
    memset(name, 0, c->latest_chat.name_size+1);
    message = alloca(c->latest_chat.message_size+1);
    memset(message, 0, c->latest_chat.message_size+1);

    if (size = recv(sock, name, c->latest_chat.name_size, 0), size == 0)
        goto failed;
    tmp_name = is_name_existed(name);
    if (!tmp_name)
    {
        if (!namelist)
        {
            namelist = malloc(sizeof(struct name_struct));
            tmp_name = namelist;
        }
        else
        {
            for ( tmp_name=namelist ; tmp_name->next ; tmp_name=tmp_name->next );
            tmp_name->next = malloc(sizeof(struct name_struct));
            tmp_name = tmp_name->next;
        }        
        tmp_name->name_size = c->latest_chat.name_size;
        tmp_name->name = malloc(tmp_name->name_size + 1);
        memcpy( tmp_name->name, name, tmp_name->name_size );
        tmp_name->next = 0;
    }

    if (size = recv(sock, message, c->latest_chat.message_size, 0), size == 0)
        goto failed;
    if (!chat)
    {
        chat = malloc(sizeof(struct chat_struct));
        tmp_chat = chat;
    }
    else
    {
        for ( tmp_chat=chat ; tmp_chat && tmp_chat->next ; tmp_chat=tmp_chat->next );
        tmp_chat->next = malloc(sizeof(struct chat_struct));
        tmp_chat = tmp_chat->next;
    }
    tmp_chat->name_size = tmp_name->name_size;
    tmp_chat->name = tmp_name->name;
    tmp_chat->message_size = c->latest_chat.message_size;
    tmp_chat->message = malloc(tmp_chat->message_size + 1);
    memcpy( tmp_chat->message, message, tmp_chat->message_size );

    retvalue = 1;
    send(sock, &retvalue, 4, 0);
    close(sock);
    pthread_exit(NULL);

failed:
    retvalue = -1;
    send(sock, &retvalue, 4, 0);
    close(sock);
    pthread_exit(NULL);

}
void handle_send(struct client_struct *c)
{
    int sock, value;
    struct chat_struct *tmp_chat;

    sock = c->sock;
    c->sock = 0;
    tmp_chat = chat;
    while (tmp_chat && tmp_chat->name && tmp_chat->message)
    {
        send(sock, &tmp_chat->name_size, 4, 0);
        send(sock, tmp_chat->name, tmp_chat->name_size, 0);
        send(sock, &tmp_chat->message_size, 4, 0);
        send(sock, tmp_chat->message, tmp_chat->message_size, 0);
        tmp_chat = tmp_chat->next;
    }
    value = -1;
    send(sock, &value, 4, 0);
    close(sock);
    pthread_exit(NULL); 
}

void client_handler(struct client_struct *c) {
    int opcode, size;

    if (size = recv(c->sock, &opcode, 4, 0), size == 0)
        goto failed;
    if (opcode==0) {
        handle_recv(c);
    } else if (opcode==1) {
        handle_send(c);
    }

failed:
    opcode = -1;
    send(c->sock, &opcode, 4, 0);
    close(c->sock);
    c->sock = 0;
    pthread_exit(NULL);
}

void init()
{
    setbuf(stdout, 0);
}

int main(int argc , char *argv[])
{
    pthread_t ptid;
    struct client_struct c;
    int opt = TRUE;
    int server_sock, addrlen, client_socket;
    struct sockaddr_in address;

    init();
    memset(&c, 0, sizeof(struct client_struct));
    if( (server_sock = socket(AF_INET , SOCK_STREAM , 0)) == 0) 
    {
        perror("socket");
        exit(EXIT_FAILURE);
    }

    //set master socket to allow multiple connections , this is just a good habit, it will work without this
    if( setsockopt(server_sock, SOL_SOCKET, SO_REUSEADDR, (char *)&opt, sizeof(opt)) < 0 )
    {
        perror("setsockopt");
        exit(EXIT_FAILURE);
    }

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons( PORT );
    addrlen = sizeof(address);

    if (bind(server_sock, (struct sockaddr *)&address, sizeof(address))<0) 
    {
        perror("bind failed");
        exit(EXIT_FAILURE);
    }
    printf("Listener on port %d \n", PORT);

    if (listen(server_sock, 3) < 0)
    {
        perror("listen");
        exit(EXIT_FAILURE);
    }

    while(TRUE) 
    {
        client_socket = accept(server_sock, (struct sockaddr *)&address, (socklen_t*)&addrlen);

        while (c.sock);
        printf("New connection to recv sock from %s:%d\n" , inet_ntoa(address.sin_addr) , ntohs(address.sin_port));
        c.sock = client_socket;
        pthread_create(&ptid, NULL, (void*)&client_handler, &c);
    }

    return 0;
} 