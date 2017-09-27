# -*- coding: Utf-8 -*
################################################################################
#                                                                              #
#                          Solitaire Chinois                                   #
#                                                                              #
#                    Jeu du type solitaire chinois                             #
#                                                                              #
#                       langage : Python 2.7                                   #
#                       API     : Pygame 1.9                                   #
#                       date    : 13/08/2017                                   #
#                       version : 1.0                                          #
#                       auteur  : guillaume michon                             #
#                                                                              #
################################################################################

from variables import *
from constantes import *
from level import *
from interface import*
from ecran_dialogue import *
from ecran_options import *

class SOLITAIRE_CHINOIS(object):
    def __init__(self):
        """Class principale préparant le jeu avant son lancement."""        

        #+- Display et sa surface associée        
        #pg.display.set_mode((WIN_WIDTH[0],WIN_HEIGHT[0]),MODE_ECRAN[0])
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()

        #+- Attributs de contrôle du jeu
        self.quitterJeu = False
        self.retourMenu = False

        #+- Attribut contenant tous les levels du jeu quand ceux-ci sont dans un fichier au format .txt sous forme de matrices
        self.tousLevels = None

        #+- Attribut contenant un level sous forme de plateau
        self.plateau = Level(self.screen,scoreBattre=32)
        
        #+- Attribut contenant l'affichage des infos        
        self.interface = Interface(self.screen,self.plateau,32)

        #+- Attribut contenant le score a battre
        self.scoreBattre = 32
        
        #+- Attribut de l'horloge de pygame
        self.clock = pg.time.Clock()

        self.surfaceMenu = None


    def event_loop(self):
        """Récupération des événements utilisateur."""
        
        for event in pg.event.get():
            # touche relachée
            if event.type == KEYUP:
                # touche 'echapement' : retour
                if event.key == K_ESCAPE:
                    if Ecran_Dialogue(self.screen,BACKGROUND,interface=self.interface,titre="Retour Menu ?",options=['OUI','NON']).optionChoisie == 'OUI':
                        self.retourMenu = True
                    else:
                        pg.mouse.set_visible(True)                        

                # touche o (menu)
                elif event.key == K_o:
                    options = Ecran_Options(self.screen,self.interface,imageMenu=BACKGROUND,options=[['Plein Ecran : ',MODE_ECRAN,[0,FULLSCREEN]],
                                                                                                     ['Volume Musique : ',VOLUME_MUSIQUE,range(11)],
                                                                                                     ['Volume Son : ',VOLUME_SON,range(11)]])
                    pg.mouse.set_visible(True)
                # touche c (changer forme)
                elif event.key == K_c:
                    self.plateau.changement_image()
                # touche r (recommencer)                    
                elif event.key == K_r:
                    self.plateau = Level(self.screen,scoreBattre=self.scoreBattre)
                    self.interface = Interface(self.screen,self.plateau,scoreBattre=self.scoreBattre)

            # souris
            elif event.type == MOUSEBUTTONDOWN :
                self.plateau.mouse_button_down()
            elif event.type == MOUSEBUTTONUP :
                self.plateau.mouse_button_up()

    def update(self):
        """Méthode de mise à jour des éléments du jeu."""
        
        if self.plateau.gameOver:
            if self.plateau.scoreBattre < self.scoreBattre:
                self.scoreBattre = self.plateau.scoreBattre
            self.game_over()
        elif self.plateau.partieGagnee:
            self.scoreBattre = self.plateau.scoreBattre
            self.interface.update()            
            self.partie_gagnee()
        else:
            self.plateau.update()
            self.interface.update()

    def draw(self):
        """Dessine le level courant et l'interface."""
        
        if not self.retourMenu:
            self.interface.draw()
            self.plateau.draw()                   

    def game_over(self):
        """Quand la partie est perdue."""
        
        ecranDialogue = Ecran_Dialogue(self.screen,BACKGROUND,self.plateau,self.interface,'GAME OVER !!!',['REJOUER','MENU'])
        if ecranDialogue.optionChoisie == 'MENU':
            self.retourMenu = True
        else:
            pg.mouse.set_visible(True)            
            self.plateau = Level(self.screen,scoreBattre=self.scoreBattre)
            self.interface = Interface(self.screen,self.plateau,scoreBattre=self.scoreBattre)            

    def partie_gagnee(self):
        """Quand la partie est gagnée."""
        
        ecranDialogue = Ecran_Dialogue(self.screen,BACKGROUND,self.plateau,self.interface,'FELICITATIONS !!!',['REJOUER','MENU'])
        if ecranDialogue.optionChoisie == 'MENU':
            self.retourMenu = True
        else:
            pg.mouse.set_visible(True)            
            self.plateau = Level(self.screen,scoreBattre=self.scoreBattre)
            self.interface = Interface(self.screen,self.plateau,scoreBattre=self.scoreBattre)

    def credits(self):
        """Affichage des crédits du jeu."""
        
        surface = pg.Surface((WIN_WIDTH[0],WIN_HEIGHT[0])).convert()
        surface.set_alpha(200)
        surface.blit(BACKGROUND,(0,0))
        rectSurface = surface.get_rect()
        font = pg.font.Font(PATH_FONT,40)
        titre = font.render(TITRE,1,(255,255,100))
        rectTitre = titre.get_rect(centerx=WIN_WIDTH[0]/2,centery=100)
        surface.blit(titre,rectTitre)
        font = pg.font.Font(PATH_FONT,16)
        texteQuitter = font.render("Echap pour quitter",1,(255,255,255))
        surface.blit(texteQuitter,(0,0))        
        credit=[('Programmeur','Guillaume Michon'),('Musique',"Kalipluche - ascent")]
        posy = 180
        font = pg.font.Font(PATH_FONT,30)        
        for c in credit:
            texte = font.render(c[0],1,(255,0,0))
            rectTexte = texte.get_rect(centerx=WIN_WIDTH[0]/2,centery=posy)
            surface.blit(texte,rectTexte)
            texte = font.render(c[1],1,(255,255,255))
            rectTexte = texte.get_rect(centerx=WIN_WIDTH[0]/2,centery=posy+40)
            surface.blit(texte,rectTexte)
            posy += 100
        retourMenu = False
        while not retourMenu:
            for event in pg.event.get():
                if event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        retourMenu = True
            
            self.screen.blit(surface,rectSurface)
            pg.display.update()
            self.clock.tick(25)

    def regles(self):
        """Affichage de la règle du jeu."""
        
        surface = pg.Surface((WIN_WIDTH[0],WIN_HEIGHT[0])).convert()
        surface.set_alpha(200)
        surface.blit(BACKGROUND,(0,0))
        rectSurface = surface.get_rect()
        font = pg.font.Font(PATH_FONT,16)
        texteQuitter = font.render("Echap pour quitter",1,(255,255,255))
        surface.blit(texteQuitter,(0,0))
        
        font = pg.font.Font(PATH_FONT,40)
        titre = font.render("regles du jeu",1,(255,255,100))
        rectTitre = titre.get_rect(centerx=WIN_WIDTH[0]/2,centery=100)
        surface.blit(titre,rectTitre)
 
        font = pg.font.Font(PATH_FONT,40)
        texteTitre = font.render("regles du jeu",1,(50,220,250))
        rectTexteTitre = texteTitre.get_rect(centerx=WIN_WIDTH[0]/2,centery=100)        

        regles=["pour gagner la partie ","il ne doit rester qu'un seul","pion sur le plateau.",
                "lorsqu'un pion saute par dessus un autre","verticalement,horizontalement ou diagonalement",
                "ce dernier disparait."]
        posy = 180
        font = pg.font.Font(PATH_FONT,18)        
        for c in regles:
            texte = font.render(c,1,(255,255,255))
            rectTexte = texte.get_rect(centerx=WIN_WIDTH[0]/2,centery=posy)
            surface.blit(texte,rectTexte)
            posy += 50
        retourMenu = False
        while not retourMenu:
            for event in pg.event.get():
                if event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        retourMenu = True
            
            self.screen.blit(surface,rectSurface)
            pg.display.update()
            self.clock.tick(25)           
    def display_fps(self):
        """Montre le taux de FPS."""

        caption = "{} - FPS: {:.0f}/{}".format(TITRE, self.clock.get_fps(),FPS)
        pg.display.set_caption(caption)

    def main_loop(self):
        """Boucle principale."""

        self.retourMenu = False
        while not self.retourMenu:
            self.event_loop()
            self.update()
            self.draw()
            pg.display.flip()
            self.clock.tick(FPS)
            self.display_fps()        

    def creation_surface_menu(self):
        """Création des surface à bliter dans le menu."""
        
        self.surfaceMenu = pg.Surface((WIN_WIDTH[0],WIN_HEIGHT[0])).convert()
        self.surfaceMenu.set_alpha(200)
        rectSurfaceMenu = self.surfaceMenu.get_rect()

        font = pg.font.Font(PATH_FONT,40)
        texteTitre = font.render("solitaire chinois",1,(50,220,250))
        rectTexteTitre = texteTitre.get_rect(centerx=WIN_WIDTH[0]/2,centery=100)
        font = pg.font.Font(PATH_FONT,30)
        texteOpt1 = font.render("1 : Jeu",1,(250,250,250))
        rectTexteOpt1 = texteOpt1.get_rect(x=rectTexteTitre.x+40,centery=200)        
        texteOpt2 = font.render("2 : Options",1,(250,250,250))
        rectTexteOpt2 = texteOpt2.get_rect(x=rectTexteTitre.x+40,centery=260)
        texteOpt3 = font.render("3 : Credits",1,(250,250,250))
        rectTexteOpt3 = texteOpt3.get_rect(x=rectTexteTitre.x+40,centery=320)
        texteOpt4 = font.render("4 : Regles",1,(250,250,250))
        rectTexteOpt4 = texteOpt4.get_rect(x=rectTexteTitre.x+40,centery=380)        

        self.surfaceMenu.blit(BACKGROUND,(0,0))
        self.surfaceMenu.blit(texteTitre,rectTexteTitre)
        self.surfaceMenu.blit(texteOpt1,rectTexteOpt1)
        self.surfaceMenu.blit(texteOpt2,rectTexteOpt2)
        self.surfaceMenu.blit(texteOpt3,rectTexteOpt3)
        self.surfaceMenu.blit(texteOpt4,rectTexteOpt4)        
        
    def menu(self):
        """"Menu principal."""

        pg.mouse.set_visible(False)
        pg.mixer.music.load(MUSIQUE)
        pg.mixer.music.play(-1)

        self.creation_surface_menu()

        while not self.quitterJeu:
            for event in pg.event.get():
                if event.type == KEYUP:
                    # Quitter le jeu
                    if event.key == K_ESCAPE:
                        self.quitterJeu = True
                    # Nouvelle partie
                    if event.key == K_KP1:
                        pg.mouse.set_visible(True)
                        self.plateau = Level(self.screen,scoreBattre=self.scoreBattre)
                        self.interface = Interface(self.screen,self.plateau,scoreBattre=self.scoreBattre)
                        self.main_loop()
                        pg.mouse.set_visible(False)
                    # Options
                    elif event.key == K_KP2:
                        options = Ecran_Options(self.screen,self.interface,imageMenu=BACKGROUND,options=[['Plein Ecran : ',MODE_ECRAN,[0,FULLSCREEN]],
                                                                                                         ['Volume Musique : ',VOLUME_MUSIQUE,range(11)],
                                                                                                         ['Volume Son : ',VOLUME_SON,range(11)]])
                    # Credits
                    elif event.key == K_KP3:
                        self.credits()
                    # Regles
                    elif event.key == K_KP4:
                        self.regles()

            self.screen.blit(self.surfaceMenu,(0,0))            
            pg.display.flip()

            self.clock.tick(FPS)
            self.display_fps()

        
if __name__ == "__main__":

    solitaireChinois = SOLITAIRE_CHINOIS()
    solitaireChinois.menu()
    
    pg.quit()
    try:
        sys.exit()
    except:
        pass
