from cgitb import text
from string import ascii_letters
import pygame
import os
import socket
import cv2
import textwrap
import sys
import time
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1440,720     #altezza e larghezza della finestra
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) #Creo la finestra
pygame.display.set_caption("QUIZ TIME")      #nome della finestra
logo=pygame.image.load(os.path.join('Assets', 'Titolo_icona.png'))
pygame.display.set_icon(logo)       #imposto l'icona del gioco

WHITE = [255,255,255]       #COLORI
ULTRAMARINE = [122,142,205]
LIGHT_BLUE = [114,202,212]
LIGHT_PINK = [255, 174, 201]
DARK_PINK = [238, 58, 162]
GOLD = [255,215,0]
SILVER = [192,192,192]
BRONZE = [205,127,50]


SUONO_CLICK = pygame.mixer.Sound(os.path.join('Assets','click.wav'))                        #SUONI
SUONO_RISPOSTA_CORRETTA = pygame.mixer.Sound(os.path.join('Assets','risposta_giusta.wav'))
SUONO_RISPOSTA_SBAGLIATA = pygame.mixer.Sound(os.path.join('Assets','risposta_sbagliata.wav'))

FPS = 60

FONT_NEONLED = pygame.font.Font(os.path.join('Fonts','NEONLEDLight.otf'), 65) #font e grandezza dei testi
FONT_NEONLED_SMALL = pygame.font.Font(os.path.join('Fonts','NEONLEDLight.otf'), 55) #font e grandezza dei testi
FONT_NEONLED_LITTLE = pygame.font.Font(os.path.join('Fonts','NEONLEDLight.otf'), 30) #font e grandezza dei testi
FONT_NEONLED_PULSANTI = pygame.font.Font(os.path.join('Fonts','NEONLEDLight.otf'), 40) #font e grandezza dei testi
FONT_NEONLED_BIG = pygame.font.Font(os.path.join('Fonts','NEONLEDLight.otf'), 90) #font e grandezza dei testi
FONT_NEONLED_HUGE = pygame.font.Font(os.path.join('Fonts','NEONLEDLight.otf'), 120) #font e grandezza dei testi

