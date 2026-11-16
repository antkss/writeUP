#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <stdint.h>
#include <stdbool.h>

#define CONSTANT    0
#define REGISTER    1
#define MEM         2
#define MAX_COUNT 0x100

enum COMMAND_TYPE {
    ADD,
    SUBTRACT,
    MULTIPLY,
    DIVIDE,
    STORE,
    LOAD
};

struct arg {
    size_t type;
    size_t val;
};

struct command {
    size_t func;
    struct arg arg[3];
};

struct node {
    uint32_t error_handler;
    uint32_t cur_cmd;
    uint32_t nb_cmd;
    uint32_t next_node;
    int (*error_callback)(struct node *, uint32_t, bool);
    struct command cmd[0];
};


uint32_t node_head;
struct node * node_list[MAX_COUNT];
uint32_t ip;
uint64_t re[5];

char * mem;
size_t mem_size;

uint64_t get_val(struct arg * arg) {
    switch (arg->type) {
        case CONSTANT:
            return arg->val;
        case REGISTER:
            return re[arg->val];
        case MEM:
            return *(uint64_t *)(&mem[arg->val]);
    }
}

void store_val(struct arg * arg, uint64_t val) {
    switch (arg->type) {
        case CONSTANT:
            return;
        case REGISTER:
            re[arg->val] = val;
            return;
        case MEM:
            *(uint64_t *)(&mem[arg->val]) = val;
            return;
    }
}

uint64_t get_val_safe(struct arg * arg) {
    switch (arg->type) {
        case CONSTANT:
            return arg->val;
        case REGISTER:
            return re[arg->val];
        case MEM:
            if (arg->val + 8 > mem_size) {
                mem_size = arg->val + 8;
                return 0;
            }
            return 0;
    }
}

void store_val_safe(struct arg * arg, uint64_t val) {
    switch (arg->type) {
        case CONSTANT:
            return;
        case REGISTER:
            return re[arg->val] = val;
        case MEM:
            if (arg->val + 8 > mem_size) {
                mem_size = arg->val + 8;
                return;
            }
    }
}

int handler1(struct node * node, uint32_t ip, bool debug) {
    if (debug)
        printf("Error happen at node %d, cmd[%d] - CONTINUE\n", ip, node->cur_cmd);
    return 0;
}

int handler2(struct node * node, uint32_t ip, bool debug) {
    if (debug)
        printf("Error happen at node %d, cmd[%d] - DISCONTINUE\n", ip, node->cur_cmd);
    return -1;
}

int handler3(struct node * node, uint32_t ip, bool debug) {
    char buf[5];
    if (debug) {
        printf("Error happen at node %d, cmd[%d] - CONTINUE? (y/n)", ip, node->cur_cmd);
        read(0, buf, 2);
        if (buf[0] == 'Y' || buf[0] == 'y') {
            return 0;
        }
    }
    return -1;
}

uint32_t resolve_error(struct node * cur_node, uint32_t ip, bool debug) {
    if (cur_node->error_callback) {
        if (!debug) {
            cur_node->cur_cmd++;
            return 1;
        }
        if (cur_node->error_callback(cur_node, ip, debug)) {
            return 0;
        }
        else {
            cur_node->cur_cmd++;
            return 1;
        }
    }
    else {
        cur_node->cur_cmd = 0;
        return 2;
    }
}

