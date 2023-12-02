from __future__ import annotations
from .Point import Point

class Light(Point): 
    def __init__(self, id: int, position : Point, directions: dict = {"east": 1, "north": 1, "west": 1, "south": 1}):
        super().__init__(position.x, position.y)
        self.id = id
        self.directions = directions
        
    def __repr__(self):
        return f"(id = {self.id} {super().__repr__()} directions = {self.directions})"        