class Game:
    def setup(self):
        self.ClientSocket = socket.socket()  #socket client
        self.host = 'localhost'
        self.port = 6716

        print("WAITING FOR CONNECTION")

        try:
            self.ClientSocket.connect((self.host, self.port))
        except socket.error as e:
            print(str(e))

        self.title()        #vado alla schermata del titolo



    def title(self):                    #funzione che gestisce la schermata del titolo
        self.clock = pygame.time.Clock()        #dichiaro il clock
        self.run= True
        self.titolo_immagine = pygame.image.load(os.path.join('Assets', 'Titolo.png'))  #importo l'immagine del titolo
        self.titolo = pygame.transform.scale(self.titolo_immagine, (452,191))       #croppo l'immagine del titolo per ridurla
        self.video = cv2.VideoCapture(os.path.join('Assets','titolo_background.mp4'))        #acquisisco il video
        self.video_lenght = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))           #acquisico la lunghezza del video
        self.UltimoFrame, self.video_immagine = self.video.read()                   #acquisico un frame
        self.video_shape = self.video_immagine.shape[1::-1]                         #ridimensiono il video
        self.count = 1                                                              #variabile che conta quanti frame sono stati visualizzati
        self.pulsante_inizia_immagine=pygame.image.load(os.path.join('Assets','PulsanteInizia.png'))
        self.pulsante_inizia_rect= pygame.Rect(WIDTH//2-130,HEIGHT//2+50, 260, 125)
        while self.run:
            self.clock.tick(FPS)    #configuro il clock a 60 fps
            for event in pygame.event.get():
                if event.type == pygame.QUIT:   #controllo se l'utente chiude la finestra
                    self.ClientSocket.close()           #chiudo il socket
                    pygame.quit()                       #chiudo il gioco
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.pulsante_inizia_rect.collidepoint(event.pos):
                        SUONO_CLICK.play()
                        self.run = False
            self.UltimoFrame, self.video_immagine = self.video.read()               #acquisico un frame
            self.count+=1
            if self.count==self.video_lenght:                                       #se il numero di frame ?? uguale alla lunghezza del video lo faccio ripartire da capo
                self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
                self.count=0
            self.drawTitle()        #disegno la finestra iniziale
        self.flag_same = False
        self.getNickname()


    def drawTitle(self):        #funzione che diegna la finestra TITOLO
        WIN.blit(pygame.image.frombuffer(self.video_immagine.tobytes(), self.video_shape, "BGR"),(0, 0))        #video
        WIN.blit(self.titolo, (WIDTH/2-226,50))                                                                 #titolo
        WIN.blit(self.pulsante_inizia_immagine,(self.pulsante_inizia_rect.x,self.pulsante_inizia_rect.y))
        pygame.display.update()





    def getNickname(self):          #funzione che gestisce l'acquisizione del nickname
        self.run = True
        self.background = pygame.image.load(os.path.join('Assets', 'background.png'))
        self.ask_nick="INSERIRE IL PROPRIO NICKNAME"
        self.txt_ask_nick=FONT_NEONLED.render(self.ask_nick, True, LIGHT_BLUE)   #converto il testo in immagine
        self.rect_txt_ask_nick = self.txt_ask_nick.get_rect(center=(WIDTH//2+75,HEIGHT//2-200)) #creo un rettangolo con cui l'utente puo interagire
        self.avanti="AVANTI"
        self.txt_avanti=FONT_NEONLED.render(self.avanti, True, LIGHT_BLUE)    #converto il testo in immagine
        self.rect_txt_avanti = self.txt_avanti.get_rect(center=(WIDTH-225,HEIGHT-125)) #creo un rettangolo con cui l'utente puo interagire
        self.rect_input_box = pygame.Rect(WIDTH //2 - 90 , HEIGHT //2 - 20, 400, 60)        #rettangolo input box
        self.input_box = ""
        self.txt_input_box = FONT_NEONLED.render(self.input_box, True, LIGHT_BLUE)        #testo all'interno dell'input box
        self.warning = "Il nickname deve contenere almeno 3 caratteri"  
        self.txt_warning = FONT_NEONLED_LITTLE.render(self.warning, True, LIGHT_BLUE)        #testo warning
        self.warning2 = "Il nickname deve contenere massimo 6 caratteri"
        self.txt_warning2 = FONT_NEONLED_LITTLE.render(self.warning2, True, LIGHT_BLUE)        #testo warning
        self.flag_warning = False                           #True = l'utente ha provato ad inserire un nick con meno di 3 caratteri
        self.flag_warning2= False                           #True = l'utente ha provato ad inserire un nick con pi?? di 6 caratteri
        self.txt_same = FONT_NEONLED_LITTLE.render("Nickname gia utilizzato",True,LIGHT_BLUE)
        while self.run:
            self.clock.tick(FPS)
            for event in pygame.event.get():        
                if event.type == pygame.QUIT:           #controlllo se il giocatore chiude la finestra
                    self.ClientSocket.close()           #chiudo il socket
                    pygame.quit()                       #chiudo il gioco
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.rect_txt_avanti.collidepoint(event.pos):    #controllo se il giocatore clicca sul testo "AVANTI"
                        if len(self.input_box)>2:               #controllo se ha scritto almeno 3 caratteri
                            self.run = False
                        else:
                            self.flag_warning = True
                            self.flag_same = False
                if event.type == pygame.KEYDOWN:                    #controllo se l'utente sta digitando
                    if event.key == pygame.K_BACKSPACE:             #controllo se vuole cancellare un carattere
                        self.input_box = self.input_box[:-1]
                    if event.key != pygame.K_RETURN and event.key != pygame.K_BACKSPACE and event.key != pygame.K_SPACE and len(self.input_box)<6: #controllo se vuole scrivere
                        self.input_box += event.unicode
                    elif event.key != pygame.K_RETURN and event.key != pygame.K_BACKSPACE and event.key != pygame.K_SPACE and len(self.input_box)==6:   #controllo se vuole scrivere ma ha gia scritto 6 caratteri
                        self.flag_warning = False
                        self.flag_warning2 = True
                        self.flag_same = False
                    if event.key == pygame.K_RETURN:             #controllo se vuole premere invio
                        if len(self.input_box)>2:               #controllo se ha scritto almeno 3 caratteri
                            self.run = False
                        else:
                            self.flag_warning2 = False
                            self.flag_warning = True
                            self.flag_same = False
                    self.txt_input_box = FONT_NEONLED_SMALL.render(self.input_box, True, LIGHT_BLUE)
            
            self.drawGetNickname()
        SUONO_CLICK.play()
        self.ClientSocket.send(str.encode(self.input_box)) #invio il nickname al server
        time.sleep(0.01)
        if self.ClientSocket.recv(2048).decode('utf-8') == "1":
            self.flag_same = True
            self.getNickname()
        else:
            self.menuPrincipale()



    def drawGetNickname(self):      #funzione che disegna la finestra GETNICKNAME
        WIN.blit(self.background, (0,0))       #colore del background
        WIN.blit(self.txt_ask_nick, self.rect_txt_ask_nick)     #testo che chiede il nickname
        WIN.blit(self.txt_avanti, self.rect_txt_avanti)         #testo "AVANTI"
        self.rect_input_box.w = max(200,self.txt_input_box.get_width()+10)      #aggiorno la lunghezza della box in base alla lunghezza del nick
        WIN.blit(self.txt_input_box,(self.rect_input_box.x+5, self.rect_input_box.y+10))          #testo input box
        pygame.draw.rect(WIN, LIGHT_BLUE, self.rect_input_box, 5)                #input box
        if self.flag_warning == True:       #se ha scritto meno di tre caratteri mostro il messaggio
            WIN.blit(self.txt_warning, (self.rect_input_box.x-175, self.rect_input_box.y-50))
        if self.flag_warning2 == True:
            WIN.blit(self.txt_warning2,(self.rect_input_box.x-175, self.rect_input_box.y-50))
        if self.flag_same == True:
            WIN.blit(self.txt_same,(self.rect_input_box.x-50, self.rect_input_box.y-50))
        pygame.display.update()




    def menuPrincipale(self):           #funzione che gestisce il menu principale
        self.run = True
        self.puls_gioca_pers = Pulsanti(480,325,"PARTITA PER ARGOMENTO",480+35,325+18)     #pulsante partita personalizzata
        self.puls_gioca_vel = Pulsanti(480,225,"PARTITA CLASSIFICATA",480+65,225+18)             #pulsante partita veloce
        self.puls_class = Pulsanti(480,425,"CLASSIFICA",480+180,425+18)                     #pulsante classifica
        self.puls_esci = Pulsanti(480,525,"ESCI",480+240,525+18)                            #pulsante esci
        self.puls_ind = PulsanteIndietro()                  #pulsante indietro (utilizzato successivamente)
        self.risp=0
        self.ranked = False

        while self.run:
            self.clock.tick(FPS)               
            for event in pygame.event.get():        
                if event.type == pygame.QUIT:           #controlllo se il giocatore chiude la finestra
                    self.ClientSocket.close()           #chiudo il socket
                    pygame.quit()
                if self.puls_esci.premuto(event) == True:                     #chiudo il gioco se l'utente clicca sul pulsante esci
                    self.ClientSocket.close()           #chiudo il socket
                    pygame.quit()
                if self.puls_class.premuto(event) == True:      #controllo se l'utente clicca sulla classifica
                    self.run = False
                    self.risp="3"
                    self.ClientSocket.send(str.encode(self.risp))
                    self.classifica()
                if self.puls_gioca_vel.premuto(event) == True:      #controllo se l'utente vuole fare una partita veloce
                    self.run = False
                    self.round=0
                    self.score=0
                    self.ranked = True
                    self.risp="1"
                    self.ClientSocket.send(str.encode(self.risp))
                    self.partitaVeloce()
                if self.puls_gioca_pers.premuto(event) == True:      #controllo se l'utente vuole fare una partita personalizzata
                    self.run = False
                    self.risp="2"
                    self.score = 0
                    self.round=0
                    self.ranked = False
                    self.ClientSocket.send(str.encode(self.risp))
                    self.scegliCategoria()
            self.puls_gioca_pers.mouseSopra()           #controllo se il giocatore ha il mouse sopra il pulsante partita personalizzata
            self.puls_gioca_vel.mouseSopra()            #controllo se il giocatore ha il mouse sopra il pulsante partita veloce
            self.puls_class.mouseSopra()                #controllo se il giocatore ha il mouse sopra il pulsante classifica
            self.puls_esci.mouseSopra()                 #controllo se il giocatore ha il mouse sopra il pulsante esci
            self.drawMenuPrincipale()


    def drawMenuPrincipale(self):       #funzione che disegna la finestra MENUPRINCIPALE
        WIN.blit(self.background, (0,0))            #disegno lo sfondo
        WIN.blit(self.titolo, (WIDTH/2-175,20))        #disegno il titolo
        self.puls_gioca_pers.drawButton()           #disegno il pulsante partita veloce
        self.puls_gioca_vel.drawButton()            #disegno il pulsante partita personalizzata
        self.puls_class.drawButton()                #disegno il pulsante classifica
        self.puls_esci.drawButton()                 #disegno il pulsante esci
        pygame.display.update()




    def classifica(self):           #funzione che mostra la classifica
        self.run = True
        self.top_1=self.ClientSocket.recv(2048).decode('utf-8')             #acquisisco il primo classificato dal server
        print(self.top_1, flush=True)   
        self.top_1=str(self.top_1)                                          #converto il messaggio in stringa
        self.top_1=self.top_1.split(',')                                    #divido la stringa in score/nome
        self.score_1=self.top_1[0]                                          #acquisisco lo score separatamente
        self.name_1=self.top_1[1]                                           #acquisisco il nome separatamente
        self.top_2=self.ClientSocket.recv(2048).decode('utf-8')             #acquisisco il secondo classificato dal server
        print(self.top_2, flush=True)
        self.top_2=str(self.top_2)
        self.top_2=self.top_2.split(',')
        self.score_2=self.top_2[0]
        self.name_2=self.top_2[1]
        self.top_3=self.ClientSocket.recv(2048).decode('utf-8')             #acquisisco il terzo classificato dal server
        print(self.top_3, flush=True)
        self.top_3=str(self.top_3)
        self.top_3=self.top_3.split(',')
        self.score_3=self.top_3[0]
        self.name_3=self.top_3[1]
        self.messaggio = "TOP 3"
        self.txt_mess = FONT_NEONLED_HUGE.render(self.messaggio,True, LIGHT_PINK)
        self.leaderboard_img = pygame.image.load(os.path.join('Assets','leaderboard.png'))
        while self.run:
            self.clock.tick(FPS)
            for event in pygame.event.get():        
                if event.type == pygame.QUIT:           #controlllo se il giocatore chiude la finestra
                    self.ClientSocket.close()           #chiudo il socket
                    pygame.quit()
                if self.puls_ind.premuto(event) == True:
                    self.run = False
                    self.menuPrincipale()
            self.puls_ind.mouseSopra()
            self.drawClassifica()


    def drawClassifica(self):
        WIN.blit(self.leaderboard_img,(0,0))
        self.puls_ind.drawPuls()
        WIN.blit(self.txt_mess,(580,40))
        self.txt_score_1 = FONT_NEONLED_BIG.render(self.score_1, True, GOLD)
        WIN.blit(self.txt_score_1,(500, 250))
        self.txt_name_1 = FONT_NEONLED_BIG.render(self.name_1, True, GOLD)
        WIN.blit(self.txt_name_1,(800, 250))
        self.txt_score_2 = FONT_NEONLED_BIG.render(self.score_2, True, SILVER)
        WIN.blit(self.txt_score_2,(500, 375))
        self.txt_name_2 = FONT_NEONLED_BIG.render(self.name_2, True, SILVER)
        WIN.blit(self.txt_name_2,(800, 375))
        self.txt_score_3 = FONT_NEONLED_BIG.render(self.score_3, True, BRONZE)
        WIN.blit(self.txt_score_3,(500, 500))
        self.txt_name_3 = FONT_NEONLED_BIG.render(self.name_3, True, BRONZE)
        WIN.blit(self.txt_name_3,(800, 500))
        pygame.display.update()






    def partitaVeloce(self):           #funzione che fa partire la partita veloce
        self.run = True
        self.getDalServer()     #prendo le domande dal server
        self.template_quiz_img = pygame.image.load(os.path.join('Assets','template_quiz.png'))
        self.puls_a = Pulsanti(150,400,self.risp_a[0],442-(len(self.risp_a[0])*12),400+18)  #creo il primo pulsante
        self.puls_b = Pulsanti(150,550,self.risp_b[0],442-(len(self.risp_b[0])*12),550+18)  #creo il primo pulsante
        self.puls_c = Pulsanti(750,400,self.risp_c[0],1042-(len(self.risp_c[0])*12),400+18)  #creo il primo pulsante
        self.puls_d = Pulsanti(750,550,self.risp_d[0],1042-(len(self.risp_d[0])*12),550+18)  #creo il primo pulsante
        if self.score == 0:
            self.txt_score_str = FONT_NEONLED.render("000", True, LIGHT_BLUE)
        else:
            self.score_str = str(self.score)
            self.score_str = "0" + self.score_str
            self.txt_score_str = FONT_NEONLED.render(self.score_str, True, LIGHT_BLUE)
        self.risposta = ""
        self.risposto = False           #True = l'utente ha risposto
        self.corretto = False           #True = la risposta ?? corretta
        while self.run:
            self.clock.tick(FPS)
            for event in pygame.event.get():        
                if event.type == pygame.QUIT:           #controlllo se il giocatore chiude la finestra
                    self.ClientSocket.close()           #chiudo il socket
                    pygame.quit()
                if self.puls_a.premuto(event) == True:
                    self.risposto = True
                    self.risposta = self.risp_a[0]
                    self.controllaRisp()
                if self.puls_b.premuto(event) == True:
                    self.risposto = True
                    self.risposta = self.risp_b[0]
                    self.controllaRisp()
                if self.puls_c.premuto(event) == True:
                    self.risposto = True
                    self.risposta = self.risp_c[0]
                    self.controllaRisp()
                if self.puls_d.premuto(event) == True:
                    self.risposto = True
                    self.risposta = self.risp_d[0]
                    self.controllaRisp()
            self.puls_a.mouseSopra()
            self.puls_b.mouseSopra()
            self.puls_c.mouseSopra()
            self.puls_d.mouseSopra()
            self.drawPartitaVeloce()
            if self.risposto == True:
                self.round+=1
                if self.round < 10:
                    self.partitaVeloce()
                else:
                    self.schermataScore()


    def drawPartitaVeloce(self):
        WIN.blit(self.template_quiz_img,(0,0))
        for i in range(len(self.domanda)):
            self.txt_domanda = FONT_NEONLED_SMALL.render(self.domanda[i], True, LIGHT_BLUE)       
            WIN.blit(self.txt_domanda,(450, 275-(45*(len(self.domanda)-i+1))))
        self.puls_a.drawButton()
        self.puls_b.drawButton()
        self.puls_c.drawButton()
        self.puls_d.drawButton()
        WIN.blit(self.txt_score_str,(WIDTH-200,40))
        pygame.display.update()

    def getDalServer(self):         #funzione che prende la domanda e le risposte dal server
        time.sleep(0.01)
        self.domanda = self.ClientSocket.recv(2048).decode('utf-8')
        self.domanda = textwrap.wrap(self.domanda,width = 21)
        time.sleep(0.01)
        self.risp_a = self.ClientSocket.recv(2048).decode('utf-8')#ricevo la prima risposta dal server
        self.risp_a = textwrap.wrap(self.risp_a,width = 40)
        time.sleep(0.01)
        self.risp_b = self.ClientSocket.recv(2048).decode('utf-8')#ricevo la seconda risposta dal server
        self.risp_b = textwrap.wrap(self.risp_b,width = 40)
        time.sleep(0.01)
        self.risp_c = self.ClientSocket.recv(2048).decode('utf-8')#ricevo la terza risposta dal server
        self.risp_c = textwrap.wrap(self.risp_c,width = 40)
        time.sleep(0.01)
        self.risp_d = self.ClientSocket.recv(2048).decode('utf-8')#ricevo la quarta risposta dal server
        self.risp_d = textwrap.wrap(self.risp_d,width = 40)

    def controllaRisp(self):
        self.ClientSocket.send(str.encode(self.risposta))
        time.sleep(0.001)
        if self.ClientSocket.recv(2048).decode('utf-8') == "Giusto":
            SUONO_RISPOSTA_CORRETTA.play()
            self.score+=10
        else:
            SUONO_RISPOSTA_SBAGLIATA.play()




    def schermataScore(self):
        self.run = True
        if self.score == 0:
            self.score_str = "000"
        elif self.score == 100:
            self.score_str = "100"
        else:
            self.score_str = str(self.score)
            self.score_str = "0" + self.score_str
        self.testo_score = "hai realizzato "+self.score_str+" punti !!!"
        self.txt_testo_score = FONT_NEONLED.render(self.testo_score,True,LIGHT_BLUE)
        if self.ranked == True:
            self.ClientSocket.send(str.encode(self.score_str))
        self.continua = Pulsanti(500,400,"Continua",500+190,400+18)
        while self.run:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:           #controlllo se il giocatore chiude la finestra
                    self.ClientSocket.close()           #chiudo il socket
                    pygame.quit()
                if self.continua.premuto(event) == True:
                    self.menuPrincipale()
            self.continua.mouseSopra()
            self.drawScore()

    
    def drawScore(self):
        WIN.blit(self.background,(0,0))
        WIN.blit(self.txt_testo_score,(370,200))
        self.continua.drawButton()
        pygame.display.update()







    def scegliCategoria(self):           #funzione che fa partire la partita personalizzata facendo scegliere la categoria
        self.run = True
        self.txt_scegli_categoria = FONT_NEONLED.render("Selezionare la Categoria",True,LIGHT_BLUE)
        self.puls_storia = Pulsanti(475,200,"Storia",475+220,200+18)
        self.puls_geografia = Pulsanti(475,300,"Geografia",475+170,300+18)
        self.puls_informatica = Pulsanti(475,400,"Informatica",475+160,400+18)
        self.puls_scienze = Pulsanti(475,500,"Scienze",475+200,500+18)
        self.categoria = ""
        while self.run:
            self.clock.tick(FPS)
            for event in pygame.event.get():        
                if event.type == pygame.QUIT:           #controlllo se il giocatore chiude la finestra
                    self.ClientSocket.close()           #chiudo il socket
                    pygame.quit()
                if self.puls_scienze.premuto(event) == True:
                    self.categoria = "1"
                    self.ClientSocket.send(str.encode(self.categoria))
                    time.sleep(0.01)
                    self.partitaVeloce()
                if self.puls_informatica.premuto(event) == True:
                    self.categoria = "2"
                    self.ClientSocket.send(str.encode(self.categoria))
                    time.sleep(0.01)
                    self.partitaVeloce()
                if self.puls_geografia.premuto(event) == True:
                    self.categoria = "3"
                    self.ClientSocket.send(str.encode(self.categoria))
                    time.sleep(0.01)
                    self.partitaVeloce()
                if self.puls_storia.premuto(event) == True:
                    self.categoria = "4"
                    self.ClientSocket.send(str.encode(self.categoria))
                    time.sleep(0.01)
                    self.partitaVeloce()
            self.puls_scienze.mouseSopra()
            self.puls_storia.mouseSopra()
            self.puls_geografia.mouseSopra()
            self.puls_informatica.mouseSopra()
            self.drawScegliCategoria()


    def drawScegliCategoria(self):
        WIN.blit(self.background,(0,0))
        WIN.blit(self.txt_scegli_categoria,(350,110))
        self.puls_storia.drawButton()
        self.puls_geografia.drawButton()
        self.puls_informatica.drawButton()
        self.puls_scienze.drawButton()
        pygame.display.update()







class PulsanteIndietro:                 #classe che gestisce il pulsante torna indietro
    def __init__(self):
        self.rect = pygame.Rect(220,40,100,100)
        self.puls_acceso = pygame.image.load(os.path.join('Assets','PulsanteIndietroAcceso.png'))
        self.puls_spento = pygame.image.load(os.path.join('Assets','PulsanteIndietroSpento.png'))

    def mouseSopra(self):                   #controllo se il mouse ?? sopra il pulsante
        self.sopra=False
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.sopra = True
    
    def drawPuls(self):               #disegno il pulsante a seconda se il mouse ?? sopra o no
        if self.sopra == True:
            WIN.blit(self.puls_spento,(self.rect.x, self.rect.y))
        else:
            WIN.blit(self.puls_acceso,(self.rect.x,self.rect.y))
    
    def premuto(self,event):            #vedo se ?? premuto
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                SUONO_CLICK.play()
                return True
        else:
            return False


class Pulsanti:             #classe che gestisce i pulsanti

    def __init__(self,x,y,testo,testox,testoy):           #costruttore
        self.rect = pygame.Rect(x,y,585,70)    #creo il rettangolo
        self.testo_spento = FONT_NEONLED_PULSANTI.render(testo, True, DARK_PINK)   #creo il Testo al suo interno
        self.testo_acceso = FONT_NEONLED_PULSANTI.render(testo, True, LIGHT_PINK)   #creo il Testo al suo interno
        self.img_acceso = pygame.image.load(os.path.join('Assets', 'PulsanteSelezioneAcceso.png')) #pulsante di default
        self.img_spento = pygame.image.load(os.path.join('Assets', 'PulsanteSelezioneSpento.png')) #pulsante con mouse sopra
        self.testox = testox
        self.testoy = testoy

    def mouseSopra(self):                   #controllo se il mouse ?? sopra il pulsante
        self.sopra=False
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.sopra = True

    def drawButton(self):               #disegno il pulsante a seconda se il mouse ?? sopra o no
        if self.sopra == True:
            WIN.blit(self.img_spento,(self.rect.x, self.rect.y))
            WIN.blit(self.testo_acceso,(self.testox,self.testoy))
        else:
            WIN.blit(self.img_acceso,(self.rect.x,self.rect.y))
            WIN.blit(self.testo_spento,(self.testox,self.testoy))
    
    def premuto(self,event):            #vedo se ?? premuto
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                SUONO_CLICK.play()
                return True
        else:
            return False

        





def main():
    game=Game()
    game.setup()


if __name__ == "__main__":
    main()