void simulate() {
    struct node * cur_node;
    size_t i;
    ip = node_head;
    memset(re, 0, sizeof re);
    memset(mem, 0, mem_size);
    uint64_t tmp;
    uint32_t cycle = 0;
    uint32_t status_code;
    while (cycle <= 0x5000) {
        cur_node = node_list[ip];
        if (!cur_node) {
            break;
        }
        if (cur_node->cur_cmd >= cur_node->nb_cmd) {
            if (cur_node->next_node) {
                ip = cur_node->next_node;
                cur_node = node_list[ip];
            }
            else {
                break;
            }
        }
        cycle++;
        switch (cur_node->cmd[cur_node->cur_cmd].func) {
            case ADD:
                tmp = get_val_safe(&cur_node->cmd[cur_node->cur_cmd].arg[0]) + get_val_safe(&cur_node->cmd[cur_node->cur_cmd].arg[1]);
                store_val_safe(&cur_node->cmd[cur_node->cur_cmd].arg[2], tmp);
                cur_node->cur_cmd++;
                break;
            case SUBTRACT:
                tmp = get_val_safe(&cur_node->cmd[cur_node->cur_cmd].arg[0]) - get_val_safe(&cur_node->cmd[cur_node->cur_cmd].arg[1]);
                store_val_safe(&cur_node->cmd[cur_node->cur_cmd].arg[2], tmp);
                cur_node->cur_cmd++;
                break;
            case MULTIPLY:
                tmp = get_val_safe(&cur_node->cmd[cur_node->cur_cmd].arg[0]) * get_val_safe(&cur_node->cmd[cur_node->cur_cmd].arg[1]);
                store_val_safe(&cur_node->cmd[cur_node->cur_cmd].arg[2], tmp);
                cur_node->cur_cmd++;
                break;
            case DIVIDE:
                if (get_val_safe(&cur_node->cmd[cur_node->cur_cmd].arg[1]) == 0) {
                    status_code = resolve_error(cur_node, ip, 0);
                    if (status_code == 0) {
                        return;
                    }
                    if (status_code == 1) {
                        break;
                    }
                    if (status_code == 2) {
                        ip = cur_node->error_handler;
                        continue;
                    }
                }
                tmp = get_val_safe(&cur_node->cmd[cur_node->cur_cmd].arg[0]) / get_val_safe(&cur_node->cmd[cur_node->cur_cmd].arg[1]);
                store_val_safe(&cur_node->cmd[cur_node->cur_cmd].arg[2], tmp);
                cur_node->cur_cmd++;
                break;
            case LOAD:
                if (cur_node->cmd[cur_node->cur_cmd].arg[0].type != MEM) {
                    status_code = resolve_error(cur_node, ip, 0);
                    if (status_code == 0) {
                        return;
                    }
                    if (status_code == 1) {
                        break;
                    }
                    if (status_code == 2) {
                        ip = cur_node->error_handler;
                        continue;
                    }
                }
                tmp = get_val_safe(&cur_node->cmd[cur_node->cur_cmd].arg[0]);
                store_val_safe(&cur_node->cmd[cur_node->cur_cmd].arg[1], tmp);
                cur_node->cur_cmd++;
                break;
            case STORE:
                if (cur_node->cmd[cur_node->cur_cmd].arg[0].type != MEM) {
                    status_code = resolve_error(cur_node, ip, 0);
                    if (status_code == 0) {
                        return;
                    }
                    if (status_code == 1) {
                        break;
                    }
                    if (status_code == 2) {
                        ip = cur_node->error_handler;
                        continue;
                    }
                }
                store_val_safe(&cur_node->cmd[cur_node->cur_cmd].arg[0], get_val_safe(&cur_node->cmd[cur_node->cur_cmd].arg[1]));
                cur_node->cur_cmd++;
                break;
        }        
    }
    for (i = 0; i < MAX_COUNT; ++i) {
        if (node_list[i]) {
            node_list[i]->cur_cmd = 0;
        }
    }
}
void run() {
    struct node * cur_node;
    ip = node_head;
    memset(re, 0, sizeof re);
    memset(mem, 0, mem_size);
    uint64_t tmp;
    uint32_t cycle = 0;
    uint32_t status_code;
    while (cycle <= 0x5000) {
        cur_node = node_list[ip];
        if (!cur_node) {
            break;
        }
        if (cur_node->cur_cmd >= cur_node->nb_cmd) {
            if (cur_node->next_node) {
                ip = cur_node->next_node;
                cur_node = node_list[ip];
            }
            else {
                break;
            }
        }
        cycle++;
        switch (cur_node->cmd[cur_node->cur_cmd].func) {
            case ADD:
		// 0+1
                tmp = get_val(&cur_node->cmd[cur_node->cur_cmd].arg[0]) + get_val(&cur_node->cmd[cur_node->cur_cmd].arg[1]);
                store_val(&cur_node->cmd[cur_node->cur_cmd].arg[2], tmp);
                cur_node->cur_cmd++;
                break;
            case SUBTRACT:
                tmp = get_val(&cur_node->cmd[cur_node->cur_cmd].arg[0]) - get_val(&cur_node->cmd[cur_node->cur_cmd].arg[1]);
                store_val(&cur_node->cmd[cur_node->cur_cmd].arg[2], tmp);
                cur_node->cur_cmd++;
                break;
            case MULTIPLY:
                tmp = get_val(&cur_node->cmd[cur_node->cur_cmd].arg[0]) * get_val(&cur_node->cmd[cur_node->cur_cmd].arg[1]);
                store_val(&cur_node->cmd[cur_node->cur_cmd].arg[2], tmp);
                cur_node->cur_cmd++;
                break;
            case DIVIDE:
                if (get_val(&cur_node->cmd[cur_node->cur_cmd].arg[1]) == 0) {
                    status_code = resolve_error(cur_node, ip, 1);
                    if (status_code == 0) {
                        goto output;
                    }
                    if (status_code == 1) {
                        break;
                    }
                    if (status_code == 2) {
                        ip = cur_node->error_handler;
                        continue;
                    }
                }
                tmp = get_val(&cur_node->cmd[cur_node->cur_cmd].arg[0]) / get_val(&cur_node->cmd[cur_node->cur_cmd].arg[1]);
                store_val(&cur_node->cmd[cur_node->cur_cmd].arg[2], tmp);
                cur_node->cur_cmd++;
                break;
            case LOAD:
                if (cur_node->cmd[cur_node->cur_cmd].arg[0].type != MEM) {
                    status_code = resolve_error(cur_node, ip, 1);
                    if (status_code == 0) {
                        goto output;
                    }
                    if (status_code == 1) {
                        break;
                    }
                    if (status_code == 2) {
                        ip = cur_node->error_handler;
                        continue;
                    }
                }
                tmp = get_val(&cur_node->cmd[cur_node->cur_cmd].arg[0]);
                store_val(&cur_node->cmd[cur_node->cur_cmd].arg[1], tmp);
                cur_node->cur_cmd++;
                break;
            case STORE:
                if (cur_node->cmd[cur_node->cur_cmd].arg[0].type != MEM) {
                    status_code = resolve_error(cur_node, ip, 1);
                    if (status_code == 0) {
                        goto output;
                    }
                    if (status_code == 1) {
                        break;
                    }
                    if (status_code == 2) {
                        ip = cur_node->error_handler;
                        continue;
                    }
                }
                store_val(&cur_node->cmd[cur_node->cur_cmd].arg[0], get_val(&cur_node->cmd[cur_node->cur_cmd].arg[1]));
                cur_node->cur_cmd++;
                break;

        }

        
    }
output:
    puts("Finish running");
    printf("IP: %u\n", ip);
}

