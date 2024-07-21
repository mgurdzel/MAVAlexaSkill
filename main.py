# -------------------------------------
# Mav Controller speech controll Backend
# In diesem Program werden die Befehle aus der Alexa Sprachsteeurung
# vom MQTT Server ausgelesen und in Bewegungsbefehle gewandelt
#
# Die Verbindung zum Netzwerk des Mav und das auslesen der MQTT Nachrichten findet parallelisiert statt
# Als Schnittstelle dient die Marvin-Class dessen Objekt von beiden Threads bearbeitet wird.

# EntwicklerInnen:
# Luca Zimmer
# William Schmidt
# Moritz Gurdzel
# Fanny Zotter
# -----------------------------

import requests
import threading
import marvin_class
import paho.mqtt.client as mqtt

# global variables
# token for mqtt server
token = 0
# manual for mqtt server
manual = 0
# marvin input class objekt global definiert
marvin = marvin_class.input_mav()



# Funktion für das Bewegen des Roboters
def run_while_loop():
    #maybe this is not needed
    session = requests.Session()
    url = 'http://10.10.6.100/'
    response = session.get(url)
    url = 'http://10.10.6.100/jquery.mobile-1.4.5.min.css'
    response = session.get(url)
    url = 'http://10.10.6.100/webInterface.css'
    response = session.get(url)
    url = 'http://10.10.6.100/remote_control?x=0.000&y=0.000&teach=0&manual=0&get_control=0&steer_type=2&omni_forw=1&token=0&loadunload=0&speedScale=1'
    response = session.post(url)


    while 1:
        if marvin.get_breakloop()==True:
            #to kill the thread
            break
        # wenn eine Antwort vom Marvin eingegangen ist hier starten
        if response.status_code == 200:
            # die neue Position vom Marin in der marvin Klasse speichern
            marvin.set_real_coordinates(float(response.text.split(" ")[5]),float(response.text.split(" ")[6]))

            # eingegangene Error nachrichten auslesen
            errors_det = response.text.split(" ")[10]
            # Marker für den Status vom Mav
            navitool_state = response.text.split(" ")[11]
            # Kommunikationstoken für den Mav
            token = response.text.split(" ")[22]

            # Verbindeung zum Mav
            url = f'http://10.10.6.100/remote_control?x={marvin.get_mavX()}&y={marvin.get_mavY()}&teach=0&manual={manual}&get_control=0&steer_type=2&omni_forw=1&token={token}&loadunload=0&speedScale=1'
            response = session.post(url)

            # Berechne die Distanz die der Mav seit dem letzten Update gefahren ist. Wenn es mehr als 21cm sind wird ein Bewegungsschritt gezählt
            if marvin.distanz_2d(marvin.get_lineOfMovement())>=0.21: # wenn etwas distanz zwischen den beiden punkten liegt führe die
                marvin.add_step()
                marvin.set_current_rotation() # Berechne die Richtung in die der Mav sich bewegt (auf kurze Distanzen ungenau)
                print("curr rot:",marvin.get_current_rotation(), marvin.get_XYreal())
                marvin.set_Old_Coordinates(marvin.get_XYreal()) # Update die alten koordinaten um den Bewegungsschritt zu beenden
            if errors_det == '0':

                manual = 1
                # no errors manual mode activated
                if navitool_state == '16':

                    # manual state confirmed
                    marvin.compute_new_data()
            else:
                #if errors to this
                print("errors")
                manual = 0
                marvin.set_mavXY(0,0) # Geschwindigkeit auf 0
                url = url + "&clear_errors=1"

            # print(url)
        else:
            print(f"Fehler: {response.status_code}")


def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("mav/#")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic + "  here  " + str(msg.payload))
    # Mav gets movement information from the mqtt.message
    marvin.move_marvin(msg.topic, msg.payload)
    # we get controll information from the messages

# Kontinuiertlich laufende Abfrage vom mqtt server
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect("test.mosquitto.org", 1883, 60)
#                   addr , port, timeout

# new rand = [5.692,2.715]
# old rand=[5.862,2.517]

while_loop_thread = threading.Thread(target=run_while_loop)
while_loop_thread.start()

input_thread_t= threading.Thread(target=marvin.input_thread)
#input_thread_t.start()
mqttc.loop_forever()
input_thread_t.join()
while_loop_thread.join()
mqttc.loop_stop()