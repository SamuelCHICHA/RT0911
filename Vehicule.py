from __future__ import annotations
from Point import Point
from MQTTClient import MQTTClient
import json

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
    def __init__(self, id : int, position : Point, start : int, speed : int, path : list):
        self.id = id
        self.position = position
        self.start = start
        self.speed = speed
        self.path = path
    
    # Affichage du véhicule
    def __repr__(self) -> str:
        return f"Vehicule {json.dumps(self, cls=self.__class__.Encoder)}"
    
    def send_position(self, mqtt_client: MQTTClient, time_since_start : int = 0) -> None:
        mqtt_client.client.publish("", json.dumps({
            "id": self.id,
            "Pos": f"{self.position.x}, {self.position.y}",
            "slot": time_since_start
        }))
        
    @classmethod
    def load_vehicule(cls, file_path : str):
        with open(file_path) as vehicule_file:
            vehicule_config = json.load(vehicule_file)
            id = vehicule_config['id']
            initial_position = Point(vehicule_config['path'][0]['x'], vehicule_config['path'][0]['y'])
            start = vehicule_config['start']
            speed = vehicule_config['speed']
            path = vehicule_config['path']
            return Vehicule(id, initial_position, start, speed, path)
