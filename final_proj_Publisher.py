import json
import time, sys
import paho.mqtt.client as mqtt
import dataGen as dg

broker_address = '192.168. 1.32'
# delay = 0.2

nclients = 3
max_msg = 2

all_clients = []
for i in range(nclients):
    t = int(time.time())

    client_id= "Client_{}_{}_".format(i, t) 
    print('create:', client_id)
    
    
def on_connect(mqttc, userdata, flags, rc):
    print('connected...rc=' + str(rc))


def on_disconnect(mqttc, userdata, rc):
    print('disconnected...rc=' + str(rc))


def on_message(mqttc, userdata, msg):
    print('message received...')
    print('topic: ' + msg.topic + ', qos: ' + 
          str(msg.qos) + ', message: ' + str(msg.payload))


def on_publish(mqttc, userdata, mid):
    print("Message published ID :{}".format(mid))

mqttc = mqtt.Client(client_id) 
mqttc.connect(broker_address)  
mqttc = mqtt.Client()
mqttc.on_disconnect = on_disconnect
mqttc.on_message = on_message
mqttc.on_publish = on_publish
mqttc.loop_start() 
all_clients.append([client_id, mqttc])
mqttc.connect(host= broker_address, port=4206)

count = 0
while True:
    try:
        msg_dict = dg.desired_val()
        data = json.dumps(msg_dict)
        mqttc.publish(topic='network', payload=data, qos=0)
        print("Published msg: {}".format(msg_dict))
        count += 1
        if count >= max_msg:
            break  
        time.sleep(5)
    except (KeyboardInterrupt, SystemExit):
        mqtt.disconnect()
        sys.exit()

mqttc.disconnect()