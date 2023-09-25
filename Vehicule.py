from __future__ import annotations
from Point import Point
from MQTTClient import MQTTClient
import json

# Classe Véhicule
class Vehicule:
    
    # Création d'un véhicule
    def __init__(self, id : int, position : Point, start : int, speed : int, hop_number : int, path : list):
        self.id = id
        self.position = position
        self.start = start
        self.speed = speed
        self.hop_number = hop_number
        self.path = path
        
    # Modifier la position du véhicule
    def setPosition(self, position : Point) -> None:
        self.position = position
        
    # Récupérer la position du véhicule
    def getPosition(self) -> Point:
        return self.position
    
    # Affichage du véhicule
    def __str__(self) -> str:
        return f"Véhicule (id:{self.id}; start: {self.start}s; speed: {self.speed}km/h; hop_number: {self.hop_number}sauts, position : {self.position})"
    
    
    # Convertir le véhicule en JSON
    def convertirJson(self) -> str: 
        x = {
            "id": self.id,
            "start": self.start,
            "speed": self.speed,
            "hop_nomber": self.hop_number,
            "position": json.loads(self.position.convertirJson())
        }
        return json.dumps(x)
    
    def send_position(self, mqtt_client: MQTTClient, timestamp : int = 0) -> None:
        mqtt_client.client.publish("", json.dumps({
            "id": self.id,
            "Pos": f"{self.position.x}, {self.position.y}",
            "slot": timestamp
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
            return Vehicule(id, initial_position, start, 0, speed, path)
        
        
    
# Véhicule 1
# v1 = Vehicule(1, Point(0,0) ,12, 20, 2)
# print(v1)
# v1.setPosition(Point(1,65))
# print(v1)


# # Véhicule 3
# v3 = Vehicule(1, Point(1,65) ,12, 20, 2)

# vehicules = [v1.position, v3.position]

# # Véhicule 2
# v2 = Vehicule(1, Point(0,1) ,12, 20, 2)
# print(v2)
# print(Point.verifierSiPointVide(v2.position,vehicules))

# v2.setPosition(Point(1,65))
# print(Point.verifierSiPointVide(v2.position,vehicules))

# print(v1)

# print(v1.convertirJson())