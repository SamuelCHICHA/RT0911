import paho.mqtt.client as mqtt 
import time
import random
import json

broker_hostname = "194.57.103.203"
port = 1883 

client = mqtt.Client("Client1")
client.connect(broker_hostname, port)

lights = {
    1 : "0,0,0,0",
    2 : "0,0,0,0",
    3 : "0,0,0,0",
    4 : "0,0,0,0",
    5 : "0,0,0,0",
    6 : "0,0,0,0",
    7 : "0,0,0,0",
    8 : "0,0,0,0",
    9 : "0,0,0,0",
    10 : "0,0,0,0",
    12 : "0,0,0,0",
    13 : "0,0,0,0",
    14 : "0,0,0,0",
    15 : "0,0,0,0",
    16 : "0,0,0,0",
    17 : "0,0,0,0",
    18 : "0,0,0,0",
    19 : "0,0,0,0",
    20 : "0,0,0,0",
    21 : "0,0,0,0",
    22 : "0,0,0,0",
    23 : "0,0,0,0",
    24 : "0,0,0,0",
    25 : "0,0,0,0",
    26 : "0,0,0,0",
    27 : "0,0,0,0",
    28 : "0,0,0,0",
    29 : "0,0,0,0",
}

combinaisons = ["0,0,0,0", "1,0,0,0", "0,1,0,0", "0,0,1,0", "0,0,0,1"]

while True:
    # Assigner une combinaison aléatoire à chaque lumière
    for i in range(1, 30):  # Correction de l'itération de 1 à 30 pour correspondre aux clés dans le dictionnaire lights
        lights[i] = random.choice(combinaisons)

    # Convertir le dictionnaire de lumières en JSON
    lights_json = json.dumps(lights)

    # Afficher les lumières avec leurs combinaisons
    print(lights_json)

    # Publier le JSON sur le canal MQTT
    client.publish("lights", lights_json)

    time.sleep(5)
