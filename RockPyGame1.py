import pygame
import paho.mqtt.client as mqtt


#pygame setup
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    MOUSEBUTTONDOWN,
)


readyToPlay=False
DidPlayerMove=False
recievedResults=False
displayTotalsFlag=False
recievedClearToSend=False
resultsMessage=''
playerMove=''
resultsMessage=''
PlayerWins=0
OpponentWins=0

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

running = True
BLUE = (0, 0, 255)
GREEN =(1,50,32)
LIGHT_GREEN=(56,93,56)
WHITE=(255,255,255)
font = pygame.font.SysFont('Corbel', 30)
rects=[]
#welcome = font.render('Welcome to Rock, Paper, Scissors Virtual Version 2.0!', True, WHITE)
#readyToPlaytext = font.render('Are you ready to play? If so, press up on your keyboard!',True, WHITE)


def drawtext(text,color1,fontToUse='Corbel',size=30):
    font=pygame.font.SysFont(fontToUse,size)
    textSurface=font.render(text,True,color1)
    return textSurface
def isValidMove(move):
    if move=='rock' or move =='paper' or move == 'scissors':
        return True
    else:
        return False
def isRock(move):
    if move== 'rock':
        return True
    else:
        return False
def isPaper(move):
    if move== 'paper':
        return True
    else:
        return False
def isScissors(move):
    if move== 'scissors':
        return True
    else:
        return False
def setMove(index):
    if index==0:
        return "rock"
    elif index == 1:
        return 'paper'
    elif index == 2:
        return 'scissors'




#MQTT setup


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
  client.subscribe("ece180d/rockpaperscissors/servertoplayer1", qos=1)
  
  
# The callback of the client when it disconnects.
def on_disconnect(client, userdata, rc):
  if rc != 0:
    print('Unexpected Disconnect')
  else:
    print('Expected Disconnect')
# The default message callback.
# (you can create separate callbacks per subscribed topic)
# The default message callback.
# (you can create separate callbacks per subscribed topic)
def on_message(client, userdata, message):
    if message.topic == "ece180d/rockpaperscissors/servertoplayer1":
        message_to_send=str(message.payload)
        serverMessage=message_to_send[2:-1]
        if serverMessage == "cleartosend":
            global recievedClearToSend
            recievedClearToSend = True
            print(serverMessage)
        else:
            print(serverMessage)
            global recievedResults
            recievedResults=True
            global resultsMessage
            resultsMessage=serverMessage
            reverse_results= resultsMessage[::-1]
            if reverse_results[0:4] == "!eit":
                pass
            elif reverse_results[0:4] == "!tso":
                global OpponentWins
                OpponentWins = OpponentWins +1
            elif reverse_results[0:4] == "!now": 
                global PlayerWins
                PlayerWins = PlayerWins+1
           

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

# 3. call one of the loop*() functions to maintain network traffic flow with the broker.
client.loop_start()

# client.loop_forever()
while True: 
    while running:
        mouse = pygame.mouse.get_pos()


        
        for event in pygame.event.get():
            #print(event)
            # Did the user hit a key?
            if event.type == KEYDOWN:
                # Was it the Escape key? If so, stop the loop.
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_UP and (not readyToPlay) and recievedClearToSend:
                    readyToPlay = True
                elif event.key == K_UP and recievedResults:
                    readyToPlay= False
                    recievedResults =False
                    resultsMessage=''
                    playerMove=''
                    DidPlayerMove=False
                elif event.key == K_DOWN:
                    displayTotalsFlag= not displayTotalsFlag
            elif event.type == MOUSEBUTTONDOWN and readyToPlay:
                for index,rect in enumerate(rects):
                    if rect.collidepoint(pygame.mouse.get_pos()):
                        playerMove=setMove(index)
                        DidPlayerMove=True
                        client.publish('ece180d/rockpaperscissors/player1toserver',playerMove,qos=1)
                        break
                    else:
                        continue
            # Did the user click the window close button? If so, stop the loop.
            elif event.type == QUIT:
                running = False
        
        screen.fill((255, 255, 255))

        surf = pygame.Surface((50, 50))
        #Display Stuff
        if displayTotalsFlag:
                totals=drawtext("You have won " + str(PlayerWins)+ " games and have lost " + str(OpponentWins)+".",WHITE)
                totals_rect=totals.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
                pygame.draw.rect(screen,GREEN,totals_rect)
                screen.blit(totals,totals_rect)
        elif not readyToPlay:
            welcome=drawtext('Welcome to Rock, Paper, Scissors Virtual Version 2.0!',WHITE)
            readyToPlaytext=drawtext('If your ready to play press up on your keyboard!',WHITE)
            welcome_rect = welcome.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2-30))
            readyToPlaytext_rect=readyToPlaytext.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2+10))
            pygame.draw.rect(screen,GREEN,welcome_rect)
            pygame.draw.rect(screen,GREEN,readyToPlaytext_rect)
            screen.blit(welcome,welcome_rect)
            screen.blit(readyToPlaytext,readyToPlaytext_rect)
        else:
            if not DidPlayerMove:
                movePrompt=drawtext("Make your move!Click on your Choice!",WHITE)
                movePrompt_rect=movePrompt.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2-100))
                pygame.draw.rect(screen,GREEN,movePrompt_rect)
                screen.blit(movePrompt,movePrompt_rect)
                rock=drawtext("Rock",WHITE)
                paper=drawtext("Paper",WHITE)
                scissors=drawtext("Scissor",WHITE)
                rock_rect=rock.get_rect(center=(SCREEN_WIDTH/2-100, SCREEN_HEIGHT/2))
                paper_rect=paper.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2+75))
                scissors_rect=scissors.get_rect(center=((SCREEN_WIDTH/2+100, SCREEN_HEIGHT/2)))
                rects=[rock_rect,paper_rect,scissors_rect]
                choices=[rock,paper,scissors]
                for rect in rects:
                    if rect.collidepoint(pygame.mouse.get_pos()):
                        pygame.draw.rect(screen,LIGHT_GREEN,rect)
                    else:
                        pygame.draw.rect(screen,GREEN,rect)
                screen.blit(rock,rock_rect)
                screen.blit(paper,paper_rect)
                screen.blit(scissors,scissors_rect)

            elif DidPlayerMove:
                if (not recievedResults):
                    waiting = drawtext("Waiting for the other player to make a choice!",WHITE)
                    waiting_rect = waiting.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
                    pygame.draw.rect(screen,GREEN,waiting_rect)
                    screen.blit(waiting,waiting_rect)
                elif recievedResults:
                
                    results = drawtext(resultsMessage,WHITE)
                    results_rect = waiting.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
                    pygame.draw.rect(screen,GREEN,results_rect)
                    screen.blit(results,results_rect)

        pygame.display.flip()


client.loop_stop()
client.disconnect()

   












