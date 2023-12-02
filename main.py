import json
import threading
import paho.mqtt.client as mqtt_client
from Vehicule import Vehicule
from map.Point import Point
from map.Map import Map
from typing import Tuple

def on_connect(client: mqtt_client, user_data: Tuple[Map, Vehicule, Point], flags, result_code: int):
    client.subscribe("positions")
    client.subscribe("lights")
    client.subscribe("top")

def on_message(client: mqtt_client, _, msg):
    # print(f"{msg.topic} - {msg.payload.decode()}")
    if msg.topic == "top":
        if vehicule.started_since == 0:
            vehicule.started_since = 1
            vehicule._cv.notify()
    if msg.topic == "positions":
        pass
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
# client = mqtt_client.Client(userdata=(map, vehicule, destination))
client = mqtt_client.Client()
thread = threading.Thread(target=vehicule.hit_the_roads, args=(destination, map, client))
thread.start()
client.enable_logger()
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqtt_host, mqtt_port)
client.loop_start()
thread.join()