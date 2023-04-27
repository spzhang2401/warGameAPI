from copy import *
import random

orderedDeck = []
for i in range(4): # for each suit: spades, clubs, diamonds, hearts
    for j in range(2, 15): # for each card, ranging from 2 through 14. 
        # 11 = Jack; 12 = Queen; 13 = King; 14 = Ace
        orderedDeck.append(j)

class Underdog:
    def __init__ (self, playerA, playerB):
        # can input player's names:
        self.playerA = playerA
        self.playerB = playerB

        self.gameWon = False
        self.winner = None

        # shuffle the original deck and split between players:
        playDeck = orderedDeck.copy()
        random.shuffle(playDeck)
        self.playingDeck = playDeck

        self.aCards = self.playingDeck[:26]
        self.bCards = self.playingDeck[26:]

        self.turnCount = 0
    
    # run the whole game
    def play (self):
        while (not self.gameWon):
            self.playTurn()
        return self.winner

    # run one turn of the game
    def playTurn (self):
        
        def drawTop(deck): # lift top card of a player's deck.
            return deck.pop(0)
        
        # counter used to cut off infinite games
        self.turnCount += 1
        if (self.turnCount == 10000):
            self.gameWon = True
            if (len(self.aCards) > len(self.bCards)):
                self.winner = self.playerA
            else:
                self.winner = self.playerB
            return self.winner

        cardA = drawTop(self.aCards)
        cardB = drawTop(self.bCards)

        soldiers = [] # initialize the war card pile
        underdogA = False
        underdogB = False

        if (cardA > cardB):
            self.aCards.append(cardA)
            self.aCards.append(cardB)

        elif (cardA < cardB):
            self.bCards.append(cardB)
            self.bCards.append(cardA)

        else: # values are equal, war ensues
            soldiers.append(cardA)
            soldiers.append(cardB)

            # War repeats if the next upturned cards are also the same.
            while ( (cardA == cardB) and 
                    (len(self.aCards) >= 2) and
                    (len(self.bCards) >= 2) and
                    not self.gameWon) :

                # Face-down or upturned, we add all of these cards into the "soldiers" pile.
                udA = drawTop(self.aCards)
                if (udA == 11): # if a downturned card is a Jack, the player who it belonged to becomes an underdog.
                    underdogA = True
                soldiers.append(udA)
                cardA = drawTop(self.aCards)
                soldiers.append(cardA)

                udB = drawTop(self.aCards)
                if (udB == 11):
                    underdogB = True
                soldiers.append(udB)
                soldiers.append(drawTop(self.bCards))
                cardB = drawTop(self.bCards)
                soldiers.append(cardB)

            random.shuffle(soldiers) # assists with avoiding the infinite game problem.

            if (cardA == cardB): # Outside of the loop. One player necessarily has insufficient cards.
                if (len(self.aCards) < 2):
                    self.bCards.extend(soldiers)
                    self.winner = self.playerB
                else:
                    self.aCards.extend(soldiers)
                    self.winner = self.playerA
                self.gameWon = True
            
            # add all of the soldier cards into the winner's deck.
            # swap who gets the cards if the losing player is an underdog.
            elif (cardA > cardB):
                if underdogB:
                    self.bCards.extend(soldiers)
                else:
                    self.aCards.extend(soldiers)
            else:
                if underdogA:
                    self.aCards.extend(soldiers)
                else:
                    self.bCards.extend(soldiers)
        
        # Final checks if someone won:
        if (not self.aCards or not self.bCards):
            if (not self.aCards):
                self.winner = self.playerB
            else:
                self.winner = self.playerA
            self.gameWon = True

        return self.winner