#!/usr/bin/python

# This should work in both recent Python 2 and Python 3.

import socket
import json
import struct
import time
import sys

#takes in arrray up to 13 only uses 1 through 13 as values for cards that have been seen
def updatestats(showncards, hand):
    for card in hand:
        showncards[card] =  showncards[card] + 1
        
#call when a card is shown on the table

def updatestats_tablecard(showncards, tablecard):
    showncards[tablecard] = showncards[tablecard] + 1
    
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

'''
min_beat assumes that our hand contains a card 
greater than cardPlayed
'''
def min_beat(hand, cardPlayed):
    min_beat = 13
    for card in hand:
        if(card > cardPlayed):
            if(card < min_beat):
                min_beat = card
    return min_beat

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
                maxCard = max_card(hand)
                minCard = min_card(hand)
                
                # Begin 
                # 000000000000000000000
                if (msg["state"]["total_tricks"] == 0):

                    # Other player plays first
                    if ("card" in msg["state"]):
                        cardPlayed = msg["state"]["card"]
                        print("Other player's card " + str(cardPlayed))

                        if ((cardPlayed > maxCard) or (cardPlayed < minCard)):
                            cardToPlay = minCard
                        elif (cardPlayed == maxCard):
                            cardToPlay = maxCard
                        else:
                            cardToPlay = min_beat(hand, cardPlayed)

                    # You play first
                    else:
                        #challenge if average of top 3 cards is past threshhold
                        # if(msg["state"]["your_tricks"] == 3 and msg["state"]["can_challenge"]):
                            s.send({"type": "move", "request_id": msg["request_id"],
                                    "response": {"type": "offer_challenge"}})
                            break
                        else:
                            cardToPlay = minCard
                # 000000000000000000000
                #end

                
                # Begin 
                # 11111111111111111111
                elif (msg["state"]["total_tricks"] == 1):

                    # Other player plays first
                    if ("card" in msg["state"]):
                        cardPlayed = msg["state"]["card"]
                        print("Other player's card " + str(cardPlayed))

                        if ((cardPlayed > maxCard) or (cardPlayed < minCard)):
                            cardToPlay = minCard
                        elif (cardPlayed == maxCard):
                            cardToPlay = maxCard
                        else:
                            cardToPlay = min_beat(hand, cardPlayed)

                    # You play first
                    else:
                        #challenge if average of top 3 cards is past threshhold
                        if(msg["state"]["your_tricks"] == 3 and msg["state"]["can_challenge"]):
                            s.send({"type": "move", "request_id": msg["request_id"],
                                    "response": {"type": "offer_challenge"}})
                            break
                        else:
                            cardToPlay = minCard

                elif (msg["state"]["total_tricks"] == 2):

                    # Other player plays first
                    if ("card" in msg["state"]):
                        cardPlayed = msg["state"]["card"]
                        print("Other player's card " + str(cardPlayed))

                        if ((cardPlayed > maxCard) or (cardPlayed < minCard)):
                            cardToPlay = minCard
                        elif (cardPlayed == maxCard):
                            cardToPlay = maxCard
                        else:
                            cardToPlay = min_beat(hand, cardPlayed)

                    # You play first
                    else:
                        #always challenge if three tricks won
                        if(msg["state"]["your_tricks"] == 3 and msg["state"]["can_challenge"]):
                            s.send({"type": "move", "request_id": msg["request_id"],
                                    "response": {"type": "offer_challenge"}})
                            break
                        else:
                            cardToPlay = minCard

                elif (msg["state"]["total_tricks"] == 3):

                    # Other player plays first
                    if ("card" in msg["state"]):
                        cardPlayed = msg["state"]["card"]
                        print("Other player's card " + str(cardPlayed))

                        if ((cardPlayed > maxCard) or (cardPlayed < minCard)):
                            cardToPlay = minCard
                        elif (cardPlayed == maxCard):
                            cardToPlay = maxCard
                        else:
                            cardToPlay = min_beat(hand, cardPlayed)

                    # You play first
                    else:
                        #always challenge if three tricks won
                        if(msg["state"]["your_tricks"] == 3 and msg["state"]["can_challenge"]):
                            s.send({"type": "move", "request_id": msg["request_id"],
                                    "response": {"type": "offer_challenge"}})
                            break
                        else:
                            cardToPlay = minCard
                else:

                    # Other player plays first
                    if ("card" in msg["state"]):
                        cardPlayed = msg["state"]["card"]
                        print("Other player's card " + str(cardPlayed))

                        if ((cardPlayed > maxCard) or (cardPlayed < minCard)):
                            cardToPlay = minCard
                        elif (cardPlayed == maxCard):
                            cardToPlay = maxCard
                        else:
                            cardToPlay = min_beat(hand, cardPlayed)

                    # You play first
                    else:
                        #always challenge if three tricks won
                        if(msg["state"]["your_tricks"] == 3 and msg["state"]["can_challenge"]):
                            s.send({"type": "move", "request_id": msg["request_id"],
                                    "response": {"type": "offer_challenge"}})
                            break
                        else:
                            cardToPlay = minCard

                
                # if ("card" in msg["state"]):
                #     cardPlayed = msg["state"]["card"]
                #     print("Other player's card " + str(cardPlayed))
                    
                # #always challenge if three tricks won
                # if(msg["state"]["your_tricks"] == 3 and msg["state"]["can_challenge"]):
                #     s.send({"type": "move", "request_id": msg["request_id"],
                #             "response": {"type": "offer_challenge"}})
                #     break
                    
                
                # #basic card algorithm    
                # if ((cardPlayed > maxCard) or (cardPlayed < minCard)):
                #     cardToPlay = minCard
                # elif (cardPlayed == maxCard):
                #     cardToPlay = maxCard
                # else:
                #     cardToPlay = min_beat(hand, cardPlayed)
                
                
                print hand
                s.send({"type": "move", "request_id": msg["request_id"],
                    "response": {"type": "play_card", "card": cardToPlay}})
                    
            #opponent challenge handling
            elif msg["request"] == "challenge_offered":
                if(desHandAvg(hand, 9)):
                    s.send({"type": "move", "request_id": msg["request_id"],
                            "response": {"type": "accept_challenge"}})
                else:
                    s.send({"type": "move", "request_id": msg["request_id"],
                            "response": {"type": "reject_challenge"}})
                            
        elif msg["type"] == "greetings_program":
            print("Connected to the server.")
        elif msg["type"] == "game_won":
            print("Game Over: "+msg["by"]+" won")

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