import json
import threading
import paho.mqtt.client as mqtt_client
from Vehicule import Vehicule
from map.Point import Point
from map.Map import Map
from typing import Tuple
from Observer import Observer

# Lors de la connexion, on s'abonne aux files suivantes
## positions - file contenant la position de l'ensemble des véhicules
## lights - file contenant la position de l'ensemble des feux de circulation
## top - file pour synchroniser le départ des véhicules
def on_connect(client: mqtt_client, user_data: Tuple[Map, Vehicule, Point], flags, result_code: int):
    client.subscribe("positions")
    client.subscribe("lights")
    client.subscribe("top")

# Lors de la récéption d'un message
## top
### On démarre le thread se chargeant du déplacement du véhicule
## lights
### On met à jour les informations sur les feux de circulation
def on_message(client: mqtt_client, _, msg):
    if msg.topic == "top":
        if vehicule.started_since == 0:
            vehicule.started_since = 1
            with vehicule._cv:
                vehicule._cv.notify()
    elif msg.topic == "lights":
        lights = json.loads(msg.payload.decode())
        if not isinstance(lights, dict):
            raise TypeError("Lights are supposed to be a dict.")
        for id, directions in lights.items():
            map.load_light_from_queue(int(id), eval(directions))
            
# Open configuration of car
vehicule = Vehicule.load_vehicule("config/vehicule.ini")

# Open configuration on map
map = Map("config/map.ini")

# Final point to stop the car
destination = Point(70,40)

# Open file configuration file of messages
with open('mqtt_conn_config.json') as mqtt_conn_config_file:
    mqtt_conn_config = json.load(mqtt_conn_config_file)
    mqtt_host = mqtt_conn_config['host']
    mqtt_port = mqtt_conn_config['port']
# On crée le client MQTT
client = mqtt_client.Client()
# On charge un thread de s'occuper du déplacement du véhicule
thread = threading.Thread(target=vehicule.hit_the_roads, args=(destination, map, client))
# On le démarre
thread.start()
# On configure le client MQTT
client.enable_logger()
client.on_connect = on_connect
client.on_message = on_message
# On se connecte à la file
client.connect(mqtt_host, mqtt_port)
# On crée l'observer et on le démarre
observer = Observer(mqtt_host, mqtt_port, vehicule)
observer.start()
client.loop_start()
# On attend que le déplacement du véhicule se finisse pour arrêter l'observer
thread.join()
observer.stop()