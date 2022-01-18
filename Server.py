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
    threaded_client.name = connection.recv(2048)
    print("\nClient name: " + str(threaded_client.name.decode('utf-8')))
    while True:
        whatToDo=0
        whatToDo = connection.recv(2048)
       
        if whatToDo.decode('utf-8') == "1" :
            domandList = [0, 6, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72]
            i = 0
            while i < 10 :
                    i = i +1
                    with open(os.path.join('Files','domande.txt')) as f:
                        mylist = list(f)
                    c = random.choice(domandList)
                    domandainvio = mylist[c]
                    domandList.remove(c)
                    connection.send(domandainvio.encode('utf-8'))
                    b = c
                    for x in range(4):
                            b= b +1
                            inviorisposta = mylist[b]
                            print(inviorisposta + str(x))
                            connection.send(inviorisposta.encode('utf-8'))
                    veraRisp = mylist[c+5]
                    b = c
                    controlloRisp = connection.recv(2048)
                    if controlloRisp.decode('utf-8') == veraRisp:
                        connection.send(str.encode("Giusto"))
                    elif controlloRisp.decode('utf-8') != veraRisp:
                        connection.send(str.encode("Falso"))  
        
        elif whatToDo.decode('utf-8') == "3" :
            file = open(os.path.join('Files',"score.txt"),"r")
            readthefile = file.readlines()
            sortedData = sorted(readthefile,reverse=True)
            for line in range(3):
                classifica = str(sortedData[line].replace(',',''))
                connection.send(classifica.encode('utf-8'))



while True:
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount) )
ServerSocket.close()