import json
from Vehicule import Vehicule
import paho.mqtt.client as mqtt_client

class Observer:
    def __init__(self, host: str, port: int, vehicule: Vehicule):
        self.vehicule = vehicule
        print(self.vehicule)
        self.client = None
        self.host = host
        self.port = port
        
    @staticmethod
    def on_connect(client: mqtt_client, userdata: Vehicule, flags, result_code: int):
        client.subscribe("UT")
        
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
        self.client = mqtt_client.Client(userdata=self.vehicule)
        self.client.enable_logger()
        self.client.on_connect = self.__class__.on_connect
        self.client.on_message = self.__class__.on_message
        self.client.connect(self.host, self.port)
        self.client.loop_start()
    
    def stop(self):
        self.client.loop_stop()
    