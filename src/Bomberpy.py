import os, sys
import pygame
from pygame.locals import *
from time import time, sleep
from tkinter import*
from tkinter.messagebox import showinfo
import random

# Initialisation Pygame
pygame.init()

global winner, bombsPlacedByPlayer1, bombsPlacedByPlayer2
winner = str("")
bombsPlacedByPlayer1 = 0
bombsPlacedByPlayer2 = 0

def init():
    startWindow = Tk()
    startWindow.title("Accueil")
    startWindow.geometry("450x450+450+125")

    #On ne peut pas redimentionner la fenêtre
    startWindow.resizable(width=False, height=False)
 
    can = Canvas(startWindow, width=450, height=450, bg='#0ea598')
    welcome = PhotoImage(file='.\\assets\\welcome.png')
    can.create_image(0,0, anchor=NW, image=welcome)
    can.place(x=0,y=0)
    
    def about():
        showinfo(
            "A propos\n\n",

            "*** Programme réalisé par ***\n"
            "GERARD Christopher et STEMELEN Frédéric \n"
            "Tle NSI - Lycée Louis Armand - Mulhouse \n"
        )
        return()

    def rules():
        showinfo(
            "Règles du jeu\n\n",

            "Commandes du joueur 1 (rouge):\n"
            "   - Déplacements : Flèches directionnelles\n"
            "   - Bombes : Touche 'M'\n\n"

            "Commandes du joueur 2 (vert):\n"
            "   - Déplacements : Touhces 'Z', 'Q', 'S', 'D'\n"
            "   - Bombes : Touche 'Espace'\n\n"

            "Le but est de faire exploser le joueur adverse grâce à vos bombes!!\n\n"
            "ENJOY ;)\n"
        )
        return()

    buttonAbout = Button(startWindow, text="A propos", command=about)
    buttonAbout = buttonAbout.pack(side=BOTTOM, padx=5, pady=5)

    buttonGameRules = Button(startWindow, text="Règles du jeu", command=rules)
    buttonGameRules = buttonGameRules.pack(side=BOTTOM, padx=5, pady=5)

    buttonContinue = Button(startWindow, text='Continuer', command=startWindow.destroy)
    buttonContinue = buttonContinue.pack(side=BOTTOM, padx=5, pady=5)

    startWindow.mainloop()
init()

#Ouverture de la fenêtre Pygame
gameWindow = pygame.display.set_mode((450, 450))

#Chargement et collage du fond
background = pygame.image.load("assets/background_main.jpg").convert()
gameWindow.blit(background, (0,0))

#Chargement et collage du personnage 1
player1 = pygame.image.load("assets/player1_down.png").convert_alpha()
xPlayer1 = 0
yPlayer1 = 0
gameWindow.blit(player1, (xPlayer1,yPlayer1))

#Chargement et collage du personnage 2:
player2 = pygame.image.load("assets/player2_down.png").convert_alpha()
xPlayer2 = 420
yPlayer2 = 420
gameWindow.blit(player2, (xPlayer2,yPlayer2))

# Chargement de toutes les images utiles
breakableWall =pygame.image.load("assets/wall_breakable.png").convert_alpha()
unbreakableWall = pygame.image.load("assets/wall_unbreakable.png").convert_alpha()
grass = pygame.image.load("assets/background_pixel.jpg").convert_alpha()
bombe1 = pygame.image.load("assets/bomb_yellow.png").convert_alpha()
bombe2 = pygame.image.load("assets/bomb_red.png").convert_alpha()

# Son d'ambiance
pygame.mixer.music.load("assets/theme.wav")
pygame.mixer.music.play()

# Initialisation tableau de gestion des bombes
bombs = []


# Gestion de la Map
a = -1
m = 'm'
d = 'd'
l = [0,d]

