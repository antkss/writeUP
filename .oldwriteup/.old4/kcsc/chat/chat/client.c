#include <ncurses.h>
#include <string.h>
#include <arpa/inet.h>
#include <stdio.h>
#include <sys/socket.h>
#include <unistd.h>
#include <stdlib.h>

#define MAXINPUT 256

struct chat_struct
{
    int id;
    char *name;
    char *message;
    struct chat_struct *next;
} *chat;

int row;
int col;

void init()
{
    setbuf(stdout, 0);
}

void backspace(int *pos, int *input_count, char *input){
    char tmp[MAXINPUT];
    int i, j=0;

    if (*pos<=0)
        return;
    memset(tmp, 0, sizeof(tmp));
    for (i=0; i<*pos-1; i++)
        tmp[j++] = input[i];
    for (int i=*pos; i<*input_count; i++)
        tmp[j++] = input[i];
    *input_count = *input_count-1;
    *pos = *pos-1;
    memset(input, 0, MAXINPUT);
    memcpy(input, tmp, MAXINPUT);
}

void delete(int *pos, int *input_count, char *input){
    char tmp[MAXINPUT];
    int i, j=0;

    if (*pos==*input_count)
        return;
    memset(tmp, 0, sizeof(tmp));
    for (i=0; i<*pos; i++)
        tmp[j++] = input[i];
    for (int i=*pos+1; i<*input_count; i++)
        tmp[j++] = input[i];
    *input_count = *input_count-1;
    memset(input, 0, MAXINPUT);
    memcpy(input, tmp, MAXINPUT);
}

void insert_char(int *pos, int *input_count, char *input, int ch){
    char tmp[MAXINPUT];
    int i, j=0;

    memset(tmp, 0, sizeof(tmp));
    if (*pos==*input_count)
    {
        input[*pos] = ch;
        *pos = *pos + 1;
        *input_count = *input_count + 1;
        return;
    }
    else if (*pos==0)
    {
        tmp[j++] = ch;
        for (i=*pos; i<*input_count; i++)
            tmp[j++] = input[i];
    }
    else
    {
        for (i=0; i<*pos; i++)
            tmp[j++] = input[i];
        tmp[j++] = ch;
        for (i=*pos; i<*input_count; i++)
            tmp[j++] = input[i];
    }
    *pos = *pos + 1;
    *input_count = *input_count + 1;
    memset(input, 0, MAXINPUT);
    memcpy(input, tmp, MAXINPUT);
}

