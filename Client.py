from string import ascii_letters
import pygame
import os
import socket
import cv2
import textwrap
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1440,720     #altezza e larghezza della finestra
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) #Creo la finestra
pygame.display.set_caption("QUIZ")      #nome della finestra
logo=pygame.image.load(os.path.join('Assets', 'Titolo_icona.png'))
pygame.display.set_icon(logo)       #imposto l'icona del gioco

WHITE = [255,255,255]       #COLORI
ULTRAMARINE = [122,142,205]
LIGHT_BLUE = [114,202,212]
LIGHT_PINK = [255, 174, 201]
DARK_PINK = [238, 58, 162]

FPS = 60

FONT_NEONLED = pygame.font.Font(os.path.join('Fonts','NEONLEDLight.otf'), 65) #font e grandezza dei testi
FONT_NEONLED_SMALL = pygame.font.Font(os.path.join('Fonts','NEONLEDLight.otf'), 55) #font e grandezza dei testi
FONT_NEONLED_LITTLE = pygame.font.Font(os.path.join('Fonts','NEONLEDLight.otf'), 30) #font e grandezza dei testi
FONT_NEONLED_PULSANTI = pygame.font.Font(os.path.join('Fonts','NEONLEDLight.otf'), 40) #font e grandezza dei testi

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
                        self.run = False
            self.UltimoFrame, self.video_immagine = self.video.read()               #acquisico un frame
            self.count+=1
            if self.count==self.video_lenght:                                       #se il numero di frame é uguale alla lunghezza del video lo faccio ripartire da capo
                self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
                self.count=0
            self.drawTitle()        #disegno la finestra iniziale

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
        self.flag_warning = False                           #True = l'utente ha provato ad inserire un nick con meno di 3 caratteri
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
                if event.type == pygame.KEYDOWN:                    #controllo se l'utente sta digitando
                    if event.key == pygame.K_BACKSPACE:             #controllo se vuole cancellare un carattere
                        self.input_box = self.input_box[:-1]
                    if event.key != pygame.K_RETURN and event.key != pygame.K_BACKSPACE and event.key != pygame.K_SPACE: #controllo se vuole scrivere
                        self.input_box += event.unicode
                    if event.key == pygame.K_RETURN:             #controllo se vuole premere invio
                        if len(self.input_box)>2:               #controllo se ha scritto almeno 3 caratteri
                            self.run = False
                        else:
                            self.flag_warning = True
                    self.txt_input_box = FONT_NEONLED_SMALL.render(self.input_box, True, LIGHT_BLUE)
            
            self.drawGetNickname()
        self.ClientSocket.send(str.encode(self.input_box)) #invio il nickname al server
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
        pygame.display.update()




    def menuPrincipale(self):           #funzione che gestisce il menu principale
        self.run = True
        self.puls_gioca_pers = Pulsanti(480,325,"PARTITA PERSONALIZZATA",480+24,325+18)     #pulsante partita personalizzata
        self.puls_gioca_vel = Pulsanti(480,225,"PARTITA VELOCE",480+125,225+18)             #pulsante partita veloce
        self.puls_class = Pulsanti(480,425,"CLASSIFICA",480+175,425+18)                     #pulsante classifica
        self.puls_esci = Pulsanti(480,525,"ESCI",480+240,525+18)                            #pulsante esci
        self.puls_ind = PulsanteIndietro()                  #pulsante indietro (utilizzato successivamente)
        self.risp=0

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
                    self.classifica()
                if self.puls_gioca_vel.premuto(event) == True:      #controllo se l'utente vuole fare una partita veloce
                    self.run = False
                    self.risp="1"
                    self.ClientSocket.send(str.encode(self.risp))
                    self.partitaVeloce()
                if self.puls_gioca_pers.premuto(event) == True:      #controllo se l'utente vuole fare una partita personalizzata
                    self.run = False
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
        WIN.fill(ULTRAMARINE)
        self.puls_ind.drawPuls()
        pygame.display.update()






    def partitaVeloce(self):           #funzione che fa partire la partita veloce
        self.run = True
        self.domanda = self.ClientSocket.recv(2048).decode('utf-8')
        self.domanda = textwrap.wrap(self.domanda,width = 30)
        self.risp_a = self.ClientSocket.recv(2048).decode('utf-8')#ricevo la prima risposta dal server
        self.risp_a = textwrap.wrap(self.risp_a,width = 40)
        self.risp_b = self.ClientSocket.recv(2048).decode('utf-8')#ricevo la seconda risposta dal server
        self.risp_b = textwrap.wrap(self.risp_b,width = 40)
        self.risp_c = self.ClientSocket.recv(2048).decode('utf-8')#ricevo la terza risposta dal server
        self.risp_c = textwrap.wrap(self.risp_c,width = 40)
        self.risp_d = self.ClientSocket.recv(2048).decode('utf-8')#ricevo la quarta risposta dal server
        self.risp_d = textwrap.wrap(self.risp_d,width = 40)
        while self.run:
            self.clock.tick(FPS)
            for event in pygame.event.get():        
                if event.type == pygame.QUIT:           #controlllo se il giocatore chiude la finestra
                    self.ClientSocket.close()           #chiudo il socket
                    pygame.quit()
            self.drawPartitaVeloce()


    def drawPartitaVeloce(self):
        WIN.fill(LIGHT_PINK)
        for i in range(len(self.domanda)):
            self.txt_domanda = FONT_NEONLED.render(self.domanda[i], True, LIGHT_BLUE)
            WIN.blit(self.txt_domanda,(300, 200-(50*(len(self.domanda)-i+1))))
        for i in range(len(self.risp_a)):
            self.txt_risp_a = FONT_NEONLED_PULSANTI.render(self.risp_a[i], True, LIGHT_BLUE)
            WIN.blit(self.txt_risp_a,(300, 400-(50*(len(self.risp_a)-i+1))))
        for i in range(len(self.risp_b)):
            self.txt_risp_b = FONT_NEONLED_PULSANTI.render(self.risp_b[i], True, LIGHT_BLUE)
            WIN.blit(self.txt_risp_b,(300, 500-(50*(len(self.risp_b)-i+1))))
        for i in range(len(self.risp_c)):
            self.txt_risp_c = FONT_NEONLED_PULSANTI.render(self.risp_c[i], True, LIGHT_BLUE)
            WIN.blit(self.txt_risp_c,(300, 600-(50*(len(self.risp_c)-i+1))))
        for i in range(len(self.risp_d)):
            self.txt_risp_d = FONT_NEONLED_PULSANTI.render(self.risp_d[i], True, LIGHT_BLUE)
            WIN.blit(self.txt_risp_d,(300, 700-(50*(len(self.risp_d)-i+1))))
        pygame.display.update()





    def scegliCategoria(self):           #funzione che fa partire la partita personalizzata facendo scegliere la categoria
        self.run = True
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
            self.drawScegliCategoria()


    def drawScegliCategoria(self):
        WIN.fill(LIGHT_BLUE)
        self.puls_ind.drawPuls()
        pygame.display.update()







