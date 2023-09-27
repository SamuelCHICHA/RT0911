from __future__ import annotations
from collections.abc import Callable
import json
from typing import Any

# Classe Point
class Point:
    class Encoder(json.JSONEncoder):
        def default(self, o: Point) -> dict:
            return o.__dict__
        
    class Decoder(json.JSONDecoder):
        def decode(self, s: str) -> Point:
            obj = super().decode(s)
            return Point(obj['x'], obj['y'])
    
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
    def __repr__(self) -> str:
        return f"({self.x},{self.y})"
    
    def __str__(self) -> str:
        return f"Point {json.dumps(self, cls=self.__class__.Encoder)}"
    
    def __eq__(self, __value: object) -> bool:
        return __value.x == self.x and __value.y == self.y
    
    