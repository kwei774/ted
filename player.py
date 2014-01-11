#!/usr/bin/python

# This should work in both recent Python 2 and Python 3.

import socket
import json
import struct
import time
import sys

#Returns maximum card in your hand
def max_card(hand):
    max_value = 0
    for card in hand:
        if(max_value < card):
            max_value = card
    return max_value        

#Returns minimum card in your hand
def min_card(hand):
    min_value = 13
    for card in hand:
        if(min_value > card):
            min_value = card
    return min_value

#Returns average value of hand
def hand_avg(hand):
    total = 0
    for card in hand:
        total = total + card
    return total / len(hand)
    
#Tests hand value against a desired average
def desHandAvg(hand, avg):
    return hand_avg(hand) >= avg   

#Averages top topNum cards in hand
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

#Tests average of top topNum cards
def desHandAvgMax(hand, avg, topNum):
    return hand_avg_top(hand, topNum) >= avg

#Finds minimum card to beat or tie the other player's card
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


#FIX S FIX S FIX S MAKE IT IN SCOPE
#Function that handles when the other person goes first
def otherFirst(msg, hand, minCard, maxCard):
    cardPlayed = msg["state"]["card"]
    cardToPlay = 0
    print("Other player's card " + str(cardPlayed))

    if (msg["state"]["total_tricks"] == 0):
        if (desHandAvgMax(hand, 11, 3) and msg["state"]["can_challenge"]):
            s.send({"type": "move", "request_id": msg["request_id"], "response": {"type": "offer_challenge"}})
    elif (msg["state"]["total_tricks"] == 1):
        if (desHandAvgMax(hand, 11, 2) and msg["state"]["can_challenge"]):
            s.send({"type": "move", "request_id": msg["request_id"], "response": {"type": "offer_challenge"}})
    elif (msg["state"]["your_tricks"] > 3 and msg["state"]["can_challenge"]):
        s.send({"type": "move", "request_id": msg["request_id"], "response": {"type": "offer_challenge"}})         
    elif ((cardPlayed > maxCard) or (cardPlayed < minCard)):
        cardToPlay = minCard
    elif (cardPlayed == maxCard):
        cardToPlay = maxCard
    else:
        cardToPlay = min_beat(hand, cardPlayed)
        
    return cardToPlay

'''
leads with the lowest card of 6,7, or 8 (if exists)
otherwise returns min_card(hand)
'''
def chooseLead(hand):
    return min_card(hand)
'''
    lead = 0;
    for card in hand:
        if(card == 6):
            return card
        elif(card == 7):
            lead = card
        elif(card == 8 and lead != 7):
            lead = card
    if(lead == 0):
        return min_card(hand)
    else:
        return lead 
'''
        

def sample_bot(host, port):
    s = SocketLayer(host, port)

    #variable declarations
    gameId = None
    hand = [0, 0, 0, 0, 0]
    game_number = 0
    
    while True:
        #games = 0
        #hands = 0
        #avghands = 0
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
                #hands = hands + 1
                if (msg["state"]["total_tricks"] == 0):

                    # Other player plays first
                    if ("card" in msg["state"]):
                        cardToPlay = otherFirst(msg, hand, minCard, maxCard)

                    # You play first
                    else:
                        #challenge if average of top 3 cards is past threshhold
                        if( desHandAvgMax(hand, 11, 3) and msg["state"]["can_challenge"]):
                            s.send({"type": "move", "request_id": msg["request_id"],
                                    "response": {"type": "offer_challenge"}})
                            print("Challenge issued")

                        else:
                            cardToPlay = chooseLead(hand)
                
                # 11111111111111111111
                elif (msg["state"]["total_tricks"] == 1):

                    # Other player plays first
                    if ("card" in msg["state"]):
                        cardToPlay = otherFirst(msg, hand, minCard, maxCard)

                    # You play first
                    else:
                        #challenge if average of top 3 cards is past threshhold
                        if( desHandAvgMax(hand, 11, 2) and msg["state"]["can_challenge"]):
                            s.send({"type": "move", "request_id": msg["request_id"],
                                    "response": {"type": "offer_challenge"}})
                            print("Challenge issued")
                        else:
                            cardToPlay = chooseLead(hand)

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
                            cardToPlay = chooseLead(hand)

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
                            cardToPlay = chooseLead(hand)
                
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
                            cardToPlay = chooseLead(hand)
                
                #end of giant if/else, send our response
                s.send({"type": "move", "request_id": msg["request_id"],
                    "response": {"type": "play_card", "card": cardToPlay}})
                    
            #they challenge
            elif msg["request"] == "challenge_offered":
                #if they have >= three tricks don't accept
                if(msg["state"]["their_tricks"] >= 3):
                    s.send({"type": "move", "request_id": msg["request_id"],
                            "response": {"type": "reject_challenge"}})
                #if our average is favorable accept
                if(desHandAvg(hand, 10) or (msg["state"]["their_points"] > (msg["state"]["your_points"] + 5))):
                    s.send({"type": "move", "request_id": msg["request_id"],
                            "response": {"type": "accept_challenge"}})
                else:
                    s.send({"type": "move", "request_id": msg["request_id"],
                            "response": {"type": "reject_challenge"}})
        
        #misc stuff                  
        elif msg["type"] == "greetings_program":
            print("Connected to the server.")
        elif msg["type"] == "game_won":
            #games = games + 1
            #avghands = hands /games
            #if msg["state"][in_challenge] and (msg["by"] == 
                
            print("Game Over: "+msg["by"]+" won")
        #if games%300 == 0:
            #print("The Average Hands per game is: " + avghands)
            #print()



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
    loop(sample_bot, "cuda.contest", 9999)