class PulsanteIndietro:                 #classe che gestisce il pulsante torna indietro
    def __init__(self):
        self.rect = pygame.Rect(100,20,100,100)
        self.puls_acceso = pygame.image.load(os.path.join('Assets','PulsanteIndietroAcceso.png'))
        self.puls_spento = pygame.image.load(os.path.join('Assets','PulsanteIndietroSpento.png'))

    def mouseSopra(self):                   #controllo se il mouse é sopra il pulsante
        self.sopra=False
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.sopra = True
    
    def drawPuls(self):               #disegno il pulsante a seconda se il mouse é sopra o no
        if self.sopra == True:
            WIN.blit(self.puls_spento,(self.rect.x, self.rect.y))
        else:
            WIN.blit(self.puls_acceso,(self.rect.x,self.rect.y))
    
    def premuto(self,event):            #vedo se é premuto
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
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

    def mouseSopra(self):                   #controllo se il mouse é sopra il pulsante
        self.sopra=False
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.sopra = True

    def drawButton(self):               #disegno il pulsante a seconda se il mouse é sopra o no
        if self.sopra == True:
            WIN.blit(self.img_spento,(self.rect.x, self.rect.y))
            WIN.blit(self.testo_acceso,(self.testox,self.testoy))
        else:
            WIN.blit(self.img_acceso,(self.rect.x,self.rect.y))
            WIN.blit(self.testo_spento,(self.testox,self.testoy))
    
    def premuto(self,event):            #vedo se é premuto
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        else:
            return False

        





def main():
    game=Game()
    game.setup()


if __name__ == "__main__":
    main()

