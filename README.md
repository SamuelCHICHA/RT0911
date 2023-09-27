# RT0911

## But du projet

Simuler le déplacement d'un véhicule sur une carte. Il devra s'adapter aux différentes contraintes comme les feux rouges et celles posées par les autres véhicules. On obtiendra les informations sur ces dernières à partir des différentes files MQTT mises à diisposition.

## Spécifications

* Le véhicule devra attendre le message donnant le signal de départ, après quoi il attendra x secondes avant de commencer à se déplacer.
* Chaque seconde, le véhicule devra envoyer sa position sur une file MQTT
* Chaque seconde, le véhicule devra récupérer les informations sur une file MQTT.
* Les véhicules doivent se déplacer uniquement sur des routes répertoriées.
* Un véhicule doit s'arrêter quand il atteint un croisement dont le feu est rouge.