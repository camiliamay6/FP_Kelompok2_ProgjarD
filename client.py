import socket
import select
import sys
import msvcrt
#FTP
from ftplib import FTP
from tkinter import *

class Window(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)               
       
        container = Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        
        for F in (CreateRoom_frame, JoinRoom_frame):
            frame = F(container, self)
            self.frames[F]=frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(Main_Menu)
    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()
#Buat halaman Main Meny
class Main_Menu(Frame):
     def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Main Menu")
        label.pack(pady=10,padx=10)
            
        b_new_room = Button(self, text="Create New Room", command=lambda: controller.show_frame(CreateRoom_frame))
        b_new_room.pack()
            
        b_join_room = Button(self, tect="Join room", command=lambda: controller.show_frame(JoinRoom_frame))
        b_join_room.pack()        
    #Buat room baru
class CreateRoom_frame(Frame):
     def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Main Menu")
        label.pack(pady=10,padx=10)
            
        b_new_room = Button(self, text="Create New Room", command=lambda: controller.show_frame(CreateRoom_frame))
        b_new_room.pack()
            
        b_join_room = Button(self, text="Join room", command=lambda: controller.show_frame(JoinRoom_frame))
        b_join_room.pack()
 #Menu utama
class JoinRoom_frame(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Main Menu")
        label.pack(pady=10,padx=10)
        
        b_new_room = Button(self, text="Create New Room", command=lambda: controller.show_frame(CreateRoom_frame))
        b_new_room.pack()
            
        b_join_room = Button(self, text="Join room", command=lambda: controller.show_frame(JoinRoom_frame))
        b_join_room.pack()
        
        
app = Window()
app.mainloop()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_address = '127.0.0.1'
port = 8081
server.connect((ip_address, port))
sockets_list =  []
#main program
root.mainloop()

while True:
    sockets_list = [server]
    read_socket = select.select(sockets_list, [],[], 3)[0]
    
    if msvcrt.kbhit():
        read_socket.append(sys.stdin)
    
    for socks in read_socket:
        if socks == server:
            message = socks.recv(2048).decode()
            sys.stdout.write(message)
                 
            
        else:
            message = sys.stdin.readline()

            if message == "LIST\n":
                print('current working directory' + f.pwd())
                names = f.dir()
                print('list of directory : ' +str(names))
        
            elif message == "PWD\n":
                print('Folder sekarang' + f.pwd())
                
            elif message == "CD\n":
                dirname = str(raw_input("Masukan nama folder tujuan: "))
                f.cwd(dirname)
        
            elif message =="MKDIR\n":
                dirname = str(raw_input("Masukan nama folder : "))
                f.mkd(dirname)
                file = []
                f.retrlines('LIST', file.append)
                for f1 in file:
                    print(f1) 
                    
            elif message == "SENDALL\n":
                print("kodingan sendal\n")
                
            elif message == "DOWNZIP\n":
                print("kodingan downzip\n")
                
                    
            else:            
                server.send(message.encode())
                sys.stdout.write('<You>')
                sys.stdout.write(message)
                sys.stdout.flush()
            
server.close()
            
