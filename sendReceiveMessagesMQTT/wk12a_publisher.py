import json
import wk12a_util
import time, sys
import paho.mqtt.client as mqtt


def on_connect(rc):
    print('connected...rc=' + str(rc))


def on_disconnect(rc):
    print('disconnected...rc=' + str(rc))


def on_message(msg):
    print('message received...')
    print('topic: ' + msg.topic + ', qoss: ' + 
          str(msg.qoss) + ', message: ' + str(msg.payload))


def on_publish(mid):
    print("published message ID :{}".format(mid))


# Creating Mqtt client
mqttc = mqtt.Client()
# Register callbacks
mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
mqttc.on_message = on_message
mqttc.on_publish = on_publish
# Connect to Mqtt broker on specified host and port
mqttc.connect(host='localhost', port=4206)


''' Message publish cycle up to max limit - max_msg
If max_msg == 1 then only 1 message will be published and cycle will stop '''
max_msg = 2
count = 0
while True:
    try:
        # Create payload data
        msg_dict = wk12a_util.create_data() 
        # Convert to string    
        data = json.dumps(msg_dict)
        # Publish on a topic
        mqttc.publish(topic='network', payload=data, qoss=0)
        print("Published msg: {}".format(msg_dict))
        # increament published cycle count
        count += 1
        # Break when max cycle count achieved
        if count >= max_msg:
            break 
        # Sleep loop for 5 senconds       
        time.sleep(5)
    except (KeyboardInterrupt, SystemExit):
        mqtt.disconnect()
        sys.exit()
# Dsconnect from Mqtt broker
mqttc.disconnect()