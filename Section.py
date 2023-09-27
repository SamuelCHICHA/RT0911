from __future__ import annotations
from Point import Point
import json

class Section:
    class Encoder(json.JSONEncoder):
        def default(self, o: Section) -> dict:
            return o.__dict__
        
    class Decoder(json.JSONDecoder):
        def decode(self, s: str) -> Point:
            obj = super().decode(s)
            return Point(obj['id'], obj['posA'], obj['posB'])
    
    def __init__(self, id : int, posA : Point, posB : Point):
        self.id = id
        self.posA = posA
        self.posB = posB

    def __str__(self):
        return f"Section {json.dumps(self, cls=self.__class__.Encoder)}"
    
    def __repr__(self):
        return f"Section {json.dumps(self, cls=self.__class__.Encoder)}"
    
    def __eq__(self, __value: object) -> bool:
        return self.id == __value.id and __value.posA == self.posA and __value.posB == self.posB

    def get_translation(self) -> Point:
        return self.posB - self.posA