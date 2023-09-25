from Point import Point

class Croisement(Point):
    ROUGE = 0
    VERT = 1
    
    # Etat des feux (croisements)
    
    # Initialisation du croisement
    def __init__(self, position : Point):
        super().__init__(position.x, position.y)
        self.etat = 0
    
    # Récupération de l'état du croisement (Feu)
    def getEtatCroisement(self):
        return self.etat
        
    # Modification de l'état du croisement (Feu)
    def setEtatCroisement(self, etat : int):
        self.etat = etat
        
    def __str__(self):
        feu = "/"
        if self.etat == self.__class__.ROUGE:
            feu = "ROUGE"
        elif self.etat == self.__class__.VERT:
            feu = "VERT"
        return f"({super().__str__()} etat = {feu})"
    
