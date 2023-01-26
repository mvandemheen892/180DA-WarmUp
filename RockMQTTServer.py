import paho.mqtt.client as mqtt

OkayToSendFlag= False
DidPlayer1Move= False
DidPlayer2Move= False
player1move = ''
player2move = ''

def whoWon(player1move,player2move):
    if player1move == player2move :
        #tie
        return 0
    elif (player1move == 'rock' and player2move =='scissors') or (player1move == "paper" and player2move == "rock") or (player1move == 'scissors' and player2move == 'paper'):
        return 1
    else:
        return 2









# 0. define callbacks - functions that run when events happen.
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
  print("Connection returned result: " + str(rc))
  # Subscribing in on_connect() means that if we lose the connection and
  # reconnect then subscriptions will be renewed.
  client.subscribe("ece180d/rockpaperscissors/player2toserver", qos=1)
  client.subscribe("ece180d/rockpaperscissors/player1toserver", qos=1)  
  
# The callback of the client when it disconnects.
def on_disconnect(client, userdata, rc):
  if rc != 0:
    print('Unexpected Disconnect')
  else:
    print('Expected Disconnect')
# (you can create separate callbacks per subscribed topic)
def on_message(client, userdata, message):
  print("Reciveved Messages")
  if message.topic == "ece180d/rockpaperscissors/player2toserver" and OkayToSendFlag:
    message_to_send=str(message.payload)
    global player2move
    player2move=message_to_send[2:-1]
    if not (player2move =='rock' or player2move == 'paper' or player2move == 'scissors'):
      client.publish("ece180d/rockpaperscissors/servertoplayer2","That isn't a valid choice!",qos=1)
      client.publish("ece180d/rockpaperscissors/servertoplayer2","What is your choice!",qos=1)
    else:
      print("Player2 Moved")
      global DidPlayer2Move
      DidPlayer2Move = True

  if message.topic == "ece180d/rockpaperscissors/player1toserver" and OkayToSendFlag:
    message_to_send=str(message.payload)
    global player1move
    player1move=message_to_send[2:-1]
    if not (player1move =='rock' or player1move == 'paper' or player1move == 'scissors'):
      client.publish("ece180d/rockpaperscissors/servertoplayer1","That isn't a valid choice!",qos=1)
      client.publish("ece180d/rockpaperscissors/servertoplayer1","What is your choice!",qos=1)
    else:
      global DidPlayer1Move
      DidPlayer1Move = True
      print("Player1 Moved")
            

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

client.publish("ece180d/rockpaperscissors/servertoplayer1","Welcome to Rock Paper Scissors Virtual!",qos=1)
client.publish("ece180d/rockpaperscissors/servertoplayer2","Welcome to Rock Paper Scissors Virtual!",qos=1)


# client.loop_forever()
while True: 
  
  client.publish("ece180d/rockpaperscissors/servertoplayer1","What is your choice?",qos=1)
  client.publish("ece180d/rockpaperscissors/servertoplayer2","What is your choice?",qos=1)
  print("Sent Players the Prompt!")
  OkayToSendFlag=True
  while (not DidPlayer1Move):
    pass
 
  
  while (not DidPlayer2Move):
    pass
  

  print("Both Players Moved")  
  result = whoWon(player1move,player2move)
  if result == 0:
    client.publish("ece180d/rockpaperscissors/servertoplayer1","You both put " + player1move + ", its a tie!",qos=1)
    client.publish("ece180d/rockpaperscissors/servertoplayer2","You both put " + player1move + ", its a tie!",qos=1)
  elif result == 1:
    client.publish("ece180d/rockpaperscissors/servertoplayer1","Player 2 put " + player2move + ", you won!",qos=1)
    client.publish("ece180d/rockpaperscissors/servertoplayer2","Player 1 pu " + player1move + ", you lost!",qos=1)
  elif result == 2:
    client.publish("ece180d/rockpaperscissors/servertoplayer1","Player 2 put " + player2move + ", you lost!",qos=1)
    client.publish("ece180d/rockpaperscissors/servertoplayer2","Player 1 put" + player1move + ", you won!",qos=1)

  OkayToSendFlag= False
  DidPlayer1Move= False
  DidPlayer2Move= False
  player1Move = ''
  player2Move = ''



     # perhaps add a stopping condition using some break or something.
  pass 


client.loop_stop()
client.disconnect()