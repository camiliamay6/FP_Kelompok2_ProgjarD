import socket
import select
import sys
import msvcrt
import string
import random
import threading
#thread
from threading import Thread
#FTP
from ftplib import FTP
from tkinter import *
from tkinter.ttk import *

#konfigurasi dengan server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.settimeout(10)
ip_address = '127.0.0.1'
port = 8081
server.connect((ip_address, port))
sockets_list =  []
join = 0
uname = 0
namaclient = "default"

class Window(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)               
       
        container = Frame(self)
        user_input= StringVar()
        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        #setiap kelas frame masukin ke dalam kurung sini ya
        for F in (CreateRoom_frame, JoinRoom_frame, Main_Menu, EnterUserName_frame, NotFound_frame, PlayMode_frame):
            frame = F(container, self)
            self.frames[F]=frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(Main_Menu)

    #show frame    
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def create_msg(self, id_room, username):
        create_message = "CREATE " + id_room + ' ' + username
        print(username)
        global namaclient
        namaclient = username

        server.send(create_message.encode())
        message = server.recv(1024).decode()
        print(message)
        if message == 'berhasil':
            print('berhasil')
            frame = self.frames[PlayMode_frame]
            frame.tkraise()
        else: 
            frame = self.frames[NotFound_frame]
            frame.tkraise()
            
        #    frame = self.frames[JoinRoom_frame]
        #    frame.tkraise()
            # join_message = username +" JOIN " + id_room
            # server.send(join_message.encode())
            # join_response_message = server.recv(1024).decode()
            # if join_response_message == username + ' joined':
            #     join = 1
            #     frame = self.frames[PlayMode_frame]
            #     frame.tkraise()


    #fungsi join
    def Join_msg(self, konten):
        #dari entry ambil valuenya
        join_id = "JOIN " + konten
        
        print(konten)
        server.send(join_id.encode())
        message = server.recv(1024).decode()
        if message == 'berhasil':
            frame = self.frames[EnterUserName_frame]
            frame.tkraise()
        else:
            frame = self.frames[NotFound_frame]
            frame.tkraise()

    
    #fungsi enter username
    def Uname_msg(self, konten):
        uname_id = "UNAME " + konten

        print(konten)
        global namaclient 
        namaclient = konten
        server.send(uname_id.encode())
        print("ngirim ke server...")
        message = server.recv(1024).decode()
        if message == 'berhasil':
            frame = self.frames[PlayMode_frame]
            frame.tkraise()
        else:
            frame = self.frames[NotFound_frame]
            frame.tkraise()


    # generate random string
    def randomKey(self, entry):
        entry.delete(0, END)
        lettersAndDigits = string.ascii_letters + string.digits
        return ''.join((random.choice(lettersAndDigits) for i in range(5)))

    # masukin kode
    def generateKode(self, entry): 
        password1 = self.randomKey(entry) 
        entry.insert(10, password1) 
    
    # receive message dari server
    def receive(self, entry):
        while True:
            try:
                msg = server.recv(1024).decode()
                print(str(msg))
                entry.insert(END, msg)
            except OSError:  # Possibly client has left the chat.
                break

    # send message ke chat
    def send(self,entry,entry2 , msg):
        msgchat = "KIRIMCHAT"+"////" + namaclient + ": " + msg
        msgchat2 = namaclient + ": " + msg
        print(msgchat)
        entry.insert(END, msgchat2)
        entry2.delete(0, END)
        server.send(msgchat.encode())
        
#Buat halaman Main Menu
class Main_Menu(Frame):
     def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Main Menu")
        label.pack(pady=10,padx=10)
            
        b_new_room = Button(self, text="Create New Room", command=lambda: controller.show_frame(CreateRoom_frame))
        b_new_room.pack()
            
        b_join_room = Button(self, text="Join room", command=lambda: controller.show_frame(JoinRoom_frame))
        b_join_room.pack()   
        
#Buat room baru
class CreateRoom_frame(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        b_mainmenu = Button(self, text="Back", command=lambda: controller.show_frame(Main_Menu))
        b_mainmenu.pack(pady=15, padx=15)
        
        label = Label(self, text="Berikut id Room anda")
        label.pack(pady=10,padx=10)
        
        Room_number = Entry(self)
        Room_number.pack(pady=15,padx=15)   

        b_generate = Button(self, text="Generate", command=lambda: controller.generateKode(Room_number))
        b_generate.pack(pady=15, padx=15)   

        label_name = Label(self, text="Masukkan Username anda")
        label_name.pack(pady=10,padx=10)

        username = Entry(self)
        username.pack(pady=15,padx=15)
        
        

        b_create = Button(self, text="Create", command=lambda: controller.create_msg(Room_number.get(), username.get()))
        b_create.pack(pady=15, padx=15)
        
#Menu Join
class JoinRoom_frame(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        b_mainmenu = Button(self, text="Back", command=lambda: controller.show_frame(Main_Menu))
        b_mainmenu.pack(pady=15, padx=15)
        
        label = Label(self, text="Masukan id Ruangan")
        label.pack(pady=10,padx=10)
        
        room_number_input=Entry(self)
        room_number_input.pack()
        
        b_join_room = Button(self, text="Next", command=lambda: controller.Join_msg(room_number_input.get()))
        b_join_room.pack()
       
        
#Menu masuan Username
class EnterUserName_frame(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        b_mainmenu = Button(self, text="Back", command=lambda: controller.show_frame(Main_Menu))
        b_mainmenu.pack(pady=15, padx=15)

        label = Label(self, text="Masukan Username")
        label.pack(pady=10,padx=10)

        username_input=Entry(self, text="masukan username")
        username_input.pack()
        

        b_start = Button(self, text="Enter", command=lambda: controller.Uname_msg(username_input.get()))
        b_start.pack()

class NotFound_frame(Frame):
    def __init__(self,parent, controller):
        Frame.__init__(self,parent)
        label = Label(self, text="Room Tidak Ditemukan :(")
        label.pack(pady=20,padx=20)

class PlayMode_frame(Frame):
     def __init__(self, parent, controller):
         Frame.__init__(self, parent)
         label = Label(self, text="Ini chat room")
         label.pack(pady=10,padx=10)

         scrollbar = Scrollbar(self)  # To navigate through past messages.
         # Following will contain the messages.
         msg_list = Listbox(self, height=15, width=50, yscrollcommand=scrollbar.set)
         scrollbar.pack(side=RIGHT, fill=Y)
         msg_list.pack(side=LEFT, fill=BOTH)
         msg_list.pack()

         messagechat = Entry(self)
         messagechat.pack(pady=15,padx=15)

         #t1 = threading.Thread(target=controller.receive, args=[msg_list])
         #t1.start()
         #t1.join()
         
         
         #coba-coba
         #while True:
             #    sockets_list = [server]
             #    read_socket = select.select(sockets_list, [],[], 3)[0]
             
             #    if msvcrt.kbhit():
                 #        read_socket.append(sys.stdin)
                 
                 #   for socks in read_socket:
                     #        if socks == server:
                         #            message = socks.recv(2048).decode()
                         #            sys.stdout.write(message)
                         
                         #           
        #       else:
                    #message = sys.stdin.readline()
                    #server.send(message.encode())
                    #sys.stdout.write('<You>')
                    #sys.stdout.write(message)
                    #sys.stdout.flush()

         send_button = Button(self, text="Send", command=lambda: controller.send(msg_list, messagechat, messagechat.get()))
         send_button.pack()
        
        
app = Window()
app.geometry("500x500")
app.mainloop()


            
server.close()
            
