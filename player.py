#!/usr/bin/python

# This should work in both recent Python 2 and Python 3.

import socket
import json
import struct
import time
import sys

''' statistics code

#takes in arrray up to 13 only uses 1 through 13 as values for cards that have been seen
def updatestats(showncards, hand):
    for card in hand:
        showncards[card] =  showncards[card] + 1
        
#call when a card is shown on the table

def updatestats_tablecard(showncards, tablecard):
    showncards[tablecard] = showncards[tablecard] + 1
    
''' 


def max_card(hand):
    max_value = 0
    for card in hand:
        if(max_value < card):
            max_value = card
    return max_value        

def min_card(hand):
    min_value = 13
    for card in hand:
        if(min_value > card):
            min_value = card
    return min_value

def hand_avg(hand):
    total = 0
    for card in hand:
        total = total + card
    return total / len(hand)
    
    
def desHandAvg(hand, avg):
    return hand_avg(hand) >= avg   
    
def hand_avg_top(hand, topNum):
    temp_hand = []
    for card in hand:
        temp_hand.append(card)
        
    max_hand = []
    for i in range(0, topNum):
        maxNum = max_card(temp_hand)
        max_hand.append(maxNum)
        temp_hand.remove(maxNum)
        
    return hand_avg(max_hand)

def desHandAvgMax(hand, avg, topNum):
    return hand_avg_top(hand, topNum) >= avg

def min_beat(hand, cardPlayed):
    min_beat = 13
    canBeat = False
    for card in hand:
        if(card > cardPlayed):
            canBeat = True
            break
    if(canBeat):    
        for card in hand:
            if(card > cardPlayed):
                if(card < min_beat):
                    min_beat = card
    else:
        for card in hand:
            if(card == cardPlayed):
                min_beat = card
    return min_beat

def otherFirst(msg, hand, minCard, maxCard):
    cardPlayed = msg["state"]["card"]
    cardToPlay = 0
    print("Other player's card " + str(cardPlayed))

    if ((cardPlayed > maxCard) or (cardPlayed < minCard)):
        cardToPlay = minCard
    elif (cardPlayed == maxCard):
        cardToPlay = maxCard
    else:
        cardToPlay = min_beat(hand, cardPlayed)
        
    return cardToPlay