void send_message(char *ip, char *port, char *name, char *message)
{
    int size, opcode, client_fd;
    struct sockaddr_in serv_addr;

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(atoi(port));
    inet_pton(AF_INET, ip, &serv_addr.sin_addr);

    if ((client_fd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        return;
    }
    if ( connect(client_fd, (struct sockaddr*)&serv_addr, sizeof(serv_addr)) < 0 ) {
        return;
    }
    opcode=0;
    send(client_fd, &opcode, 4, 0);
    size=strlen(name)+1;
    send(client_fd, &size, 4, 0);
    size=MAXINPUT;
    send(client_fd, &size, 4, 0);
    size=strlen(name)+1;
    send(client_fd, name, size, 0);
    send(client_fd, message, MAXINPUT, 0);
    recv(client_fd, &size, 4, 0);

    close(client_fd);
}

void recv_message(char *ip, char *port)
{
    char *name, *msg;
    int size, opcode, client_fd, from_id, id;
    struct sockaddr_in serv_addr;
    struct chat_struct *tmp_chat;

    mvprintw(2, 0, "Receiving messages...");
    move(row-1, 2);
    refresh();

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(atoi(port));
    inet_pton(AF_INET, ip, &serv_addr.sin_addr);

    while (1)
    {
        if ((client_fd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
            sleep(1);
            continue;
        }
        if ( connect(client_fd, (struct sockaddr*)&serv_addr, sizeof(serv_addr)) < 0 ) {
            sleep(1);
            continue;
        }

        opcode=1;
        send(client_fd, &opcode, 4, 0);

        id = 0;
        while (1)
        {
            recv(client_fd, &size, 4, 0);
            if (size<0)
                break;
            name = malloc(size+1);
            for (int i=0; i<size; i++)
                recv(client_fd, &name[i], 1, 0);
            name[size] = '\0';
            recv(client_fd, &size, 4, 0);
            msg = malloc(size+1);
            for (int i=0; i<size; i++)
                recv(client_fd, &msg[i], 1, 0);
            msg[size] = '\0';

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
            tmp_chat->id = id;
            tmp_chat->name = name;
            tmp_chat->message = msg;
            tmp_chat->next = NULL;
            id++;
        }

        if (!id)
        {
            close(client_fd);
            sleep(1);
            continue;
        }
        if (id > (row-10-2)/2)
            from_id = id - (row-10 - 2)/2;
        else
            from_id=0;
        for (tmp_chat=chat; tmp_chat && tmp_chat->id!=from_id; tmp_chat=tmp_chat->next);
        for (int i=0; tmp_chat; i++, tmp_chat=tmp_chat->next)
        {
            mvprintw(2+i*2, 0, "--- %s", tmp_chat->name);
            clrtoeol();
            mvprintw(2+1+i*2, 0, "%s", tmp_chat->message);
            clrtoeol();
        }
        move(row-1, 2);
        refresh();
        for (tmp_chat=chat; tmp_chat;)
        {
            tmp_chat = chat->next;
            free(chat->name);
            free(chat->message);
            free(chat);
            chat = tmp_chat;
        }
        chat = NULL;
        close(client_fd);
        sleep(1);
    }

    close(client_fd);
}

int main(int argc, char* argv[]) {
    int size;
    char input[MAXINPUT], previnput[MAXINPUT], currentinput[MAXINPUT], name[MAXINPUT], *msg;
    int input_count = 0, pos = 0;
    MEVENT event;
    struct sockaddr_in serv_addr;

    if (argc < 3)
    {
        puts("Usage: client <server-ip> <port>");
        exit(0);
    }
    if (inet_pton(AF_INET, argv[1], &serv_addr.sin_addr) <= 0) {
        printf(
            "\nInvalid address / Address not supported \n");
        return -1;
    }

    init();
    memset(input, 0, MAXINPUT);
    memset(previnput, 0, MAXINPUT);
    memset(currentinput, 0, MAXINPUT);
    memset(name, 0, MAXINPUT);

    printf("Your name: ");
    size = read(0, name, MAXINPUT);
    if (name[size-1]=='\n')
        name[size-1]='\0';

    initscr();            // Start curses mode
    cbreak();             // Disable line buffering
    noecho();             // Don't echo input to the screen
    keypad(stdscr, TRUE); // Enable function keys and arrow keys
    curs_set(1);          // Show the cursor

    getmaxyx(stdscr, row, col); // Get the screen size

    mvprintw(0, 0, "Welcome to KMA Chat!");
    mvprintw(row-10, 0, "----------");
    mvprintw(row-2, 0, "Name: %s", name);
    move(row - 1, 0);
    printw("> ");
    refresh();

    if(!fork())
    {
        recv_message(argv[1], argv[2]);
        exit(0);
    }
    while (1) {
        int ch = wgetch(stdscr); // Wait for user input

        if (ch == KEY_UP) {
            pos = strlen(previnput);
            input_count = strlen(previnput);
            memcpy(input, previnput, MAXINPUT);
            move(row - 1, 2);
            clrtoeol();  // Clear the rest of the line
            printw("%s", input);
            refresh();
        } else if (ch == KEY_DOWN) {
            pos = strlen(currentinput);
            input_count = strlen(currentinput);
            memcpy(input, currentinput, MAXINPUT);
            move(row - 1, 2);
            clrtoeol();  // Clear the rest of the line
            printw("%s", input);
            refresh();
        } else if (ch == KEY_LEFT) {
            if (pos > 0) {
                pos--;
                move(row - 1, pos + 2);
                refresh();
            }
        } else if (ch == KEY_RIGHT) {
            if (pos < input_count) {
                pos++;
                move(row - 1, pos + 2);
                refresh();
            }
        } else if (ch == KEY_BACKSPACE) {
            move(row - 1, 2);
            clrtoeol();  // Clear the rest of the line
            backspace(&pos, &input_count, input);
            printw("%s", input);
            move(row - 1, pos + 2);
            refresh();
        } else if (ch == KEY_DL || ch == 0x14a) {
            move(row - 1, 2);
            clrtoeol();  // Clear the rest of the line
            delete(&pos, &input_count, input);
            printw("%s", input);
            move(row - 1, pos + 2);
            refresh();
        } else if (ch == '\n') {
            memcpy(previnput, input, MAXINPUT);
            msg = malloc(MAXINPUT);
            memcpy(msg, input, MAXINPUT);
            if (fork())
            {
                move(row - 1, 2);
                clrtoeol();  // Clear the input line
                pos = 0;
                input_count = 0;
                memset(input, 0, MAXINPUT);
                memset(currentinput, 0, MAXINPUT);
            }
            else
            {
                if (input_count)
                    send_message(argv[1], argv[2], name, msg);
                exit(0);
            }
        } else if (pos < MAXINPUT-1) {
            insert_char(&pos, &input_count, input, ch);
            memcpy(currentinput, input, MAXINPUT);
            move(row - 1, 2);
            clrtoeol();  // Clear the rest of the line
            printw("%s", input);
            move(row - 1, pos + 2);
            refresh();
        }

        refresh(); // Refresh the screen to update changes
    }

    endwin(); // End curses mode
    return 0;
}
