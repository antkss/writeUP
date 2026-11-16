
section .data
    dir_path db "home/as/cac", 0
    buf_size equ 1024
    buf resb buf_size

section .text
    global _start

_start:
    ; Open the directory
    mov rdi, dir_path
    mov rax, 2          ; syscall number for open
    mov rdx, 0          ; flags (O_RDONLY)
    syscall
    mov rsi, rax        ; save the file descriptor

    ; Read directory entries
read_entries:
    mov rdi, rsi        ; file descriptor
    mov rdx, buf_size   ; buffer size
    mov rax, 78         ; syscall number for getdents
    lea rdi, [buf]      ; buffer address
    syscall

    test rax, rax
    jle close_directory ; if rax <= 0, end of directory

    ; Process directory entries
    mov rsi, buf        ; pointer to the buffer
process_entries:
    mov rdx, [rsi]      ; get d_reclen
    add rsi, rdx        ; move to the next entry
    test rdx, rdx
    jz read_entries     ; if d_reclen is 0, end of entries

    ; Do something with the entry, e.g., print the names
    mov rdi, 1          ; file descriptor for stdout
    mov rax, 1          ; syscall number for write
    lea rdx, [rsi + 24] ; pointer to d_name (offset 24 in the struct)
    mov rcx, 255        ; maximum length of the file name
    syscall
    jmp process_entries

close_directory:
    ; Close the directory
    mov rdi, rsi        ; file descriptor
    mov rax, 3          ; syscall number for close
    syscall

    ; Exit
    mov rax, 60         ; syscall number for exit
    xor rdi, rdi        ; exit code 0
    syscall
