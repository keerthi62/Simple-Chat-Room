import socket
import threading
from cryptography.fernet import Fernet

# Connection Data
host = '127.0.0.1'
port = 5555

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []
banned = []

keys = []

# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            msg = client.recv(1024)
            key = keys[clients.index(client)]
            fernet = Fernet(key)
            decMessage= fernet.decrypt(msg)
            
            if decMessage.decode('utf-8').startswith('KICK'):
                if nicknames[clients.index(client)] == 'admin':
                    name_to_kick = decMessage.decode('utf-8')[5:len(decMessage)-1]
                    print(name_to_kick)
                    kick_user(str(name_to_kick))
                else:
                    client.send('command was refused'.encode('utf-8'))
            elif decMessage.decode('utf-8').startswith('BAN'):
                if nicknames[clients.index(client)] == 'admin':
                    name_to_ban = decMessage.decode('utf-8')[4:len(decMessage)-1]
                    kick_user(name_to_ban)
                    banned.append(name_to_ban)
                    client.send(f'{name_to_ban} was banned!')
                else:
                    client.send('command was refused'.encode('utf-8'))

                #nen rasindi iyyipoyindi
            else:
                broadcast(decMessage)
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('utf-8'))
            nicknames.remove(nickname)
            break


# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        
        client.send('Key'.encode('utf-8'))
        key = client.recv(1024)
        keys.append(key)

        client.send('NICK'.encode('utf-8'))

        nickname = client.recv(1024).decode('utf-8')


        if nickname in banned:
            client.send('BAN'.encode('utf-8'))
            client.close()
            continue  

        if nickname == 'admin':
            client.send('PASS'.encode('utf-8'))
            password = client.recv(1024).decode('utf-8')
            
            if password != 'adminpass':
                client.send('REFUSE'.encode('utf-8'))
                client.close()
                continue    


        nicknames.append(nickname)                   
        clients.append(client)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!\n".format(nickname).encode('utf-8'))
        client.send('Connected to server!'.encode('utf-8'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

def kick_user(name):
    if name in nicknames:
        name_index = nicknames.index(name)
        print(name_index)
        client_to_kick = clients[name_index]
        clients.remove(client_to_kick)
        client_to_kick.send('YOU WERE KICKED BY ADMIN!'.encode('utf-8'))
        client_to_kick.close()
        nicknames.remove(name)
        broadcast(f'{name} was kicked by admin!'.encode('utf-8'))
#nen rasindi iyyipoyindi

print("server is listening")
receive()