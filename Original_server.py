import socket
import threading

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

# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            #  #nen rasindi
            msg = message = client.recv(1024)
            print(msg)
            if msg.decode('ascii').startswith('KICK'):
                print(msg)
                if nicknames[clients.index(client)] == 'admin':
                    name_to_kick = msg.decode('ascii')[5:]
                    print(name_to_kick)
                    kick_user(name_to_kick)
                else:
                    client.send('command was refused'.encode('ascii'))
            elif msg.decode('ascii').startswith('BAN'):
                if nicknames[clients.index(client)] == 'admin':
                    name_to_ban = msg.decode('ascii')[4:]
                    kick_user(name_to_ban)
                    with open('bans.txt','a') as f:
                        f.write(f'{name_to_ban}\n')
                    print(f'{name_to_ban} was banned!')
                else:
                    client.send('command was refused'.encode('ascii'))

                #nen rasindi iyyipoyindi
            else:
                broadcast(message)
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break


# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode('ascii'))

        nickname = client.recv(1024).decode('ascii')

        #nen rasindi
        with open('bans.txt','r') as f:
            bans = f.readlines()

        if nickname+'\n' in bans:
            clinet.send('BAN'.encode('ascii'))
            client.close()
            continue    


        if nickname == 'admin':
            client.send('PASS'.encode('ascii'))
            password = client.recv(1024).decode('ascii')
            
            if password != 'adminpass':
                client.send('REFUSE'.encode('ascii'))
                client.close()
                continue 
        #nen rasindi iyyipoyindi     


        nicknames.append(nickname)                   
        clients.append(client)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

#nen rasindi 
def kick_user(name):
    if name in nicknames:
        name_index = nicknames.index(name)
        client_to_kick = clients[name_index]
        clients.remove(client_to_kick)
        client_to_kick.send('YOU WERE KICKED BY ADMIN!'.encode('ascii'))
        client_to_kick.close()
        nicknames.remove(name)
        broadcast(f'{name} was kicked by admin!'.encode('ascii'))
#nen rasindi iyyipoyindi

print("server is listening")
receive()