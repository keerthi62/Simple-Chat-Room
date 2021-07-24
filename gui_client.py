import socket
import threading
import tkinter
from tkinter.constants import S
import tkinter.scrolledtext
from tkinter import Text, simpledialog
from tkinter import filedialog
import time
import os
import json
from cryptography.fernet import Fernet

def write_key():
    
    key = Fernet.generate_key()
    with open("key.text", "wb") as key_file:
        key_file.write(key)
    
def load_key():
    
    #Loads the key from the current directory named `key.key`
    
    return open("key.text", "rb").read()

write_key()
key = load_key() 
print(key)
fernet = Fernet(key)


HOST = '127.0.0.1'
PORT = 5555

class Client :
    def __init__(self,host,port):
        
        self.sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        self.sock.connect((host , port))

        msg = tkinter.Tk()
        msg.withdraw()


        self.nickname = simpledialog.askstring("Nickname","Please choose a nickname", parent =msg)

        if self.nickname == 'admin':
            self.password = simpledialog.askstring("Password","Please enter a password", parent =msg)

        self.gui_done = False
        self.running = True

        self.stop_thread = False



        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)

        gui_thread.start()
        receive_thread.start()

    def gui_loop(self):
        self.win = tkinter.Tk()
        self.frame=tkinter.Frame(self.win)
        self.frame.pack()
        self.win.configure(bg='gray60')
        self.frame.configure(bg='gray60')

        self.win.title(f'Client Window: {self.nickname}')
        
        self.chat_label =tkinter.Label(self.win , text="Chat:" , bg="gray60")
        self.chat_label.config(font=("Arial",12))
        self.chat_label.pack(padx=20,pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win , bg="gray80")
        self.text_area.pack(padx=20,pady=15)
        self.text_area.config(state='disabled')

        self.upload_button = tkinter.Button(self.frame , text='Upload',command=self.write , bg="gray95")
        self.upload_button.config(font=("Arial",12))
        self.upload_button.pack(side=tkinter.LEFT,padx=0,pady=5)

        self.download_button = tkinter.Button(self.frame , text='Download',command=self.write , bg="gray95")
        self.download_button.config(font=("Arial",12))
        self.download_button.pack(side=tkinter.RIGHT, padx=90,pady=5)

        self.msg_label =tkinter.Label(self.win , text="Message:" , bg="gray60")
        self.msg_label.config(font=("Arial",12))
        self.msg_label.pack(padx=20,pady=5)

        self.input_area =tkinter.Text(self.win,height=3 , bg="gray80")
        self.input_area.pack(padx=2,pady=5)

        self.send_button = tkinter.Button(self.win , text='send',command=self.write , bg="gray95")
        self.send_button.config(font=("Arial",12))
        self.send_button.pack(padx=20,pady=5)

        self.gui_done=True

        self.win.protocol("WM_DELETE_WINDOW",self.stop)

        self.win.mainloop()
    
    def write(self): 
        if self.stop_thread == False:
            message = f"{self.nickname}:{self.input_area.get('1.0','end')}"
            if message[len(self.nickname)+1:].startswith('/'):
                    #username: /action 
                if self.nickname == 'admin':
                    if message[len(self.nickname)+1:].startswith('/kick'):
                        msg = f'KICK {message[len(self.nickname)+1+6:]}'.encode('utf-8')
                        encMessage= fernet.encrypt(msg)
                        self.sock.send(encMessage)
                    elif message[len(self.nickname)+1:].startswith('/ban'):
                        msg = f'BAN {message[len(self.nickname)+1+5:]}'.encode('utf-8')
                        encMessage= fernet.encrypt(msg)
                        self.sock.send(encMessage)
                else:
                    msg = 'actions only done by admin'.encode('utf-8')
                    encMessage= fernet.encrypt(msg)
                    self.sock.send(encMessage)
            else:
                msg = message.encode('utf-8')
                encMessage= fernet.encrypt(msg)
                print(encMessage)
                self.sock.send(encMessage)
            self.input_area.delete('1.0','end')

    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def UploadFun(self):
        self.filename = filedialog.askopenfilename()
        print('Selected:', filename) 

    def receive(self):
        while self.running:
            if self.stop_thread:
                break
            try:
                # Receive Message From Server
                # If 'NICK' Send Nickname
                message = self.sock.recv(1024).decode('utf-8')
                if message == "Key":
                    print(key)
                    self.sock.send(key)
                elif message == 'NICK':
                    self.sock.send(self.nickname.encode('utf-8'))
                    #nen rasindi 
                    next_message = self.sock.recv(1024).decode('utf-8')
                    if next_message == 'PASS':
                        self.sock.send(self.password.encode('utf-8'))
                        if self.sock.recv(1024).decode('utf-8') == 'REFUSE':
                            self.sock.send("Connection refused! Wrong Password!".encode('utf-8'))
                            self.stop_thread = True
                    elif next_message == 'BAN':
                        self.sock.send('connection refused because you were ban!'.encode('utf-8'))
                        self.sock.close()
                        self.stop_thread = True        
                    #nen rasindi iyyipoyindi
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end',message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
            except:
                # Close Connection When Error
                print("An error occured!")
                self.sock.close()
                break

cliet = Client(HOST,PORT)