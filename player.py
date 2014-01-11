#!/usr/bin/python

# This should work in both recent Python 2 and Python 3.

import socket
import json
import struct
import time
import sys


def sumHand(hand):
    total = 0
    for card in hand:
        total += card
    return total

#Returns maximum card in your hand
def findMaxCard(hand):
    maxValue = 0
    for card in hand:
        if(maxValue < card):
            maxValue = card
    return maxValue

#Returns minimum card in your hand
def findMinCard(hand):
    minValue = 13
    for card in hand:
        if(minValue > card):
            minValue = card
    return minValue

def findSecMinCard(hand):
    minValue = findMinCard(hand)
    secondMin = 0
    for card in hand:
        if (minValue < card):
            secondMin = card
    return secondMin


#Returns average value of hand
def handAvg(hand):
    total = 0
    for card in hand:
        total = total + card
    return total / len(hand)
    
#Tests hand value against a desired average
def desHandAvg(hand, avg):
    return handAvg(hand) >= avg   

#Averages top topNum cards in hand
def handAvgTop(hand, topNum):
    temp_hand = []
    for card in hand:
        temp_hand.append(card)
        
    max_hand = []
    for i in range(0, topNum):
        maxNum = findMaxCard(temp_hand)
        max_hand.append(maxNum)
        temp_hand.remove(maxNum)
        
    return handAvg(max_hand)

#Tests average of top topNum cards
def desHandAvgMax(hand, avg, topNum):
    return handAvgTop(hand, topNum) >= avg

#Finds minimum card to beat or tie the other player's card
def minBeat(hand, cardPlayed):
    minBeat = 13
    canBeat = False
    for card in hand:
        if(card > cardPlayed):
            canBeat = True
            break
    if(canBeat):    
        for card in hand:
            if(card > cardPlayed):
                if(card < minBeat):
                    minBeat = card
    else:
        for card in hand:
            if(card == cardPlayed):
                minBeat = card
    return minBeat


#Function that handles when the other person goes first
def otherFirst(msg, hand, minCard, maxCard):
    cardPlayed = msg["state"]["card"]
    cardToPlay = 0
    print("Other player's card " + str(cardPlayed))
    logFile.write("Other player's card " + str(cardPlayed) + "\n")

    if (msg["state"]["total_tricks"] == 0 and desHandAvgMax(hand, challengeThreshhold, 3) 
                                          and msg["state"]["can_challenge"]):
            cardToPlay = -1
    elif (msg["state"]["total_tricks"] == 1 and desHandAvgMax(hand, challengeThreshhold, 2) 
                                            and msg["state"]["can_challenge"]):
            cardToPlay = -1
    elif (msg["state"]["total_tricks"] == 4 and msg["state"]["their_tricks"] <= 1 and 
        msg["state"]["your_tricks"] > 2 and msg["state"]["can_challenge"]):
        cardToPlay = -1
    elif (msg["state"]["your_tricks"] >= 3 and msg["state"]["can_challenge"]):
        cardToPlay = -1
    elif ((cardPlayed > maxCard) or (cardPlayed < minCard)):
        cardToPlay = minCard
    elif (cardPlayed == maxCard):
        cardToPlay = maxCard
    else:
        cardToPlay = minBeat(hand, cardPlayed)
        
    return cardToPlay

'''
leads with the lowest card of 6,7, or 8 (if exists)
otherwise returns findMinCard(hand)
'''
def chooseLead(hand):
    return findMinCard(hand)
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
        return findMinCard(hand)
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
            logFile.write("Result object\n")
            logFile.write(str(msg["result"]) + "\n")
            if (msg["result"] == "trick_won"):
                logFile.write("trick won\n")
                # logFile.write("Winning Card is " + msg["trick_won"]["card"]+ "\n")
                # if (msg["result"]["your_player_num"] == msg["result"]["trick_won"]["by"]):
                #     logFile.write("You Win\n")
                #     #if (msg["state"]["in_challenge"])
                #     #    challengeGamesWon = challengeGamesWon + 1
                # else:
                #     logFile.write("You Lose\n")
                #     #if (msg["state"]["in_challenge"])
                #      #   challengeGamesLost = challengeGamesLost + 1
        #request handling
        elif msg["type"] == "request":
            if msg["state"]["game_id"] != gameId:
                gameId = msg["state"]["game_id"]
                print("New game started: " + str(gameId))
