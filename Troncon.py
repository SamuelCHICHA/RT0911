from Point import Point

class Troncon:
    
    # Initialisation du tronçon
    def __init__(self, posA : Point, posB : Point):
        self.posA = posA
        self.posB = posB
        
    # Affichage du tronçon
    def __repr__(self):
        return f"(A:{self.posA.__str__()}; B:{self.posB.__str__()})"
    
    def __eq__(self, __value: object) -> bool:
        return __value.posA == self.posA and __value.posB == self.posB


# t1 = Troncon(Point(1,6), Point(2,5))
# print(t1)