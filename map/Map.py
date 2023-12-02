import configparser
from .Section import Section
from .Point import Point
from .Light import Light
from Graph import Graph
from typing import Union

class Map:
    def __init__(self, file_path : str) -> None:
        self.file_path = file_path
        self.sections = None
        self.lights = None
        
    def get_sections(self) -> list[Section]:
        """Get the sections from the map file

        Returns:
            list[Section]: list of sections
        """
        if self.sections is None:
            parser = configparser.ConfigParser()
            parser.read(self.file_path)
            self.sections = []
            for id in parser['trip']:
                xa, ya, xb, yb = eval(parser['trip'][id])
                self.sections.append(Section(int(id), Point(int(xa), int(ya)), Point(int(xb), int(yb))))
        return self.sections
    
    def get_lights(self) -> list[Light]:
        """Get the intersections from the map file

        Returns:
            list[Light]: list of traffic lightsv
        """
        if self.lights is None:
            parser = configparser.ConfigParser()
            parser.read(self.file_path)
            self.lights = []
            for id in parser['trafficLight']:
                x, y = eval(parser['trafficLight'][id])
                self.lights.append(Light(int(id), Point(int(x), int(y))))
        return self.lights

    def get_graph(self) -> Graph:
        """Transforms the map into a graph

        Returns:
            Graph: resulting graph
        """
        matrix = {}
        for section in self.get_sections():
            if section.posA.__repr__() not in matrix.keys():
                matrix[section.posA.__repr__()] = {}
            if section.posB.__repr__() not in matrix[section.posA.__repr__()].keys():
                matrix[section.posA.__repr__()][section.posB.__repr__()] = {}
            matrix[section.posA.__repr__()][section.posB.__repr__()] = abs(section.posA.y - section.posB.y if section.posA.x == section.posB.x else section.posA.x - section.posB.x)
        return Graph(matrix)

    def get_light_from_id(self, id: int) -> Union[Light, None]:
        return next(filter(lambda l: l.id == id, self.get_lights()), None)
    
    def get_light_from_position(self, position: Point) -> Union[Light, None]:
        return next(filter(lambda l: l.x == position.x and l.y == position.y, self.get_lights()), None)
    
    def update_light(self, id: int, directions: dict) -> None:
        light = next(filter(lambda l: l.id == id, self.get_lights()), None)
        if light is None:
            print(self.get_lights())
            raise ValueError("No matching Traffic light.")
        light.directions = {direction: state for direction, state in directions.items() if direction in ['east', 'north', 'west', 'south']}
    
    def load_light_from_queue(self, id: int, directions: tuple):
        east, north, west, south = directions
        self.update_light(id, {
            "east": east,
            "north": north,
            "west": west,
            "south": south
        })