import paho.mqtt.client as mqtt 
import json

broker_hostname = "194.57.103.203"
port = 1883 

client = mqtt.Client("Client3")

def on_message(client, _, msg):
    payload = json.loads(msg.payload.decode())
    print("Message reçu sur le topic {}: {}".format(msg.topic, payload))

client.on_message = on_message
client.connect(broker_hostname, port)

# Boucle principale
while True:
    # Saisie de l'identifiant par l'utilisateur
    # Ouverture de la file "RESP" pour la lecture des réponses
    client.subscribe("RESP")

    # Attente des réponses
    client.loop_start()

    # Maintenant, le programme reste en écoute des réponses sur "RESP"
    try:
        while True:
            pass  # Attendre les réponses
    except KeyboardInterrupt:
        # L'utilisateur a interrompu le programme, nettoyage
        client.loop_stop()
        client.unsubscribe("RESP")

client.disconnect()
