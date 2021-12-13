import wk12a_util
import json
import paho.mqtt.client as mqtt


def on_connect(mqttc, rc):
    print('connected...rc=' + str(rc))
    mqttc.subscribe(topic='network/#', qoss=0)


def on_disconnect(rc):
    print('disconnected...rc=' + str(rc))


def on_message(msg):
    print("Received message --------")
    print('topic: ' + msg.topic + ', qoss: ' + 
          str(msg.qoss) + ', message: ' + str(msg.payload))
    decode_msg(msg.payload)    


def on_subscribe(granted_qos):
    print('subscribed (qoss=' + str(granted_qos) + ')')


def on_unsubscribe(granted_qos):
    print('unsubscribed (qoss=' + str(granted_qos) + ')')


''' Decode recived message '''
def decode_msg(msg):
    msg = msg.decode('utf-8')
    payload = json.loads(msg)
    print("\n-------- Decoded msg -----------\n")
    wk12a_util.print_data(payload)


# Create Mqtt client
mqttc = mqtt.Client()
# Register callbacks
mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
mqttc.on_message = on_message
mqttc.on_subscribe = on_subscribe
mqttc.on_unsubscribe = on_unsubscribe
# Connect to Mqtt broker on specified host and port
mqttc.connect(host='127.0.0.1', port=4206)
# Run Client forever
mqttc.loop_forever()