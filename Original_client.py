import socket
import threading
# Choosing Nickname
nickname = input("Choose your nickname: ")

#nen rasindi

if nickname == 'admin':
    password = input('ENTER PASSWORD: ')
#nen rasindi iyyipoyindi   

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 5555))

#nen rasindi
stop_thread = False
#nen rasindi iyyipoyindi

# Listening to Server and Sending Nickname
def receive():
    while True:
        #nen rasindi
        global stop_thread
        if stop_thread:
            break
        #nen rasindi iyyipoyindi
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
                #nen rasindi 
                next_message = client.recv(1024).decode('ascii')
                if next_message == 'PASS':
                    client.send(password.encode('ascii'))
                    if client.recv(1024).decode('ascii') == 'REFUSE':
                        print("Connection refused! Wrong Password!")
                        stop_thread = True
                elif next_message == 'BAN':
                    print('connection refused because you were ban!')
                    client.close()
                    stop_thread = True        
                #nen rasindi iyyipoyindi
            else:
                print(message)
        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            break

# Sending Messages To Server
def write():
    while True:
        #nen rasindi 
        if stop_thread:
            break
        #nen rasindi iyyipoyindi
        message = f'{nickname}: {input("")}'
        #nen rasindi
        if message[len(nickname)+2:].startswith('/'):
                #username: /action 
            if nickname == 'admin':
                if message[len(nickname)+2:].startswith('/kick'):
                    client.send(f'KICK {message[len(nickname)+2+6:]}'.encode('ascii'))
                elif message[len(nickname)+2:].startswith('/ban'):
                    client.send(f'BAN {message[len(nickname)+2+5:]}'.encode('ascii'))  

            else:
                print("actions only done by admin")
        else:
            #nen rasindi iyyipoyindi
            client.send(message.encode('ascii'))

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()