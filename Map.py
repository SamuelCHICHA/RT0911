import configparser
from Section import Section
from Point import Point
from Light import Light
from Graph import Graph

class Map:
    def __init__(self, file_path : str) -> None:
        self.file_path = file_path
        self.sections = None
        self.intersections = None

    def get_sections(self) -> list[Section]:
        """Get the sections from the map file

        Returns:
            list[Section]: list of sections
        """
        if self.sections is None:
            parser = configparser.ConfigParser()
            parser.read(self.file_path)
            self.sections = []
            for id in parser['sections']:
                xa, ya, xb, yb = eval(parser['sections'][id])
                self.sections.append(Section(id, Point(xa, ya), Point(xb, yb)))
        return self.sections
    
    def get_intersections(self) -> list[Light]:
        """Get the intersections from the map file

        Returns:
            list[Intersection]: list of intersections
        """
        if self.intersections is None:
            parser = configparser.ConfigParser()
            parser.read(self.file_path)
            self.intersections = []
            for id in parser['trafficLights']:
                x, y = eval(parser['trafficLights'][id])
                self.intersections.append(Light(Point(x, y)))
        return self.intersections

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

# parser = configparser.ConfigParser()
# parser.read('map.ini')
# for id in parser['trafficLights']:
#     print(id)