###############################################################################
#
# FSM OF DOOOOOM
#
###############################################################################
            if msg["request"] == "request_card":
                logFile.write("=====\n")
                hand = msg["state"]["hand"]
                cardToPlay = 0
                global challengeThreshhold
                challengeThreshhold = 10
                maxCard = findMaxCard(hand)
                minCard = findMinCard(hand)
                
                
                print hand
                print ("Your tricks " + str(msg["state"]["your_tricks"]))
                print ("Their tricks " + str(msg["state"]["their_tricks"]))
                # 000000000000000000000
                #handsPlayed = handsPlayed + 1
                if (msg["state"]["total_tricks"] == 0):
                    logFile.write(str(hand) + "\n")
                    logFile.write("Average of hand : " + str(sumHand(hand)/5) + "\n")

                    # Other player plays first
                    if (msg["state"]["their_points"] == 9 and msg["state"]["can_challenge"]):
                        cardToPlay = -1
                    elif ("card" in msg["state"]):
                        cardToPlay = otherFirst(msg, hand, minCard, maxCard)

                    # You play first
                    else:
                        #challenge if average of top 3 cards is past threshhold
                        if(desHandAvgMax(hand, challengeThreshhold, 3) and msg["state"]["can_challenge"]):
                            cardToPlay = -1
                        else:
                            cardToPlay = findSecMinCard(hand)
                
                # 11111111111111111111
                elif (msg["state"]["total_tricks"] == 1):

                    # Other player plays first
                    if ("card" in msg["state"]):
                        cardToPlay = otherFirst(msg, hand, minCard, maxCard)

                    # You play first
                    else:
                        #challenge if average of top 2 cards is past threshhold
                        if(msg["state"]["your_points"] == 1 and desHandAvgMax(hand, challengeThreshhold, 2) and msg["state"]["can_challenge"]):
                            cardToPlay = -1
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
                            cardToPlay = -1
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
                        if(msg["state"]["your_tricks"] >= 3 and msg["state"]["can_challenge"]):
                            cardToPlay = -1
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
                        if(msg["state"]["your_tricks"] >= 3 and msg["state"]["can_challenge"]):
                            cardToPlay = -1
                        elif(msg["state"]["your_tricks"] == 2 and msg["state"]["their_tricks"] <= 1 and msg["state"]["can_challenge"]):
                            cardToPlay = -1
                        else:
                            cardToPlay = chooseLead(hand)
                
                #end of giant if/else, send our response
                if (cardToPlay == -1):
                    s.send({"type": "move", "request_id": msg["request_id"],
                            "response": {"type": "offer_challenge"}})
                    print("Challenge issued")
                    logFile.write("Challenge Issued\n")
                else:
                    s.send({"type": "move", "request_id": msg["request_id"],
                            "response": {"type": "play_card", "card": cardToPlay}})
                    logFile.write('Card played ' + str(cardToPlay) + '\n')
                    

###############################################################################
#
# Challenge analyzation
#
###############################################################################
            elif msg["request"] == "challenge_offered":
                logFile.write('Challenge offered by other player\n')
                rejectChallenge = True
                #if they have >= three tricks don't accept
                if(msg["state"]["their_tricks"] >= 3):
                    rejectChallenge = True
                #if our hand average favorable or they're leading by 7
                elif(desHandAvg(hand, challengeThreshhold) 
                     or (msg["state"]["their_points"] >= (msg["state"]["your_points"] + 7))):
                        rejectChallenge = False
                elif(msg["state"]["their_points"] == 9):
                    rejectChallenge = False
                elif(msg["state"]["your_points"] == 9 and msg["state"]["their_points"] >= 5):
                    rejectChallenge = False
                else:
                    rejectChallenge = True
                
                #send challenge response
                if (rejectChallenge == True):
                    s.send({"type": "move", "request_id": msg["request_id"],
                            "response": {"type": "reject_challenge"}})
                else:
                    s.send({"type": "move", "request_id": msg["request_id"],
                            "response": {"type": "accept_challenge"}})
                    
                

        
        #misc stuff                  
        elif msg["type"] == "greetings_program":
            print("Connected to the server.")
        elif msg["type"] == "game_won":
            #games = games + 1
            #avghands = hands /games
            #if msg["state"][in_challenge] and (msg["by"] == 
                
            print("Game Over: "+msg["by"]+" won")
            logFile.write("Game Over: " + msg["by"] + " won")
            gamesPlayed += 1
            logFile.write("Games played: " + str(gamesPlayed))
        #if games%300 == 0:
            #print("The Average Hands per game is: " + avghands)
            #print()
        





def loop(player, *args):
    # Opens one logfile
    currTime = time.strftime("%I_%M_%S")
    logFileName = "log_" + currTime + ".log"
    global logFile
    logFile = open(logFileName, 'w')

    statFileName = "stat_" + currTime + ".log"
    global statFile
    # statFile = open(statFileName, 'w')
    
    #Gametracker
    '''global gamesPlayed
    global handsPlayed
    global challengeGamesWon
    global challengeGamesLost
    challengeGamesLost = 0
    challengeGamesWon = 0
    handsPlayed = 0
    gamesPlayed = 0
    gameThreshhold = 20'''
    
    #while (games < gameThreshhold):
    while True:
        try:
            player(*args)
        except KeyboardInterrupt:
            sys.exit(0)
        except Exception as e:
            print(repr(e))
        time.sleep(10)
    print("End of %d games", gameThreshhold)
        
###############################################################################
#
# END OF TREY BURKE
#
###############################################################################

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