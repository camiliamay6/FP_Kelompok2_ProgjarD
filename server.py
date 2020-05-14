import socket
import select
import sys
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ip_address = '127.0.0.1'
port = 8081
server.bind((ip_address,port))
server.listen(100)
list_of_clients = []

room_id = {'123':[]}        #dict id room dengan conn playernya
usernamelist= {'123':[]}    #dict id room dengan usernamenya
user_username = {}        #array conn dengan usernamenya
room_key=''
LISTGROUP = []
def clientthread(conn, addr):
    while True:
        try:
            message = conn.recv(2048).decode()
            
            #LISGRUP = matriks yang berisi data id_room, client_addressnya, username, dan role.
            
            #IF dipesannya ada value Create???????:
                #buat id room baru append ke matriks LISTGRUP
                #append addressnya ke matriks
                
            if 'JOIN' in message:
                N = 2
                res = message.split(' ')[N-1] 
                print(res)
                if res in room_id:
                    room_id[res].append(conn)
                    print("ada roomnya", room_id[res])
                    for clients in list_of_clients:
                        print(clients, conn)
                        if clients == conn:
                            try:
                                print("dikirim")
                                berhasil = "berhasil"
                                clients.send(berhasil.encode())
                                print("dikirim")
                            except:
                                clients.close()
                                print("gagal mengirim")
                                remove(clients)
                else:
                    print("room belum dibuat", addr)
                    conn.send("nah").encode()

            elif 'UNAME' in message:
                print("MASOKKK")
                N = 2
                res = message.split(' ')[N-1] 
                key = list(room_id.keys())
                valuess = list(room_id.values())
                print(conn)
                print(valuess)
                isi = range(len(valuess))
                print(isi)
                #cek room
                for i in isi:
                    if conn in valuess[i]:
                        room_key = key[i]
                #cek sudah dipakai atau belum
                key = list(user_username.keys())
                if res not in key:
                    status =1
                else:
                    status = 0

                print(status)
                if status==1:
                    print("check")
                    user_username[res] = conn
                    print("uname : " + room_id)
                    print("tidak ada uname", addr)
                    for clients in list_of_clients:
                        print(clients, conn)
                        if clients == conn:
                            try:
                                print("dikirim")
                                berhasil = "berhasil"
                                clients.send(berhasil.encode())
                                print("dikirim")
                            except:
                                clients.close()
                                print("gagal mengirim")
                                remove(clients)
                else:
                    print("uname dah ada", addr)
                    conn.send("nah").encode()
            
                            
            #IF dipesannya ada kata username:
                #cek ada dimana address ini
                #masukin ke matriks LISTGRUP nx4 (isinya room, address, username, role)
                
            #kalau pesan ada kata "SEBUT ":??
                #kalau belum ada:
                    #append ke dir kata['id_room']
                #kalau ada :
                    #send ke id room kalau kata udah ada
                    
            if message:
                print('<'+addr[0]+'>' + str(message))
                print (room_id)
                print (room_key)
                message_to_send = '<' + addr[0] + '>' + str(message)
                broadcast(message_to_send, conn)
            else:
                continue
        except:
            continue

def broadcast(message, connection):
    for clients in list_of_clients:
        if clients != connection:
            try:
                clients.send(message).encode()
            except:
                clients.close()
                remove(clients)

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)
        
while True:
    conn, addr = server.accept()
    list_of_clients.append(conn)
    print(addr[0]+' connected')
    threading.Thread(target=clientthread, args=(conn, addr)).start()

conn.close()