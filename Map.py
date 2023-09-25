import json
from Troncon import Troncon
from Point import Point
from Croisement import Croisement

class Map:
    def __init__(self, file_path : str) -> None:
        self.file_path = file_path

    def get_troncons(self) -> list:
        with open(self.file_path) as map_file:
            map = json.load(map_file)
            return [Troncon(Point(troncon['xa'], troncon['ya']), Point(troncon['xb'], troncon['yb'])) for troncon in map['troncons']]
        
    def get_croisements(self) -> list:
        with open(self.file_path) as map_file:
            map = json.load(map_file)
            return [Croisement(Point(croisement['x'], croisement['y'])) for croisement in map['croisements']]