#pragma once

#include <_cheader.h>
#include <stdint.h>
#include <stddef.h>

_Begin_C_Header

extern void * memset(void * dest, int c, size_t n);
extern void * memcpy(void * dest, const void * src, size_t n);
extern void * memmove(void * dest, const void * src, size_t n);

extern void * memchr(const void * src, int c, size_t n);
extern void * memrchr(const void * m, int c, size_t n);
extern int memcmp(const void *vl, const void *vr, size_t n);

extern void * __attribute__ ((malloc)) malloc(uintptr_t size);
extern void * __attribute__ ((malloc)) realloc(void * ptr, uintptr_t size);
extern void * __attribute__ ((malloc)) calloc(uintptr_t nmemb, uintptr_t size);
extern void * __attribute__ ((malloc)) valloc(uintptr_t size);
extern void free(void * ptr);

extern char * strdup(const char * s);
extern char * stpcpy(char * d, const char * s);
extern char * strcpy(char * dest, const char * src);
extern char * strchrnul(const char * s, int c);
extern char * strchr(const char * s, int c);
extern char * strrchr(const char * s, int c);
extern char * strpbrk(const char * s, const char * b);
extern char * strstr(const char * h, const char * n);

extern char * strncpy(char * dest, const char * src, size_t n);

extern int strcmp(const char * l, const char * r);
extern int strncmp(const char *s1, const char *s2, size_t n);
extern int strcoll(const char * s1, const char * s2);

extern size_t strcspn(const char * s, const char * c);
extern size_t strspn(const char * s, const char * c);
extern size_t strlen(const char * s);

extern int atoi(const char * s);

extern char * strcat(char *dest, const char *src);
extern char * strncat(char *dest, const char *src, size_t n);

extern char * strtok(char * str, const char * delim);
extern char * strtok_r(char * str, const char * delim, char ** saveptr);

extern char * strncpy(char *dest, const char *src, size_t n);

extern char * strerror(int errnum);
extern size_t strxfrm(char *dest, const char *src, size_t n);

extern char * strsignal(int sign);
extern const char * const sys_siglist[];

_End_C_Header

#include <strings.h>
