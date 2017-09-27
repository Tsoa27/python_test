# -*- coding: Utf-8 -*

from constantes import *
from variables import *
from sprites import *

class Level(object):
    """Classe Level qui gère la mise à jour des éléments (déplacements) et leur blitting."""
    
    def __init__ (self,screen,scoreBattre=0,modeDemo=False,surfaceMenu=None):

        # la surface de dessin correspondant au display
        self.screen = screen

        # la surface du menu a dessiner en mode démo cf.:def update_demo() si présente
        self.surfaceMenu = surfaceMenu

        # booleens de contrôle de la partie
        self.gameOver = False
        self.partieGagnee = False

        # le score à battre
        self.scoreBattre = 0

        # containers pour les différents sprites
        # pg.sprite.LayeredUpdates(),pg.sprite.OrderedUpdates(),pg.sprite.Group(),pg.sprite.GroupSingle()
        
        Pion.containers = pg.sprite.LayeredUpdates()
    
        # indice de déplacement dans la liste des images de pions
        self.indiceListeImagesPions = 0

        # le pion sélectionné
        self.pionSelectionne = None
        # le pion retiré
        self.pionRetire = pg.sprite.GroupSingle()

        # le nombre de déplacements possibles
        self.nbrMouvementsPossibles = 0

        # la matrice 2:position interdite, 1:pion, 0:espace libre
        self.matrice = [[2,2,1,1,1,2,2],
                        [2,2,1,1,1,2,2],
                        [1,1,1,1,1,1,1],
                        [1,1,1,0,1,1,1],
                        [1,1,1,1,1,1,1],
                        [2,2,1,1,1,2,2],
                        [2,2,1,1,1,2,2]]

 
        # création des pions
        for indiceLigne in range(len(self.matrice)):
            for indiceColonne in range(len(self.matrice[0])):
                if self.matrice[indiceLigne][indiceColonne] == 1:
                    pion = Pion(indiceColonne,indiceLigne,IMAGE_PION1,None)

        # recherche initiale des mouvements possibles
        self.recherche_mouvements_possibles()

    def changement_image(self):
        """Lorsque l'on veut changer l'image des pions."""
        
        self.indiceListeImagesPions = (self.indiceListeImagesPions+1)%len(LISTE_IMAGES_PIONS)
        for pion in Pion.containers.sprites():
            pion.imageOriginale = LISTE_IMAGES_PIONS[self.indiceListeImagesPions]
            pion.image = pion.imageOriginale

    def mouse_button_down(self):
        """Click souris sur un pion."""
        
        hitList = Pion.containers.get_sprites_at(pg.mouse.get_pos())
        if hitList:
            self.pionSelectionne = hitList[0]
            Pion.containers.move_to_front(self.pionSelectionne)
            self.pionSelectionne.image = pg.transform.smoothscale(self.pionSelectionne.image,(self.pionSelectionne.rect.w+5,self.pionSelectionne.rect.h+5))
            self.pionSelectionne.rect = self.pionSelectionne.image.get_rect(center=self.pionSelectionne.rectOriginal.center)
            #SON_PIECE_SELECTIONNEE.play()

    def mouse_button_up(self):
        """Relachement de la souris."""
        
        if self.pionSelectionne:
            # calcule des coordonnées en ligne et colonne du pion au momment du relachement
            indiceColonne = (self.pionSelectionne.rect.centerx-self.pionSelectionne.offset_x)/64
            indiceLigne = (self.pionSelectionne.rect.centery-self.pionSelectionne.offset_y)/64

            # on s'assure qu'on ne sort pas des limites de la matrice
            if indiceLigne in range(7) and indiceColonne in range(7):
                # test si le déplacement est valide
                # 1ere ligne : déplacement diagonal ou vertical égal à 2, 2eme ligne : déplacement horizontal égal à 2
                if (abs(self.pionSelectionne.indiceLigne-indiceLigne) == 2 and ((abs(self.pionSelectionne.indiceColonne-indiceColonne)==2) or abs(self.pionSelectionne.indiceColonne-indiceColonne)==0)) or\
                   (abs(self.pionSelectionne.indiceColonne-indiceColonne) == 2 and (abs(self.pionSelectionne.indiceLigne-indiceLigne)==0)):
                    # la place est-elle libre ?
                    if self.matrice[indiceLigne][indiceColonne] == 0:
                        colonnePionRetire = indiceColonne
                        lignePionRetire = indiceLigne
                        # calcule des coordonnées de l'emplacement entre  l'ancienne et la nouvelle place
                        if (self.pionSelectionne.indiceColonne-indiceColonne) < 0:
                            colonnePionRetire = indiceColonne - 1
                        elif (self.pionSelectionne.indiceColonne-indiceColonne) > 0:
                            colonnePionRetire = indiceColonne + 1
                        if (self.pionSelectionne.indiceLigne-indiceLigne) < 0:
                            lignePionRetire = indiceLigne - 1
                        elif (self.pionSelectionne.indiceLigne-indiceLigne) > 0:
                            lignePionRetire = indiceLigne + 1
                        # si un pion y est présent
                        if self.matrice[lignePionRetire][colonnePionRetire] == 1:
                            # on le trouvera dans le groupe des pions par sa position en pixels grace à 'get_sprites_at((x,y)) en tenant compte des marges de positionnement (offset)
                            self.pionRetire.add(Pion.containers.get_sprites_at((colonnePionRetire*LARGEUR_GEMME+self.pionSelectionne.offset_x,lignePionRetire*HAUTEUR_GEMME+self.pionSelectionne.offset_y))[0])
                            # mise à jour de la matrice : 2 vides sont créés et 1 rempli
                            self.matrice[self.pionRetire.sprite.indiceLigne][self.pionRetire.sprite.indiceColonne] = 0
                            self.matrice[self.pionSelectionne.indiceLigne][self.pionSelectionne.indiceColonne] = 0
                            self.matrice[indiceLigne][indiceColonne] = 1                        
                            self.pionSelectionne.positionnement(True)
                        else:
                            self.pionSelectionne.positionnement(False)                    
                    else:
                        self.pionSelectionne.positionnement(False)                    
                else:
                    self.pionSelectionne.positionnement(False)
            else:
                self.pionSelectionne.positionnement(False)

            self.pionSelectionne = None
            #SON_PIECE_POSITIONNEE.play()
                        
    def recherche_mouvements_possibles(self):
        """Recherche des mouvements possibles en fonction des coordonnées de chaque vide de la matrice.
           2 pions doivent être présents consécutivement suivant les 8 directions menant à ce vide."""

        self.nbrMouvementsPossibles = 0
        for ligne in range(len(self.matrice)):
            for colonne in range(len(self.matrice[0])):
                if self.matrice[ligne][colonne] == 0:
                    # diag haut-gauche
                    for pion in Pion.containers.sprites():
                        if pion.indiceLigne == ligne-2 and pion.indiceColonne == colonne-2 :
                            for pion2 in Pion.containers.sprites():
                                if pion2.indiceLigne == ligne-1 and pion2.indiceColonne == colonne-1:
                                    self.nbrMouvementsPossibles += 1
                    # haut
                    for pion in Pion.containers.sprites():
                        if pion.indiceLigne == ligne-2 and pion.indiceColonne == colonne :
                            for pion2 in Pion.containers.sprites():
                                if pion2.indiceLigne == ligne-1 and pion2.indiceColonne == colonne:
                                    self.nbrMouvementsPossibles += 1
                    # diag haut-droite
                    for pion in Pion.containers.sprites():                        
                        if pion.indiceLigne == ligne-2 and pion.indiceColonne == colonne+2 :
                            for pion2 in Pion.containers.sprites():
                                if pion2.indiceLigne == ligne-1 and pion2.indiceColonne == colonne+1:
                                    self.nbrMouvementsPossibles += 1
                    # diag bas-gauche
                    for pion in Pion.containers.sprites():
                        if pion.indiceLigne == ligne+2 and pion.indiceColonne == colonne-2 :
                            for pion2 in Pion.containers.sprites():
                                if pion2.indiceLigne == ligne+1 and pion2.indiceColonne == colonne-1:
                                    self.nbrMouvementsPossibles += 1
                    # bas
                    for pion in Pion.containers.sprites():                        
                        if pion.indiceLigne == ligne+2 and pion.indiceColonne == colonne :
                            for pion2 in Pion.containers.sprites():
                                if pion2.indiceLigne == ligne+1 and pion2.indiceColonne == colonne:
                                    self.nbrMouvementsPossibles += 1
                    # diag bas-droite
                    for pion in Pion.containers.sprites():                        
                        if pion.indiceLigne == ligne+2 and pion.indiceColonne == colonne+2 :
                            for pion2 in Pion.containers.sprites():
                                if pion2.indiceLigne == ligne+1 and pion2.indiceColonne == colonne+1:
                                    self.nbrMouvementsPossibles += 1
                    # gauche
                    for pion in Pion.containers.sprites():
                        if pion.indiceLigne == ligne and pion.indiceColonne == colonne-2:
                            for pion2 in Pion.containers.sprites():
                                if pion2.indiceColonne == colonne-1 and pion2.indiceLigne == ligne:
                                    self.nbrMouvementsPossibles += 1
                    # droite
                    for pion in Pion.containers.sprites():
                        if pion.indiceLigne == ligne and pion.indiceColonne == colonne+2:
                            for pion2 in Pion.containers.sprites():
                                if pion2.indiceColonne == colonne+1 and pion2.indiceLigne == ligne:
                                    self.nbrMouvementsPossibles += 1

    def update(self):
        """"Mise à jour des éléments du plateau."""

        # le pions sélectionné suis la souris
        if self.pionSelectionne:
            self.pionSelectionne.rect.center = pg.mouse.get_pos()

        # le pion retiré disparait en rétrécissant.Arrivé à une certaine dimension il est retiré de tout groupe(cf classe sprites)
        if self.pionRetire:
            self.pionRetire.update(True)
            # quand le pion retiré a disparu, on fait une recherche de mouvements possibles
            if len(self.pionRetire) == 0:
                self.recherche_mouvements_possibles()
                # si il ne reste plus qu'un pion la partie est gagnée
                if len(Pion.containers) == 1:
                    self.scoreBattre = len(Pion.containers)
                    self.partieGagnee = True
                # si il n'y a plus de mouvement possible la partie est perdue
                elif self.nbrMouvementsPossibles == 0:
                    self.scoreBattre = len(Pion.containers)
                    self.gameOver = True
                

    def draw(self):
        """Dessin des éléments du jeu dans le display."""

        # les points blancs
        for indiceLigne in range(len(self.matrice)):
            for indiceColonne in range(len(self.matrice[0])):
                if self.matrice[indiceLigne][indiceColonne] == 0:
                    pg.draw.circle(self.screen,(255,255,255),((indiceColonne*LARGEUR_GEMME+Pion.containers.sprites()[0].offset_x)+LARGEUR_GEMME/2,(indiceLigne*HAUTEUR_GEMME+Pion.containers.sprites()[0].offset_y)+HAUTEUR_GEMME/2),6,0)

        Pion.containers.draw(self.screen)
