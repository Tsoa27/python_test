# -*- coding: Utf-8 -*
from math import pi,cos,sin
from constantes import *

class Pion(pg.sprite.Sprite):
    """Classe permettant la création d'un objet Pion"""
    def __init__(self,indiceColonne,indiceLigne,image,nom):
        pg.sprite.Sprite.__init__(self,self.containers)

        self.indiceColonne = indiceColonne
        self.indiceLigne = indiceLigne     

        self.imageOriginale = image
        self.offset_x = 25
        self.offset_y = 25
        self.rectOriginal = self.imageOriginale.get_rect(x=self.indiceColonne*LARGEUR_GEMME+self.offset_x,y=self.indiceLigne*HAUTEUR_GEMME+self.offset_y)
        
        self.image = image
        self.rect = self.rectOriginal.copy()

    def position_initiale(self):
        """Remet le pion à sa position initiale."""
        
        self.image = self.imageOriginale
        self.rect = self.rectOriginal.copy()
        
    def positionnement(self,mouvementValide=True):
        """Calcule la nouvelle position du pion."""

        self.image = self.imageOriginale
        if mouvementValide:
            self.indiceColonne = (self.rect.centerx-self.offset_x)/64
            self.indiceLigne = (self.rect.centery-self.offset_y)/64
        self.rectOriginal = self.imageOriginale.get_rect(x=self.indiceColonne*LARGEUR_GEMME+self.offset_x,y=self.indiceLigne*HAUTEUR_GEMME+self.offset_y)
        self.rect = self.rectOriginal.copy()
        
    def update(self,fadeOut=False):
        """Disparition par rétrécissement du pion."""

        if fadeOut:
            self.image = pg.transform.smoothscale(self.image,(self.rect.w-8,self.rect.h-8))
            self.rect = self.image.get_rect(center=self.rectOriginal.center)
            if self.rect.w < 20:
                self.kill()