map = [[0,0,a,a,a,a,a,a,a,a,a,a,a,a,a],
        [0,a,m,a,m,a,m,a,m,a,m,a,m,a,a],
        [a,m,a,a,a,a,a,a,a,a,a,a,a,m,a],
        [a,a,m,a,m,a,m,a,m,a,m,a,m,a,a],
        [a,m,a,a,a,a,a,a,a,a,a,a,a,m,a],
        [a,a,m,a,m,a,m,a,m,a,m,a,m,a,a],
        [a,m,a,a,a,a,a,a,a,a,a,a,a,m,a],
        [a,a,m,a,m,a,m,a,m,a,m,a,m,a,a],
        [a,m,a,a,a,a,a,a,a,a,a,a,a,m,a],
        [a,a,m,a,m,a,m,a,m,a,m,a,m,a,a],
        [a,m,a,a,a,a,a,a,a,a,a,a,a,m,a],
        [a,a,m,a,m,a,m,a,m,a,m,a,m,a,a],
        [a,m,a,a,a,a,a,a,a,a,a,a,a,m,a],
        [a,a,m,a,m,a,m,a,m,a,m,a,m,a,0],
        [a,a,a,a,a,a,a,a,a,a,a,a,a,0,0]]

def map1():
    global a, map
    i = 0
    for line in map:
        i2 = 0
        for colone in line:
            if colone == a:
                c = random.choice(l)
                if c == 'd':
                    gameWindow.blit(breakableWall,(i*30,i2*30))
                    move = False
                elif c == 0:
                    gameWindow.blit(grass, (i*30, i2*30))
                    move = True
                map[i][i2] = c
            elif colone == 'm':
                gameWindow.blit(unbreakableWall,(i*30,i2*30))
                move = False
            elif colone == 'd':
                gameWindow.blit(breakableWall,(i*30,i2*30))
                move = False
            elif colone == 0:
                gameWindow.blit(grass,(i*30,i2*30))
                move = True
            elif colone == 'b1':
                gameWindow.blit(bombe1,(i*30, i2*30))
            elif colone == 'b2':
                gameWindow.blit(bombe2,(i*30, i2*30))

            i2 += 1
        i += 1
map1()

def colision():
    map1()
    x_map = int((xPlayer1+x_col)/30)
    y_map = int((yPlayer1+y_col)/30)
    if map[x_map][y_map] == 'm':
        return(False)
    elif map[x_map][y_map] =='d':
        return(False)
    elif map[x_map][y_map] == 0:
        return(True)
    elif map[x_map][y_map] == 'b1' or map[x_map][y_map] == 'b2':
        return(False)

def colision2():
    map1()
    x_map2 = int((xPlayer2+x_col2)/30)
    y_map2 = int((yPlayer2+y_col2)/30)
    if map[x_map2][y_map2] == 'm':
        return(False)
    elif map[x_map2][y_map2] =='d':
        return(False)
    elif map[x_map2][y_map2] == 0:
        return(True)
    elif map[x_map2][y_map2] == 'b1' or map[x_map2][y_map2] == 'b2':
        return(False)

def bomb():
    map[int(xPlayer1/30)][int(yPlayer1/30)] = 'b1'
    map1()
    bombs.append([int(xPlayer1/30), int(yPlayer1/30), time()+3, 1, time()+0.5])

def bomb2():
    map[int(xPlayer2/30)][int(yPlayer2/30)] = 'b1'
    map1()
    bombs.append([int(xPlayer2/30), int(yPlayer2/30), time()+3, 1, time()+0.5])

