from Vehicule import Vehicule
from map.Map import Map
from map.Point import Point

vehicule = Vehicule.load_vehicule("config/vehicule.ini")
map = Map("config/mini_map.ini")
print(map.get_lights())
map.update_light(1, {"east": 1, "north": 0, "west": 1, "south": 0, "yo": "Oui"})
print(map.get_lights())