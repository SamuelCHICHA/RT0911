import json
import threading
import paho.mqtt.client as mqtt_client
from Vehicule import Vehicule
from Point import Point
from Map import Map
from typing import Tuple


def on_connect(client: mqtt_client, user_data: Tuple[Map, Vehicule, Point], flags, result_code: int):
    client.subscribe("positions")
    client.subscribe("start")

def on_message(client: mqtt_client, user_data: Tuple[Map, Vehicule, Point], msg):
    print(f"{msg.topic} - {msg.payload.decode()}")
    map, vehicule, destination = user_data
    if msg.topic == "positions":
        if vehicule.started_since == 0:
            vehicule.started_since = 1
            thread = threading.Thread(target=vehicule.hit_the_roads, args=(destination, map, client))
            thread.start()
        else:
            pass
    elif msg.topic == "traffic_lights":
        pass
    
# exit()

# TO DO
# Connexion file MQTT
# Pour FOUCHAL
# Demander les informations connexion
# Demander pour slot => temps donné depuis le départ
# Demander pour bidirection vehicule (information sur le sens du véhicule en transit) => heading (angle par rapport à )


vehicule = Vehicule.load_vehicule("config/vehicule.ini")
map = Map("config/map.ini")
destination = Point(70,40)
with open('mqtt_conn_config.json') as mqtt_conn_config_file:
    mqtt_conn_config = json.load(mqtt_conn_config_file)
    mqtt_host = mqtt_conn_config['host']
    mqtt_port = mqtt_conn_config['port']
client = mqtt_client.Client(userdata=(map, vehicule, destination))
client.enable_logger()
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqtt_host, mqtt_port)
client.loop_forever()