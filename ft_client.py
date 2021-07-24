import socket
import tqdm
import os
splitter = " "
bf_size = 50 
fname = "edamontology/README.md"
fsize = os.path.getsize(fname)
client = socket.socket()
print("Connected to server")
client.connect(('127.0.0.1', 9090))
client.send(f"{fname}{splitter}{fsize}".encode())
file_transfer = tqdm.tqdm(range(fsize), f"Sending {fname}", unit="B", unit_scale=True, unit_divisor=50)
with open(fname, "rb") as f:
    while 1:
        read_bits = f.read(bf_size)
        if not read_bits:
            break
        client.send(read_bits)
        file_transfer.update(len(read_bits))
client.close()
