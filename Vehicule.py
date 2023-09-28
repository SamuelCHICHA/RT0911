from __future__ import annotations
from Point import Point
import json
import time
import paho.mqtt.client as mqtt_client
import configparser
from Map import Map
from Section import Section
from Light import Light

# Classe Véhicule
class Vehicule:
    class Encoder(json.JSONEncoder):
        def default(self, o: Vehicule) -> dict:
            return o.__dict__
        
    class Decoder(json.JSONDecoder):
        def decode(self, s: str) -> Vehicule:
            obj = super().decode(s)
            return Vehicule(obj['id'], obj['position'], obj['start'], obj['speed'], [])

    # Création d'un véhicule
    def __init__(self, id : int, position : Point, start : int, speed : int, path : list, started_since : int = 0):
        self.id = id
        self.position = position
        self.start = start
        self.speed = speed
        self.path = path
        self.started_since = started_since
    
    # Affichage du véhicule
    def __repr__(self) -> str:
        return f"Vehicule {json.dumps(self, cls=self.__class__.Encoder)}"
    
    def send_position(self, client: mqtt_client) -> None:
        client.publish("position_pub", json.dumps({
            "id": self.id,
            "Pos": f"{self.position.x},{self.position.y}",
            "slot": self.started_since
        }))
        
    @classmethod
    def load_vehicule(cls, file_path : str):
        parser = configparser.ConfigParser()
        parser.read(file_path)
        id = int(parser['general_informations']['id'])
        initial_position = Point.from_tuple(eval(parser['general_informations']['init_position']))
        start = int(parser['general_informations']['time_start'])
        speed = int(parser['general_informations']['speed'])
        return Vehicule(id, initial_position, start, speed, [])
        
    def advance_to_point(self, destination_point: Point) -> None:
        """Move a vehicule on a point according to its speed

        Args:
            destination_point (Point): destination
        """
        translation = destination_point - self.position
        if translation >= Point(0, 0):
            if translation.x > 0: # East
                translation_that_can_be_done = min([translation.x, self.speed])
                self.position.x += translation_that_can_be_done
            else: # North 
                translation_that_can_be_done = min([translation.y, self.speed])
                self.position.y += translation_that_can_be_done
        else:
            if translation.x < 0: # South
                translation_that_can_be_done = min([abs(translation.y), self.speed])
                self.position.y -= translation_that_can_be_done
            else: # West
                translation_that_can_be_done = min([abs(translation.x), self.speed])
                self.position.x -= translation_that_can_be_done

    def get_path(self, map: Map, destination_point: Point) -> list[Point]:
        """Get the shortest path based on a map from the vehicule position to a destination point

        Args:
            map (Map): map
            destination_point (Point): destination

        Returns:
            list[Point]: list of points to go to
        """
        graph = map.get_graph()
        sp = graph.shortest_path(self.position.__repr__(), destination_point.__repr__())
        return [Point.from_tuple(eval(p)) for p in sp]
    
    def hit_the_roads(self, destination: Point, map: Map, client: mqtt_client) -> None:
        time.sleep(self.start)
        # to do change to while to adapt path
        previous_point = self.position
        for next_point in self.get_path(map, destination)[1:]:
            section = next(filter(lambda s: s.posA == previous_point and s.posB == next_point, map.get_sections()), None)
            if section is not None:
                while self.position != section.posB:
                    self.started_since += 1
                    self.advance_to_point(section.posB)
                    print(self)
                    self.send_position(client)
                    time.sleep(1)
                previous_point = next_point
            else:
                raise ValueError(f"This section {previous_point} - {next_point} does not exist.")
        client.loop_stop()