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
room_id = {'123':['78987283']}
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
                    print("ada roomnya", addr)
                    for clients in list_of_clients:
                        print(clients, conn)
                        if clients == conn:
                            try:
                                print("dikirim")
                                berhasil = "berhasil"
                                clients.send(berhasil.encode())#!!!!Masih belum bisa ngirim
                                print("dikirim")
                            except:
                                    clients.close()
                                    print("gagal mengirim")
                                    remove(clients)
                else:
                    print("room belum dibuat", addr)
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
                message_to_send = '<' + addr[0] + '>' + str(message)
                broadcast(message_to_send, conn)
            else:
                remove(conn)
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