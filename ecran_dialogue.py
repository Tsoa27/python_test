# -*- coding: Utf-8 -*

from constantes import *

class Ecran_Dialogue(object):
    """Classe qui crée écran de dialogue à choix multiple en transparence sur le level courant."""
    def __init__(self,screen=None,background=None,plateau=None,interface=None,titre=None,options=None):

        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.background = background
        
        self.plateau = plateau
        self.interface = interface
        
        self.titre = titre

        self.options = options

        self.clock = pg.time.Clock()        

        self.font = pg.font.Font(PATH_FONT,28)

        self.texteTitre = self.font.render(self.titre,1,(0,255,255))
        self.rectTitre = self.texteTitre.get_rect(centerx=self.screen_rect.w/2,y=100)

        self.optionChoisie = None

        self.surface = pg.Surface((self.screen_rect.size)).convert()
        self.surface.set_alpha(200)
        self.rectSurface = self.surface.get_rect()

        pg.mouse.set_visible(False)
        self.main_loop()
            
    def main_loop(self):

        indice = 0
        while 1 :
            for event in pg.event.get():
                if event.type == KEYUP:
                    if event.key == K_RETURN:
                        self.optionChoisie = self.options[indice]
                        return
                    
                    if event.key == K_UP:
                        indice = (indice-1)%len(self.options)
                    if event.key == K_DOWN:
                        indice = (indice+1)%len(self.options)
                        

            if self.background:
                self.screen.blit(self.background,(0,0))
            if self.interface:
                self.interface.draw()
            if self.plateau:
                self.plateau.draw()
            
            self.surface.fill((0,0,0))
            self.surface.blit(self.texteTitre,self.rectTitre)
            posy = 200
            for option in self.options[indice/8:]:
                if self.options.index(option) == indice:
                    texte = self.font.render(option,1,(255,0,0))
                else:
                    texte = self.font.render(option,1,(255,255,255))
                rectTexte = texte.get_rect(centerx=self.screen_rect.w/2,y=posy)
                self.surface.blit(texte,rectTexte)
                posy += 50
            pg.draw.rect(self.surface,(255,255,255),Rect(0,0,WIN_WIDTH[0],WIN_HEIGHT[0]),1)
            self.screen.blit(self.surface,self.rectSurface)
            pg.display.flip()
            self.clock.tick(25)