def fin():
    endWindow = Tk()
    endWindow.title("Fin de la partie")
    endWindow.geometry("450x450+450+125")

    #On ne peut pas redimentionner la fenêtre
    endWindow.resizable(width=False, height=False)
 
    can = Canvas(endWindow, width=450, height=450, bg='#0ea598')
    g_o = PhotoImage(file='.\\assets\\game_over.png')
    can.create_image(0,0, anchor=NW, image=g_o)
    can.place(x=0,y=0)
    
    buttonExit = Button(endWindow, text="Quitter", command=endWindow.quit)
    buttonExit = buttonExit.pack(side=BOTTOM, padx=5, pady=5)

    buttonWinner = Button(endWindow, text="Qui à gagné?", command=score)
    buttonWinner.pack(side=BOTTOM, padx=5, pady=5)

    buttonReplay = Button(endWindow, text="Rejouer", command=restart)
    buttonReplay.pack(side=BOTTOM, padx=5, pady=5)

    endWindow.mainloop()

def score():
    global bombsPlacedByPlayer1, bombsPlacedByPlayer2
    bombsPlacedByPlayer1 = str(bombsPlacedByPlayer1)
    bombsPlacedByPlayer2 = str(bombsPlacedByPlayer2)
    if winner == "egal":
        showinfo(
            "score...\n\n",

            "Il y a match nul parce que vous êtes nul :p\n\n"

            "Le joueur 1 a posé " + bombsPlacedByPlayer1 + " bombe(s)\n"
            "Le joueur 2 a posé " + bombsPlacedByPlayer2 + " bombe(s)\n"
        )
    else:
        showinfo(
            "Score...\n\n",

            "Le joueur " + winner + " gagne!\n\n"

            "Le joueur 1 a posé " + bombsPlacedByPlayer1 + " bombe(s)\n"
            "Le joueur 2 a posé " + bombsPlacedByPlayer2 + " bombe(s)\n"
        )
    return()

def restart():
    os.execl(sys.executable, sys.executable, *sys.argv) #Relance le programme depuis le début
    

# Rafraîchissement
pygame.display.flip()