def sample_bot(host, port):
    s = SocketLayer(host, port)

    #variable declarations
    gameId = None
    hand = [0, 0, 0, 0, 0]
    
    while True:
        msg = s.pump()
        if msg["type"] == "error":
            print("The server doesn't know your IP. It saw: " + msg["seen_host"])
            sys.exit(1)
            
        #result handling
        elif msg["type"] == "result":
            '''
            Once a player has made their move, information about the results 
            of the move will be sent to the players.
            '''
        
        #request handling
        elif msg["type"] == "request":
            if msg["state"]["game_id"] != gameId:
                gameId = msg["state"]["game_id"]
                print("New game started: " + str(gameId))

            if msg["request"] == "request_card":
                hand = msg["state"]["hand"]
                cardPlayed = 0
                cardToPlay = 0
                maxCard = max_card(hand)
                minCard = min_card(hand)
                
                
                print hand
                print ("Your tricks " + str(msg["state"]["your_tricks"]))
                print ("Their tricks " + str(msg["state"]["their_tricks"]))
                # 000000000000000000000
                if (msg["state"]["total_tricks"] == 0):

                    # Other player plays first
                    if ("card" in msg["state"]):
                        cardToPlay = otherFirst(msg, hand, minCard, maxCard)

                    # You play first
                    else:
                        #challenge if average of top 3 cards is past threshhold
                        if( desHandAvgMax(hand, 11.5, 3) and msg["state"]["can_challenge"]):
                            s.send({"type": "move", "request_id": msg["request_id"],
                                    "response": {"type": "offer_challenge"}})
                            print("Challenge issued")

                        else:
                            if(max_card(hand) < 9):
                                cardToPlay = minCard
                            else:
                                cardToPlay = maxCard
                
                # 11111111111111111111
                elif (msg["state"]["total_tricks"] == 1):

                    # Other player plays first
                    if ("card" in msg["state"]):
                        cardToPlay = otherFirst(msg, hand, minCard, maxCard)

                    # You play first
                    else:
                        #challenge if average of top 3 cards is past threshhold
                        if( desHandAvgMax(hand, 11.5, 2) and msg["state"]["can_challenge"]):
                            s.send({"type": "move", "request_id": msg["request_id"],
                                    "response": {"type": "offer_challenge"}})
                            print("Challenge issued")
                        else:
                            if(max_card(hand) < 9):
                                cardToPlay = minCard
                            else:
                                cardToPlay = maxCard

                # 22222222222222222222
                elif (msg["state"]["total_tricks"] == 2):

                    # Other player plays first
                    if ("card" in msg["state"]):
                        cardToPlay = otherFirst(msg, hand, minCard, maxCard)

                    # You play first
                    else:
                        #always challenge if three tricks won
                        if(msg["state"]["your_tricks"] == 3 and msg["state"]["can_challenge"]):
                            s.send({"type": "move", "request_id": msg["request_id"],
                                    "response": {"type": "offer_challenge"}})
                            print("Challenge issued")
                        else:
                            if(max_card(hand) < 9):
                                cardToPlay = minCard
                            else:
                                cardToPlay = maxCard

                # 33333333333333333333
                elif (msg["state"]["total_tricks"] == 3):

                    # Other player plays first
                    if ("card" in msg["state"]):
                        cardToPlay = otherFirst(msg, hand, minCard, maxCard)

                    # You play first
                    else:
                        #always challenge if three tricks won
                        if(msg["state"]["your_tricks"] == 3 and msg["state"]["can_challenge"]):
                            s.send({"type": "move", "request_id": msg["request_id"],
                                    "response": {"type": "offer_challenge"}})
                            print("Challenge issued")
                        else:
                            if(max_card(hand) < 9):
                                cardToPlay = minCard
                            else:
                                cardToPlay = maxCard
                
                # 44444444444444444444
                else:

                    # Other player plays first
                    if ("card" in msg["state"]):
                        cardToPlay = otherFirst(msg, hand, minCard, maxCard)

                    # You play first
                    else:
                        #always challenge if three tricks won
                        if(msg["state"]["your_tricks"] == 3 and msg["state"]["can_challenge"]):
                            s.send({"type": "move", "request_id": msg["request_id"],
                                    "response": {"type": "offer_challenge"}})
                            print("Challenge issued")
                        else:
                            if(max_card(hand) < 9):
                                cardToPlay = minCard
                            else:
                                cardToPlay = maxCard
                
                #end of giant if/else
                s.send({"type": "move", "request_id": msg["request_id"],
                    "response": {"type": "play_card", "card": cardToPlay}})
                    
            #they challenge
            elif msg["request"] == "challenge_offered":
                #if they have >= three tricks don't accept
                if(msg["state"]["their_tricks"] >= 3):
                    s.send({"type": "move", "request_id": msg["request_id"],
                            "response": {"type": "reject_challenge"}})
                #if our average is favorable accept
                if(desHandAvg(hand, 9)):
                    s.send({"type": "move", "request_id": msg["request_id"],
                            "response": {"type": "accept_challenge"}})
                else:
                    s.send({"type": "move", "request_id": msg["request_id"],
                            "response": {"type": "reject_challenge"}})
        
        #misc stuff                  
        elif msg["type"] == "greetings_program":
            print("Connected to the server.")
        elif msg["type"] == "game_won":
            print("Game Over: "+msg["by"]+" won")



#***end of our code*** 
def loop(player, *args):
    while True:
        try:
            player(*args)
        except KeyboardInterrupt:
            sys.exit(0)
        except Exception as e:
            print(repr(e))
        time.sleep(10)

class SocketLayer:
    def __init__(self, host, port):
        self.s = socket.socket()
        self.s.connect((host, port))

    def pump(self):
        """Gets the next message from the socket."""
        sizebytes = self.s.recv(4)
        (size,) = struct.unpack("!L", sizebytes)

        msg = []
        bytesToGet = size
        while bytesToGet > 0:
            b = self.s.recv(bytesToGet)
            bytesToGet -= len(b)
            msg.append(b)

        msg = "".join([chunk.decode('utf-8') for chunk in msg])

        return json.loads(msg)

    def send(self, obj):
        """Send a JSON message down the socket."""
        b = json.dumps(obj)
        length = struct.pack("!L", len(b))
        self.s.send(length + b.encode('utf-8'))

    def raw_send(self, data):
        self.s.send(data)

if __name__ == "__main__":
    loop(sample_bot, "cuda.contest", 19999)