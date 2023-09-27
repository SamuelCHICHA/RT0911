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
            return Point(obj['posA'], obj['posB'])
    
    def __init__(self, posA : Point, posB : Point):
        self.posA = posA
        self.posB = posB

    def __repr__(self):
        return f"Section {json.dumps(self, cls=self.__class__.Encoder)}"
    
    def __eq__(self, __value: object) -> bool:
        return __value.posA == self.posA and __value.posB == self.posB
