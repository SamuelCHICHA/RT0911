from __future__ import annotations
import json

# Classe Point
class Point:
    
    # Initialisation du point
    def __init__(self, x : int, y : int):
        self.x = x
        self.y = y
        
    # Vérification si le point est vide
    def verifierSiPointVide(position : Point, points : Point) -> bool:
        for p in points:
            if(p.x == position.x and p.y == position.y):
                return False
        return True
        
    # Affichage du point
    def __str__(self):
        return f"(x:{self.x}; y:{self.y})"
    
    def __eq__(self, __value: object) -> bool:
        return __value.x == self.x and __value.y == self.y
    
    
    # Convertir un point en JSON
    def convertirJson(self): 
        x = {
            "x": self.x,
            "y": self.y,
        }
        return json.dumps(x)