bool check_func(uint64_t func) {
    if (func > LOAD) {
        return false;
    }
    return true;
}

void new_node() {
    size_t idx;
    size_t nb_cmd;
    size_t i;
    size_t j;
    struct node * node;
    struct command * cmd;
    struct arg * arg;
    char buf[5];
    uint32_t handler;

    size_t type;
    size_t val;
    size_t func;
    uint32_t next_node;
    printf("Index: ");
    idx = read_int();

    if ( idx == 0 || idx >= MAX_COUNT || node_list[idx]) {
        puts("Invalid index");
        return;
    }

    printf("Number of command: ");
    nb_cmd = read_int();

    if ( nb_cmd >= 0x10) {
        puts("Too many commands");
        return;
    }

    printf("Next node: ");
    next_node = read_int();

    if ( next_node >= MAX_COUNT) {
        puts("Invalid node");
        return;
    }

    node            = calloc(sizeof (struct node) + sizeof(struct command) * nb_cmd, 1);
    node->nb_cmd    = nb_cmd;
    node->next_node = next_node;

    printf("Fill command list: ");
    read(0, node->cmd, sizeof(struct command) * nb_cmd);

    for (i = 0; i < nb_cmd; ++i) {
        for (j = 0;j < 3; ++j) {
            cmd = &node->cmd[i];
            arg = &cmd->arg[j];
            type = arg->type;
            val = arg->val;
            func = cmd->func;
            if ( (type > MEM ) || !check_func(func) || (type == REGISTER && val >= 5) || (type == MEM && val >= 0xffffffff)) {
                free(node);
                puts("Invalid commands");
                return;
            }
        }
    }

    printf("Use default handler? (y/n): ");
    read(0, buf, 2);
    if (buf[0] == 'Y' || buf[0] == 'y') {
        printf("Input default error handler: ");
        handler = read_int();
        if (handler == 1) {
            node->error_callback = &handler1;
        }
        else if (handler == 2)
        {
            node->error_callback = &handler2;
        }
        else {
            node->error_callback = &handler3;
        } 
    }
    else {
        printf("Input error handler: ");
        handler = read_int();
        node->error_handler = handler;
    }

    node_list[idx] = node;
}

void cleanup() {
    size_t i;
    for (i = 0; i < MAX_COUNT; ++i) {
        if (node_list[i]) {
            free(node_list[i]);
            node_list[i] = NULL;
        }
    }
}

void menu() {
    printf("\n");
    puts("------------------------");
    puts("1. New node");
    puts("2. Run");
    puts("3. Exit");
    printf("> ");
}
void timeout() {
    puts("Timeout");
    exit(1);
}

int read_int() {
    char buf[20];
    memset(buf, 0, 20);
    read(0, buf, 10);
    return atoi(buf);
}

void init() {
    signal(0xe,&timeout);
    alarm(60);
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stderr, NULL, _IONBF, 0);
}

int main(void) {
    init();
    puts("A weird machine simulation!");
    int choice;
    while (1) {
        menu();
        choice = read_int();
        switch (choice) {
            case 1:
                new_node();
                break;
            case 2:
                printf("Where to start? ");
                node_head = read_int();
                if (node_head == 0 || node_head > MAX_COUNT) {
                    puts("Invalid start");
                    break;
                }
                simulate();
                mem = calloc(mem_size, 1);
                if (!mem) {
                    puts("Out of memory");
                    exit(1);
                }
                run();
                free(mem);
                mem = NULL;
                mem_size = 0;
                cleanup();
                break;
            case 3:
                exit(0);
                break;
        }
    }
}
