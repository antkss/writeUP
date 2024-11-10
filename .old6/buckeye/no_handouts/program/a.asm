section .data
    filename db 'flag.txt', 0           ; File to open (null-terminated)
    buffer   times 128 db 0             ; Buffer to store file content
    flags    dq 0                       ; O_RDONLY flag (value is 0)

section .bss
    bytes_read resb 1                   ; For storing the number of bytes read

section .text
    global _start

_start:
    ; 1. Open the file (open syscall)
    ; rax = 2 (open)
    ; rdi = pointer to filename
    ; rsi = O_RDONLY
    mov rax, 2                          ; syscall number for open
    lea rdi, [rel filename]             ; pointer to filename
    xor rsi, rsi                        ; O_RDONLY = 0
    syscall                             ; invoke syscall

    ; Check if open failed
    cmp rax, -1
    je  error                           ; Jump to error if failed
    mov rdi, rax                        ; Store file descriptor in rdi for further use

    ; 2. Read the file (read syscall)
    ; rax = 0 (read)
    ; rdi = file descriptor
    ; rsi = pointer to buffer
    ; rdx = number of bytes to read
    mov rax, 0                          ; syscall number for read
    lea rsi, [rel buffer]               ; pointer to buffer
    mov rdx, 128                        ; number of bytes to read
    syscall                             ; invoke syscall

    ; Check if read failed
    cmp rax, -1
    je  error                           ; Jump to error if failed

    ; Store the number of bytes read in rdi for writing later
    mov [bytes_read], al                ; Store number of bytes read in memory

    ; 3. Write the content to stdout (write syscall)
    ; rax = 1 (write)
    ; rdi = 1 (stdout)
    ; rsi = pointer to buffer
    ; rdx = number of bytes to write
    mov rax, 1                          ; syscall number for write
    mov rdi, 1                          ; stdout (file descriptor 1)
    lea rsi, [rel buffer]               ; pointer to buffer
    movzx rdx, byte [bytes_read]        ; number of bytes read
    syscall                             ; invoke syscall

    ; 4. Exit the program (exit syscall)
    ; rax = 60 (exit)
    ; rdi = exit code
    mov rax, 60                         ; syscall number for exit
    xor rdi, rdi                        ; exit code 0
    syscall                             ; invoke syscall

error:
    ; Error handling, exit with status code 1
    mov rax, 60                         ; syscall number for exit
    mov rdi, 1                          ; exit code 1
    syscall                             ; invoke syscall
