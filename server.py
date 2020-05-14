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

room_id = {}                 #dict id room dengan conn playernya
usernamelist= {}    #dict id room dengan usernamenya
user_username = {}          #dict conn dengan usernamenya

array_conn = []
LISTGROUP = []
def clientthread(conn, addr):
    while True:
        try:
            message = conn.recv(2048).decode()
        
            if 'CREATE' in message:
                id_room = message.split(' ')[1]
                user_name= message.split(' ')[2]
                print("id_room: " + str(id_room))
                temp = []
                temp.append(conn)
                room_id.update({str(id_room):temp})
                temp = []
                temp.append(user_name)
                usernamelist[id_room] = temp
                user_username[user_name]=str(conn)
                print("Room_id dict: " + str(room_id.keys()))
                response_message = "berhasil"

                stat = conn.send(response_message.encode())
                if stat <0:
                    print("berhasil")                 
                else:
                    print('gagal')
              
              

            elif 'JOIN' in message:
                N = 2
                res = message.split(' ')[N-1] 
                print(res)
                if res in room_id:
                    room_id[res].append(conn)
                    print(len(room_id[res]))
                    for clients in list_of_clients:
                        print(clients, conn)
                        if clients == conn:
                            try:
                                print("dikirim")
                                berhasil = "berhasil"
                                clients.send(berhasil.encode())
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
                # print(conn)
                print(usernamelist)
                isi = range(len(valuess))
                #cek room
                for i in isi:
                    if conn in valuess[i]:
                        room_key = key[i]
                #cek sudah dipakai atau belum
                #key = list(usernamelist[room_key].keys())
                if res not in usernamelist[room_key]:        
                    status =1
                else:
                    status = 0

                print(status)
                if status==1:
                    print("check")
                    # user_username[res] = str(conn)
                    print("tidak ada uname", addr)
                    for clients in list_of_clients:
                        print(clients, conn)
                        if clients == conn:
                            try:
                                #masukin ke daftar nama di suatu room
                                usernamelist[room_key].append(res)
                                #masukin ke dict :nama dengan client
                                user_username[res]=conn
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

#            if message:
                # print('<'+addr[0]+'>' + str(message))
                # print (room_id)
                # print (room_key)
#                message_to_send = '<' + addr[0] + '>' + str(message)
#                broadcast(message_to_send, conn)
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