#!/bin/python
def rol(n, k):
  k %= 64  # Handle rotations beyond 64 bits
  return ((n << k) | (n >> (64 - k))) & 0xFFFFFFFFFFFFFFFF

def ror(n, k):
  k %= 64  # Handle rotations beyond 64 bits
  return ((n >> k) | (n << (64 - k))) & 0xFFFFFFFFFFFFFFFF

data =0x7ffff7ddb740
a = rol(data,0x11)
a = a ^ 0x4ebba282612d1eff
print("result: ")
print(hex(a))
print("try to do again:")
b = a ^ 0x4ebba282612d1eff
b = ror(b,0x11)
print("result: ")
print(hex(b))
