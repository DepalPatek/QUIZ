import socket
import os
from _thread import *
import random
import time

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
        whatToDo = 0
        whatToDo = connection.recv(2048)
       
        if whatToDo.decode('utf-8') == "1" :
            domandList = [0,6,12,18,24,30,36,42,48,54,60,66,72,78,84,90,96,102,108,114,120,126,132,138,144,150,156,162,168,174,180,186,192,198,204,210,216,222,228,234,240]
            i = 0
            while i < 10 :
                    i = i +1
                    with open(os.path.join('Files','Scienza.txt')) as f:
                        mylist = list(f)
                    with open(os.path.join('Files','Informatica.txt')) as f:
                        mylist = mylist.append(f)
                    with open(os.path.join('Files','Geografia.txt')) as f:
                        mylist = mylist.append(f) 
                    with open(os.path.join('Files','Storia.txt')) as f:
                        mylist = mylist.append(f)
                    c = random.choice(domandList)
                    domandainvio = mylist[c]
                    domandList.remove(c)
                    time.sleep(0.01)
                    connection.send(domandainvio.encode('utf-8'))
                    b = c
                    for x in range(4):
                            b= b +1
                            inviorisposta = mylist[b]
                            time.sleep(0.01)
                            connection.send(inviorisposta.encode('utf-8'))
                    veraRisp = mylist[c+5]
                    veraRisp = veraRisp.rstrip("\n")
                    b = c
                    controlloRisp = connection.recv(2048)
                    if controlloRisp.decode('utf-8') == veraRisp:
                        time.sleep(0.01)
                        connection.send(str.encode("Giusto"))
                    elif controlloRisp.decode('utf-8') != veraRisp:
                        time.sleep(0.01)
                        connection.send(str.encode("Falso"))  
        elif whatToDo.decode('utf-8') == "2" :
            while whatToDo2 != 0 :
                whatToDo2 = connection.recv(2048)
                if whatToDo2.decode('utf-8') == "1" :
                    with open(os.path.join('Files','Scienza.txt')) as k:
                        listaGeneri = list(k)
                elif whatToDo2.decode('utf-8') == "2" :
                    with open(os.path.join('Files','Informatica.txt')) as k:
                        listaGeneri = list(k)
                elif whatToDo2.decode('utf-8') == "3" :
                    with open(os.path.join('Files','Geografia.txt')) as k:
                        listaGeneri = list(k) 
                elif whatToDo2.decode('utf-8') == "4" :
                    with open(os.path.join('Files','Storia.txt')) as k:
                        listaGeneri = list(k)
                domandList = [0, 6, 12, 18, 24, 30, 36, 42, 48, 54]
                i = 0
                while i < 10 :
                        i = i + 1
                        c = random.choice(domandList)
                        domandainvio = listaGeneri[c]
                        domandList.remove(c)
                        time.sleep(0.01)
                        connection.send(domandainvio.encode('utf-8'))
                        b = c
                        for x in range(4):
                                b= b +1
                                inviorisposta = mylist[b]
                                time.sleep(0.01)
                                connection.send(inviorisposta.encode('utf-8'))
                        veraRisp = listaGeneri[c+5]
                        veraRisp = veraRisp.rstrip("\n")
                        b = c
                        controlloRisp = connection.recv(2048)
                        if controlloRisp.decode('utf-8') == veraRisp:
                            time.sleep(0.01)
                            connection.send(str.encode("Giusto"))
                        elif controlloRisp.decode('utf-8') != veraRisp:
                            time.sleep(0.01)
                            connection.send(str.encode("Falso"))                          

        elif whatToDo.decode('utf-8') == "3" :
            file = open(os.path.join('Files',"score.txt"),"r")
            readthefile = file.readlines()
            sortedData = sorted(readthefile,reverse=True)
            for line in range(3):
                classifica = str(sortedData[line])
                print(classifica)
                connection.send(classifica.encode('utf-8'))
                time.sleep(0.2)



while True:
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount) )
ServerSocket.close()
