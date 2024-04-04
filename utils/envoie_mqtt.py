import paho.mqtt.client as mqtt 
import time
import random

broker_hostname = "194.57.103.203"
port = 1883 

def on_connect(client, userdata, flags, return_code):
    if return_code == 0:
        print("connected")
    else:
        print("could not connect, return code:", return_code)

client = mqtt.Client("Client1")
# client.username_pw_set(username="user_name", password="password") # uncomment if you use password auth
client.on_connect=on_connect

client.connect(broker_hostname, port)
client.loop_start()

topic1 = "vehicle"
topic2 = "positions"
msg_count = 0
tabfeux = [0,0.5,1,1.5]

try:
    while msg_count < 1000000:
        time.sleep(1)
        msg_count += 1
        
        # Publication des positions des véhicules
        result1 = client.publish(topic1, "{\"id\": " + str(random.randint(0, 98)) + ", \"vtype\": 1, \"x\": " + str(random.randint(0, 99)) + "," + "\"y\": " + str(random.randint(0, 99)) + ", \"dir\": 0, \"speed\": 0}")
        # result1 = client.publish(topic1, "{\"id\": " + str(random.randint(0, 98)) + ", \"Pos\": " + str(random.randint(0, 99)) + "," + str(random.randint(0, 99)) + ", \"direction\": 0}")
        # result1 = client.publish(topic1, "{\"id\": " + str(random.randint(0, 98)) + ", \"Pos\": " + str(random.randint(0, 99)) + "," + str(random.randint(0, 99)) + ", \"direction\": 0}")
        # result1 = client.publish(topic1, "{\"id\": " + str(random.randint(0, 98)) + ", \"Pos\": " + str(random.randint(0, 99)) + "," + str(random.randint(0, 99)) + ", \"direction\": 0}")
        # result1 = client.publish(topic1, "{\"id\": " + str(random.randint(0, 98)) + ", \"Pos\": " + str(random.randint(0, 99)) + "," + str(random.randint(0, 99)) + ", \"direction\": 0}")
        # result1 = client.publish(topic1, "{\"id\": " + str(random.randint(0, 98)) + ", \"Pos\": " + str(random.randint(0, 99)) + "," + str(random.randint(0, 99)) + ", \"direction\": 0}")
        
        # Publication des etats des feux
        # result2 = client.publish(topic2, "{\"id\": " + str(random.randint(1, 29)) +", \"direction\": " + str(tabfeux[random.randint(0, 3)]) + ", \"etat\": " + str(random.randint(0, 1)) + "}")
        # result2 = client.publish(topic2, "{\"id\": " + str(random.randint(1, 29)) +", \"direction\": " + str(tabfeux[random.randint(0, 3)]) + ", \"etat\": " + str(random.randint(0, 1)) + "}")
        # result2 = client.publish(topic2, "{\"id\": " + str(random.randint(1, 29)) +", \"direction\": " + str(tabfeux[random.randint(0, 3)]) + ", \"etat\": " + str(random.randint(0, 1)) + "}")
        # result2 = client.publish(topic2, "{\"id\": " + str(random.randint(1, 29)) +", \"direction\": " + str(tabfeux[random.randint(0, 3)]) + ", \"etat\": " + str(random.randint(0, 1)) + "}")
        # result2 = client.publish(topic2, "{\"id\": " + str(random.randint(1, 29)) +", \"direction\": " + str(tabfeux[random.randint(0, 3)]) + ", \"etat\": " + str(random.randint(0, 1)) + "}")
        
        # Vérifications que le message est bien envoyé dans la file
        status = result1[0]
        if status == 0:
            print("Message "+ str(msg_count) + " is published to topic " + str(topic1))
        else:
            print("Failed to send message to topic " + str(topic1))
            
        # Vérifications que le message est bien envoyé dans la file
        # status = result2[0]
        # if status == 0:
        #     print("Message "+ str(msg_count) + " is published to topic " + topic2)
        # else:
        #     print("Failed to send message to topic " + topic2)
finally:
    client.loop_stop()