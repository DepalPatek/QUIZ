import socket
import os
from _thread import *
import random
import time

ServerSocket = socket.socket() #dichiarazione della variabile ServerSocket come socket
host = 'localhost' #dichiaro l'ip (localhost) utilizzato per il socket
port = 6716 #porta su cui il client deve connettersi
ThreadCount = 0 
try:
    ServerSocket.bind((host, port)) #creazione del socket
except socket.error as e:
    print(str(e))

print('Waiting for a Connection..') # attesa di una connessione di un client
ServerSocket.listen(5)


def threaded_client(connection):
    threaded_client.name = connection.recv(2048) #ricevo il nickname dal client
    
    file = open(os.path.join('Files',"score.txt"),"r") #file aperto in modalita read
    checklist = file.readlines() #inserisco ogni riga del fine in una list
    while any(str(threaded_client.name.decode('utf-8').upper()) in s for s in checklist) : #controllo del nickname se già stato inserito
        teprego = "1"
        connection.send(teprego.encode('utf-8'))
        threaded_client.name = connection.recv(2048)
    teprego = "0"
    connection.send(teprego.encode('utf-8'))
    file.close()

    print("\nClient name: " + str(threaded_client.name.decode('utf-8').upper()))
    while True: #loop infinito per tenere il server sempre in ascolto
        whatToDo = 0 #variabile che conterrà la scelta dell'utente nel menù
        whatToDo = connection.recv(2048) 
        if whatToDo.decode('utf-8') == "1" : #partita Classificata
            domandList = [0, 6, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72, 78, 84, 90, 96, 102, 108, 114, 120, 126, 132, 138, 144, 150, 156, 162, 168, 174, 180, 186, 192, 198, 204, 210, 216, 222, 228, 234]
            i = 0
            while i < 10 : #loop per mandare al client 10 domande e 40 risposte
                    i = i +1
                    with open(os.path.join('Files','PartitaRapida.txt')) as f:
                        mylist = list(f)
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
            score = connection.recv(2048)
            score = score.decode('utf-8')       
            name= str(threaded_client.name.decode('utf-8'))
            name = name.upper()
            file = open(os.path.join('Files',"score.txt"),"a")
            file.write(str(score)+","+name+"\n")
            file.close() 
                        
        elif whatToDo.decode('utf-8') == "2" : #partita per argomento
            time.sleep(0.01)
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
            while i < 10 : #loop per inviare 10 domande e 40 risposte
                    i = i + 1
                    c = random.choice(domandList)
                    domandainvio = listaGeneri[c]
                    domandList.remove(c)
                    time.sleep(0.01)
                    connection.send(domandainvio.encode('utf-8'))
                    b = c
                    for x in range(4):
                            b= b +1
                            inviorisposta = listaGeneri[b]
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

        elif whatToDo.decode('utf-8') == "3" : #Classifica
            file = open(os.path.join('Files',"score.txt"),"r")
            readthefile = file.readlines()
            sortedData = sorted(readthefile,reverse=True)
            for line in range(3):
                classifica = str(sortedData[line])
                connection.send(classifica.encode('utf-8'))
                time.sleep(0.2)



while True: #Creazione di più client
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount) )
ServerSocket.close()