# Boucle infinie
global pursue
pursue = 1
while pursue:
    for bombe in bombs:
        if time() > bombe[2]: # exploser la bombe
            map[bombe[0]][bombe[1]] = 0
            bombs.remove(bombe)

            if (not bombe[0] == 14) and map[bombe[0]+1][bombe[1]] == 'd': #A droite
                map[bombe[0]+1][bombe[1]] = 0

            if (not bombe[0] == 0) and map[bombe[0]-1][bombe[1]] == 'd': #A gauche
                map[bombe[0]-1][bombe[1]] = 0

            if (not bombe[1] == 14) and map[bombe[0]][bombe[1]+1] == 'd': #En bas
                map[bombe[0]][bombe[1]+1] = 0

            if (not bombe[1] == 0) and map[bombe[0]][bombe[1]-1] == 'd': #En haut
                map[bombe[0]][bombe[1]-1] = 0

            map1()

            # Gestion des matchs nuls
            # Si joueur1-bombe-joueur2 alignés horizontalement (Match nul)
            if (bombe[0]*30 == xPlayer1+30 and bombe[0]*30 == xPlayer2-30) and (bombe[1]*30 == yPlayer1 and bombe[1]*30 == yPlayer2):
                winner = str("egal")
                fin()
                pursue = 0
            # Si joueur2-bombe-joueur1 alignés horizontalement (Match nul)
            if (bombe[0]*30 == xPlayer2+30 and bombe[0]*30 == xPlayer1-30) and (bombe[1]*30 == yPlayer1 and bombe[1]*30 == yPlayer2):
                winner = str("egal")
                fin()
                pursue = 0
            # Si joueur1-bombe-joueur2 alignés verticalement (Match nul)
            if (bombe[1]*30 == yPlayer1+30 and bombe[1]*30 == yPlayer2-30) and (bombe[0]*30 == xPlayer1 and bombe[0]*30 == xPlayer2):
                winner = str("egal")
                fin()
                pursue = 0
            # Si joueur2-bombe-joueur1 alignés verticalement (Match nul)
            if (bombe[1]*30 == yPlayer2+30 and bombe[1]*30 == yPlayer1-30) and (bombe[0]*30 == xPlayer1 and bombe[0]*30 == xPlayer2):
                winner = str("egal")
                fin()
                pursue = 0
            # Si joueur2/bombe-joueur1 alignés horizontalement (Match nul)
            if (bombe[0]*30 == xPlayer2 and bombe[0]*30 == xPlayer1-30) and (bombe[1]*30 == yPlayer1 and bombe[1]*30 == yPlayer2):
                winner = str("egal")
                fin()
                pursue = 0
            # Si joueur1/bombe-joueur2 alignés horizontalement (Match nul)
            if (bombe[0]*30 == xPlayer1 and bombe[0]*30 == xPlayer2-30) and (bombe[1]*30 == yPlayer1 and bombe[1]*30 == yPlayer2):
                winner = str("egal")
                fin()
                pursue = 0
            # Si joueur2-joueur1/bombe alignés horizontalement (Match nul)
            if (bombe[0]*30 == xPlayer1 and bombe[0]*30 == xPlayer2+30) and (bombe[1]*30 == yPlayer1 and bombe[1]*30 == yPlayer2):
                winner = str("egal")
                fin()
                pursue = 0
            # Si joueur1-joueur2/bombe alignés horizontalement (Match nul)
            if (bombe[0]*30 == xPlayer2 and bombe[0]*30 == xPlayer1+30) and (bombe[1]*30 == yPlayer1 and bombe[1]*30 == yPlayer2):
                winner = str("egal")
                fin()
                pursue = 0
            # Si joueur1/bombe-joueur2 alignés verticalement (Match nul)
            if (bombe[1]*30 == yPlayer1 and bombe[1]*30 == yPlayer2-30) and (bombe[0]*30 == xPlayer1 and bombe[0]*30 == xPlayer2):
                winner=str("egal")
                fin()
                pursue = 0
            # Si joueur1-joueur2/bombe alignés verticalement (Match nul)
            if (bombe[1]*30 == yPlayer2 and bombe[1]*30 == yPlayer1+30) and (bombe[0]*30 == xPlayer1 and bombe[0]*30 == xPlayer2):
                winner=str("egal")
                fin()
                pursue = 0
            # Si joueur2/bombe-joueur1 alignés verticalement (Match nul)
            if (bombe[1]*30 == yPlayer2 and bombe[1]*30 == yPlayer1-30) and (bombe[0]*30 == xPlayer1 and bombe[0]*30 == xPlayer2):
                winner=str("egal")
                fin()
                pursue = 0
            # Si joueur2-joueur1/bombe alignés verticalement (Match nul)
            if (bombe[1]*30 == yPlayer1 and bombe[1]*30 == yPlayer2+30) and (bombe[0]*30 == xPlayer1 and bombe[0]*30 == xPlayer2):
                winner=str("egal")
                fin()
                pursue = 0
            # Si joueur1/bombe/joueur2 sur une même case (Match nul)
            if (bombe[0]*30 == xPlayer1 and bombe[0]*30 == xPlayer2) and (bombe[1]*30 == yPlayer1 and bombe[1]*30 == yPlayer2):
                winner=str("egal")
                fin()
                pursue = 0
            # Si joueur1-bombe-joueur2 en 'L'
            if (bombe[0]*30 == xPlayer2-30) and (bombe[0]*30 == xPlayer1) and (bombe[1]*30 == yPlayer1+30) and (bombe[1]*30 == yPlayer2):
                winner=str("egal")
                fin()
                pursue = 0
            # Si joueur2-bombe-joueur1 en 'L'
            if (bombe[0]*30 == xPlayer1-30) and (bombe[0]*30 == xPlayer2) and (bombe[1]*30 == yPlayer2+30) and (bombe[1]*30 == yPlayer1):
                winner=str("egal")
                fin()
                pursue = 0
            # Si joueur2-bombe-joueur1, angle droit en bas à droite
            if (bombe[0]*30 == xPlayer2+30) and (bombe[0]*30 == xPlayer1) and (bombe[1]*30 == yPlayer1+30) and (bombe[1]*30 == yPlayer2):
                winner=str("egal")
                fin()
                pursue = 0
            # Si joueur1-bombe-joueur2, angle droit en bas à droite
            if (bombe[0]*30 == xPlayer1+30) and (bombe[0]*30 == xPlayer2) and (bombe[1]*30 == yPlayer2+30) and (bombe[1]*30 == yPlayer1):
                winner=str("egal")
                fin()
                pursue = 0
            # Si joueur2-bombe-joueur1, angle droit en haut à gauche
            if (bombe[0]*30 == xPlayer1-30) and (bombe[0]*30 == xPlayer2) and (bombe[1]*30 == yPlayer2-30) and (bombe[1]*30 == yPlayer1):
                winner = str("egal")
                fin()
                pursue = 0
            # Si joueur1-bombe-joueur2, angle droit en haut à gauche
            if (bombe[0]*30 == xPlayer2-30) and (bombe[0]*30 == xPlayer1) and (bombe[1]*30 == yPlayer1-30) and (bombe[1]*30 == yPlayer2):
                winner = str("egal")
                fin()
                pursue = 0
            # Si joueur1-bombe-joueur2, angle droit en haut à droite
            if (bombe[0]*30 == xPlayer1+30) and (bombe[0]*30 == xPlayer2) and (bombe[1]*30 == yPlayer2-30) and (bombe[1]*30 == yPlayer1):
                winner = str("egal")
                fin()
                pursue = 0
            # Si joueur2-bombe-joueur1, angle droit en haut à droite
            if (bombe[0]*30 == xPlayer2+30) and (bombe[0]*30 == xPlayer1) and (bombe[1]*30 == yPlayer1-30) and (bombe[1]*30 == yPlayer1):
                winner = str("egal")
                fin()
                pursue = 0



            # Fin de partie
            # Colision bombe + joueur 1

            if bombe[0]*30 == xPlayer1-30 and bombe[1]*30 == yPlayer1: # Si joueur à droite de la bombe
                winner = str('Vert')
                fin()
                pursue = 0
            if bombe[0]*30 == xPlayer1+30 and bombe[1]*30 == yPlayer1: # Si joueur à gauche de la bombe
                winner = str('Vert')
                fin()
                pursue = 0
            if bombe[0]*30 == xPlayer1 and bombe[1]*30 == yPlayer1-30: # Si joueur en dessous de la bombe
                winner = str('Vert')
                fin()
                pursue = 0
            if bombe[0]*30 == xPlayer1 and bombe[1]*30 == yPlayer1+30: # Si joueur au dessus de la bombe
                winner = str('Vert')
                fin()
                pursue = 0
            if bombe[0]*30 == xPlayer1 and bombe[1]*30 == yPlayer1: # Si joueur sur la bombe
                winner = str('Vert')
                fin()
                pursue = 0

            #Colision bombe + joueur 2
            if (bombe[0]*30 == xPlayer2-30 and bombe[1]*30 == yPlayer2): # Si joueur à droite de la bombe
                winner = str('Rouge')
                fin()
                pursue = 0
            if (bombe[0]*30 == xPlayer2+30 and bombe[1]*30 == yPlayer2): # Si joueur à gauche de la bombe
                winner = str('Rouge')
                fin()
                pursue = 0
            if (bombe[0]*30 == xPlayer2 and bombe[1]*30 == yPlayer2-30): # Si joueur en dessous de la bombe
                winner = str('Rouge')
                fin()
                pursue = 0
            if (bombe[0]*30 == xPlayer2 and bombe[1]*30 == yPlayer2+30): # Si joueur au dessus de la bombe
                winner = str('Rouge')
                fin()
                pursue = 0
            if bombe[0]*30 == xPlayer2 and bombe[1]*30 == yPlayer2: # Si joueur sur la bombe
                winner = str('Rouge')
                fin()
                pursue = 0


        # En attendant que la bombe explose
        elif time() > bombe[4]:
            if bombe[3] == 1:
                map[bombe[0]][bombe[1]] = 'b2'
                map1()
                bombe[3] = 2
                bombe[4] = time() + 0.5
            else:
                map[bombe[0]][bombe[1]] = 'b1'
                map1()
                bombe[3] = 1
                bombe[4] = time() + 0.5

    # Attente des évènements
    for event in pygame.event.get():
        if event.type == QUIT:
            pursue = 0

        # Déplacement joueur 1 :
        if event.type == KEYDOWN:
            if event.key == K_UP and not yPlayer1 <= 0:
                x_col = 0
                y_col = -30
                if colision() == True:
                    player1 = pygame.image.load("assets/player1_up.png").convert_alpha()
                    gameWindow.blit(grass,(xPlayer1,yPlayer1))
                    yPlayer1 -= 30
            if event.key == K_DOWN and not yPlayer1 >= 420:
                x_col = 0
                y_col = 30
                if colision() == True:
                    if yPlayer1 <= 450:
                        player1 = pygame.image.load("assets/player1_down.png").convert_alpha()
                        gameWindow.blit(grass,(xPlayer1,yPlayer1))
                        yPlayer1 += 30
            if event.key == K_LEFT and not xPlayer1 <= 0:
                x_col = -30
                y_col = 0
                if colision() == True:
                    if xPlayer1 >= 0:
                        player1 = pygame.image.load("assets/player1_left.png").convert_alpha()
                        gameWindow.blit(grass,(xPlayer1,yPlayer1))
                        xPlayer1 -= 30
            if event.key == K_RIGHT and not xPlayer1 >= 420:
                x_col = 30
                y_col = 0
                if colision() == True:
                    if xPlayer1 <= 450:
                        player1 = pygame.image.load("assets/player1_right.png").convert_alpha()
                        gameWindow.blit(grass,(xPlayer1,yPlayer1))
                        xPlayer1 += 30
            if event.key == K_m:
                bombsPlacedByPlayer1 += 1
                bomb()


        # Déplacement joueur 2 :
        if event.type == KEYDOWN:
            if event.key == K_z and not yPlayer2 <= 0:
                x_col2 = 0
                y_col2 = -30
                if colision2() == True:
                    player2 = pygame.image.load("assets/player2_up.png").convert_alpha()
                    gameWindow.blit(grass,(xPlayer2,yPlayer2))
                    yPlayer2 -= 30
            if event.key == K_s and not yPlayer2 >= 420:
                x_col2 = 0
                y_col2 = 30
                if colision2() == True:
                    if yPlayer2 <= 450:
                        player2 = pygame.image.load("assets/player2_down.png").convert_alpha()
                        gameWindow.blit(grass,(xPlayer2,yPlayer2))
                        yPlayer2 += 30
            if event.key == K_q and not xPlayer2 <= 0:
                x_col2 = -30
                y_col2 = 0
                if colision2() == True:
                    if xPlayer2 >= 0:
                        player2 = pygame.image.load("assets/player2_left.png").convert_alpha()
                        gameWindow.blit(grass,(xPlayer2,yPlayer2))
                        xPlayer2 -= 30
            if event.key == K_d and not xPlayer2 >= 420:
                x_col2 = 30
                y_col2 = 0
                if colision2() == True:
                    if xPlayer2 <= 450:
                        player2 = pygame.image.load("assets/player2_right.png").convert_alpha()
                        gameWindow.blit(grass,(xPlayer2,yPlayer2))
                        xPlayer2 += 30
            if event.key == K_SPACE:
                bombsPlacedByPlayer2 += 1
                bomb2()


    # Repositionnement des perosnnages
    gameWindow.blit(player1, (xPlayer1, yPlayer1))
    gameWindow.blit(player2, (xPlayer2,yPlayer2))
	# Rafraichissement
    pygame.display.flip()
pygame.quit()