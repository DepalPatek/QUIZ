import socket
import os
from _thread import *
import random

ServerSocket = socket.socket()
host = 'localhost'
port = 6716
ThreadCount = 0
flag = 0
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waiting for a Connection..')
ServerSocket.listen(5)


def threaded_client(connection):
    with open('domande.txt') as f:
        mylist = list(f)
    threaded_client.name = connection.recv(2048)
    print("\nClient name: " + str(threaded_client.name.decode('utf-8')))
    while True:
        flag = 0
        reply = random.choice(mylist)
        connection.send(str.encode(reply))
        data = connection.recv(2048)
        with open("risposte.txt", "r") as file:
            for line in file:
                line = line.split(",")
                if data.decode('utf-8') == line[0]:
                    flag = 1
                    reply = 'yay poggers'
                    connection.send(str.encode(reply))
        if flag ==0:
            reply = 'Not that poggers'
            connection.sendall(str.encode(reply))


while True:
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount) )
ServerSocket.close()
