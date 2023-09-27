from __future__ import annotations
import json
from typing import Tuple

# Classe Point
class Point:
    class Encoder(json.JSONEncoder):
        def default(self, o: Point) -> dict:
            return o.__dict__
        
    class Decoder(json.JSONDecoder):
        def decode(self, s: str) -> Point:
            obj = super().decode(s)
            return Point(obj['x'], obj['y'])
    
    def __init__(self, x : int, y : int):
        self.x = x
        self.y = y
        
    @staticmethod
    def from_tuple(couple: Tuple[int, int]):
        x, y = couple
        return Point(x, y)

    def __repr__(self) -> str:
        return f"({self.x},{self.y})"
    
    def __str__(self) -> str:
        return f"Point {json.dumps(self, cls=self.__class__.Encoder)}"
    
    def __eq__(self, __value: object) -> bool:
        return __value.x == self.x and __value.y == self.y
    
    def __sub__(self, __value: Point) -> Point:
        return Point(self.x - __value.x, self.y - __value.y)
    
    def __gt__(self, __value: Point) -> bool:
        return self.x > __value.x and self.y > __value.y
    
    def __lt__(self, __value: Point) -> bool:
        return self.x < __value.x and self.y < __value.y
    
    def __ge__(self, __value: Point) -> bool:
        return self.x >= __value.x and self.y >= __value.y
    
    def __le__(self, __value: Point) -> bool:
        return self.x <= __value.x and self.y <= __value.y
