from __future__ import annotations
from map.Point import Point
import json
import time
import paho.mqtt.client as mqtt_client
import configparser
from map.Map import Map
import threading

# Classe Véhicule
class Vehicule:
    EAST = 0
    NORTH = 1
    WEST = 2
    SOUTH = 3

    class Encoder(json.JSONEncoder):
        def default(self, o: Vehicule) -> dict:
            return {
                'id': o.id,
                'vtype': o.vtype,
                'position': o.position.__dict__,
                'speed': o.speed,
                'started_since': o.started_since,
                'direction': o.direction
            }

    class Decoder(json.JSONDecoder):
        def decode(self, s: str) -> Vehicule:
            obj = super().decode(s)
            return Vehicule(obj['id'], obj['vtype'], Point(obj['x'], obj['y']), obj['dir'], obj['speed'])

    # Création d'un véhicule
    def __init__(self, id : int, vtype : int, position : Point, direction : int, speed : int):
        self.id = id
        self.vtype = vtype
        self.position = position
        self.speed = speed
        self.started_since = 0
        self.direction = direction
        self._cv = threading.Condition()

    # Affichage du véhicule
    def __repr__(self) -> str:
        return f"Vehicule {json.dumps(self, cls=self.__class__.Encoder)}"

    def send_position(self, client: mqtt_client) -> None:
        client.publish("vehicle", json.dumps({
            "id": self.id,
            "vtype": 1, # [0,1,2,3,4,5]
            "x": self.position.x,
            "y": self.position.y,
            "dir": self.direction,
            "speed": self.speed
        }))

    @classmethod
    def load_vehicule(cls, file_path : str) -> Vehicule:
        parser = configparser.ConfigParser()
        parser.read(file_path)
        id = int(parser['general_informations']['id'])
        x = int(parser['general_informations']['x'])
        y = int(parser['general_informations']['y'])
        speed = int(parser['general_informations']['speed'])
        vtype = int(parser['general_informations']['vtype'])
        return Vehicule(id, vtype, Point(x, y), 0, speed)

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
                self.direction = 0
            else: # North
                translation_that_can_be_done = min([translation.y, self.speed])
                self.position.y += translation_that_can_be_done
                self.direction = 1
        else:
            if translation.x < 0: # South
                translation_that_can_be_done = min([abs(translation.y), self.speed])
                self.position.y -= translation_that_can_be_done
                self.direction = 3
            else: # West
                translation_that_can_be_done = min([abs(translation.x), self.speed])
                self.position.x -= translation_that_can_be_done
                self.direction = 2

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
        # to do change to while to adapt path
        with self._cv:
            # Attente de l'action du 'TOP'
            self._cv.wait_for(lambda: self.started_since == 1)
        previous_point = self.position
        for next_point in self.get_path(map, destination)[1:]:
            section = next(filter(lambda s: s.posA == previous_point and s.posB == next_point, map.get_sections()), None)
            if section is None:
                raise ValueError(f"This section {previous_point} - {next_point} does not exist.")
            while self.position != section.posB:
                self.started_since += 1
                self.advance_to_point(section.posB)
                print(self)
                self.send_position(client)
                time.sleep(1)
            light = map.get_light_from_position(section.posB)
            if light is not None:
                print(light)
                stopped = False
                if self.direction == Vehicule.NORTH and light.directions['south'] == 0:
                    stopped = True
                    wait_for = 'south'
                elif self.direction == Vehicule.WEST and light.directions['east'] == 0:
                    stopped = True
                    wait_for = 'east'
                elif self.direction == Vehicule.SOUTH and light.directions['north'] == 0:
                    stopped = True
                    wait_for = 'north'
                elif self.direction == Vehicule.EAST and light.directions['west'] == 0:
                    stopped = True
                    wait_for = 'west'
                if stopped:
                    while light.directions[wait_for] == 0:
                        print(wait_for)
                        print("Waiting for the green light.")
                        print(self)
                        print(light)
                        self.started_since += 1
                        self.send_position(client)
                        time.sleep(1)
                        light = map.get_light_from_position(section.posB)
            previous_point = next_point
        client.loop_stop()