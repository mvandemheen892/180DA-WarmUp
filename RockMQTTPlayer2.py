import paho.mqtt.client as mqtt

# 0. define callbacks - functions that run when events happen.
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
  print("Connection returned result: " + str(rc))
  # Subscribing in on_connect() means that if we lose the connection and
  # reconnect then subscriptions will be renewed.
  client.subscribe("ece180d/rockpaperscissors/servertoplayer2", qos=1) 
  
# The callback of the client when it disconnects.
def on_disconnect(client, userdata, rc):
  if rc != 0:
    print('Unexpected Disconnect')
  else:
    print('Expected Disconnect')
# The default message callback.
# (you can create separate callbacks per subscribed topic)
def on_message(client, userdata, message):

    if message.topic == "ece180d/rockpaperscissors/servertoplayer2":
        message_to_send=str(message.payload)
        serverMessage=message_to_send[2:-1]
        if serverMessage == "What is your choice?":
            player2move = input("What is your choice!\n")
            client.publish("ece180d/rockpaperscissors/player2toserver",player2move,qos=1)
        else:
           print(serverMessage) 

# 1. create a client instance.
client = mqtt.Client()
# add additional client options (security, certifications, etc.)
# many default options should be good to start off.
# add callbacks to client.
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
# 2. connect to a broker using one of the connect*() functions.
# client.connect_async("test.mosquitto.org")
client.connect_async('mqtt.eclipseprojects.io')
# client.connect("test.mosquitto.org", 1883, 60)
# client.connect("mqtt.eclipse.org")
# 3. call one of the loop*() functions to maintain network traffic flow with the broker.
client.loop_start()

# client.loop_forever()
while True: 
    pass  # do your non-blocked other stuff here, like receive IMU data or something.
# use subscribe() to subscribe to a topic and receive messages.
# use publish() to publish messages to the broker.
# use disconnect() to disconnect from the broker.
client.loop_stop()
client.disconnect()
