import pygame
import os
import socket
import textwrap
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))      #FINESTRA
pygame.display.set_caption("Indovinelli")           #CAMBIO NOME ALLA FINESTRA

WHITE = [255,255,255]       #COLORI
RED = [255,0,0]
GREEN = [0,255,0]
BLACK = [36,36,36]

FPS = 60

FONT = pygame.font.SysFont('impact', 28)

YOUDIEDAUDIO = pygame.mixer.Sound(os.path.join('Assets', 'Youdied.wav'))
BACKGROUNDMUSIC = pygame.mixer.Sound(os.path.join('Assets','Background.wav'))



class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.y = y
        self.color = WHITE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            if event.key != pygame.K_RETURN and event.key != pygame.K_BACKSPACE:
                self.text += event.unicode
            self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw_box(self, WIN):
        WIN.blit(self.txt_surface, (self.rect.x+5, self.rect.y))
        pygame.draw.rect(WIN, self.color, self.rect, 2)

    def is_empty(self):
        if self.text == '':
            return True
        else:
            return False 

    def get_nick(self):
        return self.text

    def gety(self):
        return self.y


class Game:

    def run(self):
        ClientSocket = socket.socket()
        self.host = 'localhost'
        self.port = 6716

        print('Waiting for connection')

        self.nickname = ''
        BACKGROUNDMUSIC.play(-1,0)
        self.Stage1()

        try:
            ClientSocket.connect((self.host, self.port))
            ClientSocket.send(str.encode(self.nickname))
        except socket.error as e:
            print(str(e))

        self.loop = True 
        while self.loop:
            self.Stage2(ClientSocket)

        

    def draw_stage_1(self,inputbox1):   
        WIN.fill(BLACK)
        inputbox1.update()
        inputbox1.draw_box(WIN)
        WIN.blit(self.txt_ask_nick, (WIDTH//2-170, HEIGHT//2-70))
        WIN.blit(self.txt_avanti, (self.rect_avanti.x, self.rect_avanti.y))
        pygame.display.update()

    def Stage1(self):               #STAGE 1 = acquisico il nome utente
            self.clock = pygame.time.Clock()        #dichiaro il clock
            self.run= True
            self.ask_nick = 'Inserire il nickname nella box'    
            self.txt_ask_nick = FONT.render(self.ask_nick, True, WHITE)
            self.rect_avanti = pygame.Rect(570, 440, 60, 40)
            self.avanti = 'AVANTI'
            self.txt_avanti = FONT.render(self.avanti, True, WHITE)
            inputbox1 = InputBox(WIDTH //2 - 90 , HEIGHT //2 - 20, 140, 40)     
            while self.run:
                self.clock.tick(FPS)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:       #si chiude in caso l'utente clicca sulla x
                        ClientSocket.close()
                        pygame.quit()
                    inputbox1.handle_event(event)       #controllo se premo col mouse sulla box
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.rect_avanti.collidepoint(event.pos):
                            if inputbox1.is_empty() == False:
                                self.nickname=inputbox1.get_nick()
                                self.run = False
                    if event.type == pygame.KEYDOWN:        #controllo se premo invio
                        if event.key == pygame.K_RETURN:
                            if inputbox1.is_empty() == False:
                                self.nickname=inputbox1.get_nick()
                                self.run = False



                self.draw_stage_1(inputbox1)            #refresho la finestra


    def Stage2(self, ClientSocket):                 #stage 2 = gioco effettivo
        self.risposta = ''
        self.clock = pygame.time.Clock()        #dichiaro il clock
        self.run= True
        inputboxRisp = InputBox(WIDTH //2 - 90 , HEIGHT //2 - 20, 140, 40)
        self.Response = ClientSocket.recv(1024)
        self.Response= textwrap.wrap(self.Response.decode('utf-8'),width = 40)
        self.rect_invio = pygame.Rect(570, 440, 60, 40)
        self.invio = 'INVIO'
        self.txt_invio = FONT.render(self.avanti, True, WHITE)
        while self.run:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:       #si chiude in caso l'utente clicca sulla x
                    ClientSocket.close()
                    pygame.quit()
                inputboxRisp.handle_event(event)       #controllo se premo col mouse sulla box
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.rect_invio.collidepoint(event.pos):
                        if inputboxRisp.is_empty() == False:
                            self.risposta=inputboxRisp.get_nick()
                            self.run = False
                if event.type == pygame.KEYDOWN:        #controllo se premo invio
                    if event.key == pygame.K_RETURN:
                        print("fatto")
                        if inputboxRisp.is_empty() == False:
                            self.risposta=inputboxRisp.get_nick()
                            self.run = False

            
            self.draw_stage_2(inputboxRisp)            #refresho la finestra

        ClientSocket.send(str.encode(self.risposta))
        self.undefinable_poggers = ClientSocket.recv(1024) 
        self.txt_may_be_poggers = FONT.render(self.undefinable_poggers, True, WHITE)
        self.draw_stage_might_be_poggers(inputboxRisp)            #refresho la finestra
        if self.undefinable_poggers.decode('utf-8') != 'yay poggers':
            YOUDIEDAUDIO.play()
        pygame.time.delay(3000)
        
            


    def draw_stage_2(self,inputboxRisp):   
        WIN.fill(BLACK)
        inputboxRisp.update()
        inputboxRisp.draw_box(WIN)
        for i in range(len(self.Response)):
            self.txt_response = FONT.render(self.Response[i], True, WHITE)
            WIN.blit(self.txt_response, (WIDTH//2 - 190, HEIGHT//2-(30*(len(self.Response)-i+1))))
        WIN.blit(self.txt_invio, (self.rect_invio.x, self.rect_invio.y))
        pygame.display.update()

    def draw_stage_might_be_poggers(self,inputboxRisp):   
        WIN.fill(BLACK)
        inputboxRisp.update()
        inputboxRisp.draw_box(WIN)
        for i in range(len(self.Response)):
            self.txt_response = FONT.render(self.Response[i], True, WHITE)
            WIN.blit(self.txt_response, (WIDTH//2-200, HEIGHT//2-(30*(len(self.Response)-i+1))))
        WIN.blit(self.txt_invio, (self.rect_invio.x, self.rect_invio.y))
        WIN.blit(self.txt_may_be_poggers, (WIDTH//2-170, inputboxRisp.gety() + 70))
        pygame.display.update()











def main():
    game = Game()
    game.run()

    
    
        
        

if __name__ == "__main__":
    main()





