import pygame as pg
from pygame.locals import *
import os,sys,glob
from variables import *

os.environ['SDL_VIDEO_CENTERED'] = '1'
pg.mixer.pre_init(22050,16,2,512)    
pg.init()
pg.key.set_repeat(20,100)

pg.display.set_mode((WIN_WIDTH[0],WIN_HEIGHT[0]),MODE_ECRAN[0])   

infoDisplay = pg.display.Info()
LARGEUR_ECRAN = infoDisplay.current_w
HAUTEUR_ECRAN = infoDisplay.current_h

TITRE = "solitaire chinois v1.0"

FPS = 30

COLOR_KEY = (0,0,0)

#--- IMAGES
#-- background
BACKGROUND = pg.image.load(os.path.join("Ressources","Images","background5.jpg")).convert()

#-- sprites
IMAGE_PION1 = pg.image.load(os.path.join("Ressources","Images","gem1.png")).convert_alpha()
IMAGE_PION2 = pg.image.load(os.path.join("Ressources","Images","gem2.png")).convert_alpha()
IMAGE_PION3 = pg.image.load(os.path.join("Ressources","Images","gem3.png")).convert_alpha()
IMAGE_PION4 = pg.image.load(os.path.join("Ressources","Images","gem4.png")).convert_alpha()
IMAGE_PION5 = pg.image.load(os.path.join("Ressources","Images","gem5.png")).convert_alpha()
IMAGE_PION6 = pg.image.load(os.path.join("Ressources","Images","gem6.png")).convert_alpha()
IMAGE_PION7 = pg.image.load(os.path.join("Ressources","Images","gem7.png")).convert_alpha()

LISTE_IMAGES_PIONS = [IMAGE_PION1,
                      IMAGE_PION2,
                      IMAGE_PION3,
                      IMAGE_PION4,
                      IMAGE_PION5,
                      IMAGE_PION6,
                      IMAGE_PION7]
#--- DIMENSIONS
LARGEUR_GEMME, HAUTEUR_GEMME = IMAGE_PION1.get_size()[0],IMAGE_PION1.get_size()[1]

#--- TEMPS ALLOUE
TEMPS_ALLOUE = 60 #sec

#--- SONS
#-- jeu
SON_PIECE_SELECTIONNEE = pg.mixer.Sound(os.path.join("Ressources","Sons","piece_tomb2.wav"))
SON_PIECE_SELECTIONNEE.set_volume(VOLUME_SON[0]/10.)

SON_PIECE_POSITIONNEE = pg.mixer.Sound(os.path.join("Ressources","Sons","glass-cork-close-1.wav"))
SON_PIECE_POSITIONNEE.set_volume(VOLUME_SON[0]/10.)

#--- Musique
MUSIQUE = os.path.join("Ressources","Sons","Kalipluche_-_ascent (2).mp3")
pg.mixer.music.set_volume(VOLUME_MUSIQUE[0]/10.)

#--- Font
PATH_FONT = os.path.join("Ressources","Font","CHINESETAKEAWAY.ttf")
