import json
from Vehicule import Vehicule
import paho.mqtt.client as mqtt_client

class Observer:
    # On charge les informations de connexion à la file MQTT ainsi que le véhicule
    def __init__(self, host: str, port: int, vehicule: Vehicule):
        self.vehicule = vehicule
        print(self.vehicule)
        self.client = None
        self.host = host
        self.port = port
    
    # Une fois connecté on s'inscrit à la file
    @staticmethod
    def on_connect(client: mqtt_client, userdata: Vehicule, flags, result_code: int):
        client.subscribe("UT")
    
    # Lorsqu'on reçoit un message sur la file UT, on envoit sur la file RESP les informations à l'instant T du véhicule
    @staticmethod
    def on_message(client: mqtt_client, vehicule: Vehicule, msg):
        # print(f"{msg.topic} - {msg.payload.decode()}")
        message = json.loads(msg.payload.decode())
        if msg.topic == "UT":
            if vehicule.id == message['id']:
                client.publish("RESP", json.dumps({
                    "id": vehicule.id,
                    "x": vehicule.position.x,
                    "y": vehicule.position.y,
                    "temps": vehicule.started_since
                }))
                            
    def start(self):
        # On crée le client MQTT et on le configure
        self.client = mqtt_client.Client(userdata=self.vehicule)
        self.client.enable_logger()
        self.client.on_connect = self.__class__.on_connect
        self.client.on_message = self.__class__.on_message
        # On se connecte à la file
        self.client.connect(self.host, self.port)
        self.client.loop_start()
    
    def stop(self):
        self.client.loop_stop()
    