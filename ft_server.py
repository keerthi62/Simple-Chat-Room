import socket
import tqdm
import os
host = "127.0.0.1"
port = 9090
bf_size = 50
splitter = " "
server = socket.socket()
server.bind((host, port))
server.listen()
print("server running")
client, address = server.accept() 
print("Connected with client!")
file_received = client.recv(bf_size).decode()
fname, fsize = file_received.split(splitter)
fname = os.path.basename(fname)
fsize = int(fsize)
file_transfer = tqdm.tqdm(range(fsize), f"Receiving {fname}", unit="B", unit_scale=True, unit_divisor=50)
with open(fname, "wb") as f:
    while 1:
        read_bits = client.recv(bf_size)
        if not read_bits:  
            break
        f.write(read_bits)
        file_transfer.update(len(read_bits))
client.close()
server.close()