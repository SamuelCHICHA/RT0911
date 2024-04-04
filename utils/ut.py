import paho.mqtt.client as mqtt 
import json

broker_hostname = "194.57.103.203"
port = 1883 

client = mqtt.Client("Client4")

client.connect(broker_hostname, port)

# Boucle principale
# Saisie de l'identifiant par l'utilisateur
id_input = input("Entrez l'identifiant (ou 'q' pour quitter) : ")

# Vérifier si l'utilisateur veut quitter
if id_input.lower() == 'q':
    client.disconnect()

# Publication de l'identifiant sur le topic "UT"
client.publish("UT", "{\"id\": " + id_input + "}")

client.disconnect()
