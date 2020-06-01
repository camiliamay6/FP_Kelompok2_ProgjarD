import socket
import select
import sys
import threading
import random 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ip_address = '127.0.0.1'
port = 8081
server.bind((ip_address,port))
server.listen(100)
list_of_clients = []

room_id = {}                #dict id room dengan conn playernya
usernamelist= {}            #dict id room dengan usernamenya
user_username = {}          #dict conn dengan usernamenya
list_vote = {}          
id_role_conn = []           #array isi id_room, conn, role(civ0, under1, white2), hidup/ngga
the_word = [['ayam', 'bebek'], ['singa', "macan"]]


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
                #buat array key dan nilainya
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
                    
            #pembagian role
            elif 'MULAI' in message:
                #cari id room pengirim
                print("MULAI")
                key = list(room_id.keys())
                valuess = list(room_id.values())
                isi = range(len(valuess))
                for i in isi:
                    if conn in valuess[i]:
                        #dapet id room
                        room_key = key[i]
                #hitung banyak anggota dalam room
                people = room_id[room_key]
                n_people = range(len(people))
                #pembagian = round(len(room_id[room_key]))/3
                #ambil random
                print(people)                
                word = random.choice(the_word)
                print(word)
                in_under = random.choice(people)
                in_white = random.choice(people)
                while in_white == in_under:
                    in_white = random.choise(people)
                for player in people:
                    if player == in_under:
                        und_mess = "SERVER: Undercover | " + word[1]
                        player.send(und_mess.encode())
                        print("uder sned")
                        id_role_conn.append([room_key, str(player), '1', 1])
                    elif player == in_white:
                        whi_mess = "SERVER :3"
                        player.send(whi_mess.encode())
                        print("player white")
                        id_role_conn.append([room_key, str(player), '2', 1])
                    else:                        
                        civ_mess = "SERVER: Civilians | " + word[0]
                        player.send(civ_mess.encode())
                        print("player civi")
                        id_role_conn.append([room_key, str(player), '0', 1])
                print(id_role_conn)
                
                
                #civilians
                #for i in range(pembagian):
#                    id_role_conn.append(room_key, people[i], '0')
#                    civ_mess = "civilian" + word[0]
#                    room_id[room_key][i].send(civ_mess.encode())
                #civilians
#                for i in (pembagian, pembagian+pembagian):
#                    id_role_conn.append(room_key, people[i], '1')
#                    under_mess = "undercover" + word[1]
#                    room_id[room_key][i].send(under_mess.encode())
#                for i in (pembagian*2, pembagian*3):
#                    id_role_conn.append(room_key, people[i], '2')
#                    mess = ":3"
#                    room_id[room_key][i].send(mess.encode())               
                
            # elif 'VOTE' in message:
            #     username = message.split(' ')[1]
            #     list_username = list(usernamelist.values())
            #     print(list_username)
            #     for room in usernamelist:
            #         if username in 
                    # if username in list_vote:
                    #     print(username)
                #         jumlah_vote = list_vote[username] + 1
                #         list_vote.update({str(username):jumlah_vote})
                #     else:
                #         list_vote.update({str(username):1})
                # print(list_vote)
            #kirim pesan dalam room
            elif "KIRIMCHAT" in message:
                username = message.split('/#/#/')[1]
                chat = message.split('/#/#/')[2]
                #cari username pengirim
                key = list(room_id.keys())
                valuess = list(room_id.values())
                isi = range(len(valuess))
                for i in isi:
                    if conn in valuess[i]:
                    #dapet id room
                        room_key = key[i]
                message = str(username) + ': ' + str(chat)
            #kirim pesannya
                broadcast(message, conn, room_key)
                
                                           
            #eliminasi 

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

def broadcast(message, connection, id_room):
    for clients in room_id[id_room]:
        if clients != connection:
            try:
                clients.send(message.encode())
                print("berhasil ngirim")
            except:
                print("gagal ngirim")

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)
        
while True:
    conn, addr = server.accept()
    list_of_clients.append(conn)
    print(addr[0]+' connected')
    threading.Thread(target=clientthread, args=(conn, addr)).start()

conn.close()