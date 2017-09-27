# -*- coding: Utf-8 -*
################################################################################
#                                                                              #
#                                Classe Interface                              #
#                                                                              # 
################################################################################

from constantes import *
from variables import *
from sprites import *

class Interface(object):
    def __init__(self,screen,plateau=None,scoreBattre=0):
        """Classe interface à implémenter """

        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.plateau = plateau
        self.scoreBattre = scoreBattre

        self.font1 = pg.font.Font(PATH_FONT,16)
        self.texteLabelPions = self.font1.render("PIONS",1,(255,255,255))
        self.rectTexteLabelPions = self.texteLabelPions.get_rect(centerx=80,y=60)
        self.texteNbrPions = self.font1.render(str(len(Pion.containers)),1,(255,255,255))
        self.rectTexteNbrPions = self.texteNbrPions.get_rect(centerx=80,y=90)

        self.font1 = pg.font.Font(PATH_FONT,13)
        self.texteLabelMouvementsPossibles = self.font1.render("MOUVEMENTS POSSIBLES",1,(255,255,255))
        self.rectTexteLabelMouvementsPossibles = self.texteLabelMouvementsPossibles.get_rect(centerx=425,y=65)

        self.texteNbrMouvementsPossibles = self.font1.render(str(self.plateau.nbrMouvementsPossibles),1,(255,255,255))
        self.rectTexteNbrMouvementsPossibles = self.texteNbrMouvementsPossibles.get_rect(centerx=425,y=100)        

        self.font1 = pg.font.Font(PATH_FONT,16)
        self.texteLabelBest = self.font1.render("BEST",1,(255,255,255))
        self.rectTexteLabelBest = self.texteLabelBest.get_rect(centerx=70,y=400)

        self.texteBest = self.font1.render(str(self.scoreBattre),1,(255,255,255))
        self.rectTexteBest = self.texteLabelBest.get_rect(centerx=80,y=430)        

        self.font1 = pg.font.Font(PATH_FONT,12)
        self.texteLabelChangerForme = self.font1.render("C : CHANGER FORME",1,(255,255,255))
        self.rectTexteLabelChangerForme = self.texteLabelChangerForme.get_rect(x=370,y=380)
        
        self.font1 = pg.font.Font(PATH_FONT,14)
        self.texteLabelRecommencer = self.font1.render("R : Recommencer",1,(255,255,255))
        self.rectTexteLabelRecommencer = self.texteLabelRecommencer.get_rect(x=370,y=400)
        
        self.texteLabelOptions = self.font1.render("O : Options",1,(255,255,255))
        self.rectTexteLabelOptions = self.texteLabelOptions.get_rect(x=370,y=420)

        self.texteLabelMenu = self.font1.render("Esc : MENU",1,(255,255,255))
        self.rectTexteLabelMenu = self.texteLabelMenu.get_rect(x=370,y=440) 
        
    def update(self):
        """Mise à jour des informations."""
        
        self.texteNbrPions = self.font1.render(str(len(Pion.containers)),1,(255,255,255))
        self.texteNbrMouvementsPossibles = self.font1.render(str(self.plateau.nbrMouvementsPossibles),1,(255,255,255))        
        
    def draw(self):
        """Dessine les informations de l'interface ."""
        
        self.screen.blit(BACKGROUND,(0,0))
        self.screen.blit(self.texteLabelPions,self.rectTexteLabelPions)
        self.screen.blit(self.texteNbrPions,self.rectTexteNbrPions)        
        self.screen.blit(self.texteLabelMouvementsPossibles,self.rectTexteLabelMouvementsPossibles)
        self.screen.blit(self.texteNbrMouvementsPossibles,self.rectTexteNbrMouvementsPossibles)        
        self.screen.blit(self.texteLabelBest,self.rectTexteLabelBest)
        self.screen.blit(self.texteBest,self.rectTexteBest)
        self.screen.blit(self.texteLabelRecommencer,self.rectTexteLabelRecommencer)        
        self.screen.blit(self.texteLabelOptions,self.rectTexteLabelOptions)
        self.screen.blit(self.texteLabelChangerForme,self.rectTexteLabelChangerForme)
        self.screen.blit(self.texteLabelMenu,self.rectTexteLabelMenu)
      
