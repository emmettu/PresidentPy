#!/usr/bin/env python3
#Emmett Underhill
#August 2014

#President.py
#Command Line president card game

import random
import sys
import time
import os

class PresidentGame:
	#Const variables
	NUM_HUMANS = 0
	NUM_COMPS = 0
	TOTAL_PLAYERS = 0
	NUM_DECKS = 0
	
	deck = []
	hands = []
	pile = ["Empty"]

	
	passed = []
	round_starter = 0

	ranks = []
	humans = []
	
	values = {"Empty":-1, "3":0, "4":1, "5":2, "6":3, "7":4, "8":5, \
	          "9":6, "10":7, "J":8, "Q":9, "K":10, "A":11, "2":12}
	
	names = []

	def __init__(self):
		if(len(sys.argv) != 4):
			print("Usage: ./President.py x y z")
			print("x = num humans, y = num comps, z = num decks")
			sys.exit()

		self.NUM_HUMANS = int(sys.argv[1])
		self.NUM_COMPS = int(sys.argv[2])
		self.NUM_DECKS = int(sys.argv[3])
		self.TOTAL_PLAYERS = self.NUM_HUMANS + self.NUM_COMPS
		self.makeDeck()
		self.hands = \
		[[] for _ in range(self.NUM_HUMANS + self.NUM_COMPS)]
		self.passed = [False] * self.TOTAL_PLAYERS
		
		#Names:
		self.names = ["HAL"+str(i*1000) for i in range(self.TOTAL_PLAYERS)]
		
		#Humans to keep track of who's human and who's comp
		self.humans = [False]*self.TOTAL_PLAYERS
		indexes = list(range(self.TOTAL_PLAYERS))
		random.shuffle(indexes)
		for i in range(self.NUM_HUMANS):
			self.humans[indexes[i]] = True	
			self.names[indexes[i]] = input("What's you're name player "+str(indexes[i])+"?: ")

	def makeDeck(self):
		for i in range(2,11):	
			self.deck.extend([str(i)]*4*self.NUM_DECKS)
		self.deck.extend(("J")*4*self.NUM_DECKS)
		self.deck.extend(["Q"]*4*self.NUM_DECKS)
		self.deck.extend(["K"]*4*self.NUM_DECKS)
		self.deck.extend(["A"]*4*self.NUM_DECKS)
		self.pile = ["Empty"]

	def deal(self):
		self.hands = \
		[[] for _ in range(self.NUM_HUMANS + self.NUM_COMPS)]
		for i in range(len(self.deck)):
			self.hands[i%self.TOTAL_PLAYERS].append(self.deck[i])

	def humanTurn(self, i):
		#To stop other players from peaking
		if self.NUM_HUMANS > 1:
			input("Press any key "+self.names[i]+": ")
			print()
		self.hands[i].sort(key=self.values.get)
		print(self.names[i]+"\'s turn")
		print()
		for j in range(len(self.hands)):
			print(self.names[j]+":", len(self.hands[j]), "cards")
		#print("Your hand:")
		self.printHand("Your hand:" ,self.hands[i])	
		self.printHand("Current card:",self.pile[-1])
		#print("Current card:", self.pile[-1])
		card = input("Select which card to put down (P to pass): ")
		card = card.split()
		if(card == ["P"]):
			self.passed[i] = True
		elif(self.hands[i] == []):
			pass
		elif self.isValid(card, i):
			self.putDown(card, i)
		else:
			print()
			self.humanTurn(i)
		
		if(self.hands[i] == []):
			self.ranks.append(i)

		os.system('cls' if os.name == 'nt' else 'clear')

	def robotTurn(self, i):
		cards = []
		#If it's a new pile
		self.hands[i].sort(key=self.values.get)
		if self.pile[-1] == "Empty":
			#play lowest card
			for j in range(self.hands[i].count(self.hands[i][0])):
				cards.append(self.hands[i][0])
			self.putDown(cards, i)

			if self.hands[i] == []:
				self.ranks.append(i)
			return
		for j in self.hands[i]:
			if self.values[j] > self.values[self.pile[-1][0]] and \
			self.hands[i].count(j) == len(self.pile[-1]):
				for x in range(self.hands[i].count(j)):
					cards.append(j)
				self.putDown(cards, i)

				if self.hands[i] == []:
					self.ranks.append(i)
				return
		self.passed[i] = True

	def playRound(self):
		i = self.round_starter
		while(self.passed.count(False) > 1):
			if(self.hands[i%self.TOTAL_PLAYERS] == []):
				self.passed[i%self.TOTAL_PLAYERS] = True
			if(self.passed[i%self.TOTAL_PLAYERS] == False):
				if self.humans[i%self.TOTAL_PLAYERS]:
					self.humanTurn(i%self.TOTAL_PLAYERS)
				else:
					self.robotTurn(i%self.TOTAL_PLAYERS)
			i += 1
		winner = self.passed.index(False)
		print("Winner =", self.names[winner])
		self.round_starter = winner
	
	def playMatch(self):
		#if no ranks are in place just have 1st player go
		if self.ranks == []:
			self.round_starter = 0

		#else scum starts round
		else:
			self.round_starter = self.ranks[-1]
		#Reset ranks
		self.ranks = []
		while len(self.ranks) < self.TOTAL_PLAYERS: 
			self.pile = ["Empty"]
			self.passed = [False] * self.TOTAL_PLAYERS
			self.playRound()

	def printRanks(self, depth=0):
		if len(self.ranks) == 1:
			print(self.names[self.ranks[0]], "is neutral")
			return
		if self.ranks == []:
			return
		print(self.names[self.ranks[0]], "is", "vice "*(depth) + "president")
		print(self.names[self.ranks[-1]], "is", "vice "*(depth) + "scum")
		self.swapCards(self.ranks[0], self.ranks[-1], depth)
		del self.ranks[-1]
		del self.ranks[0]
		self.printRanks(depth+1)

	def swapCards(self, president, scum, depth):
		amount = self.TOTAL_PLAYERS//2-depth
		print(self.names[scum],"gives his",amount,"best cards to",self.names[president])
		self.hands[scum].sort(key=self.values.get)
	#	print("gives away: ", self.hands[scum][-amount:])
		self.hands[president].extend(self.hands[scum][-amount:])
		del self.hands[scum][-amount:]

		print(self.names[president],"gives",amount,"cards to",self.names[scum])
		print()
		if self.humans[president]:
			self.humanSwapPick(president, scum, amount)
		else:
			self.roboSwapPick(president, scum, amount)
			#robo swap pick
	
	def humanSwapPick(self, president, scum, amount):
		#To stop people from peaking
		if self.NUM_HUMANS > 1:
			input(self.names[president]+" press any key to continue: ")
		self.hands[president].sort(key=self.values.get)
		#print(self.hands[president])
		self.printHand("Your hand:",self.hands[president])
		cards = input("Pick "+str(amount)+" cards to give "+self.names[scum]+": ").split()
		for i in cards:
			if i not in self.hands[president]:
				print("Invalid pick")
				self.humanSwapPick(president, scum, amount)
				return
			else:
				self.hands[president].remove(i)
				self.hands[scum].extend(i)
				amount -= 1
		if amount > 0:
			self.humanSwapPick(president, scum, amount)
			return
		os.system('cls' if os.name == 'nt' else 'clear')

	def roboSwapPick(self, president, scum, amount):
		self.hands[president].sort(key=self.values.get)
		self.hands[scum].extend(self.hands[president][:amount])
	#	print("giving away: ", self.hands[president][:amount])
		del self.hands[president][:amount]
		

	def main(self):	
		print("Game Start!")
		random.shuffle(self.deck)
		self.deal()
		self.playMatch()
		random.shuffle(self.deck)
		self.deal()
		self.printRanks()
		while True:
			self.playMatch()
			print(self.ranks)
			print(self.hands)
			random.shuffle(self.deck)
			self.deal()
			self.printRanks()

	def isValid(self, card, i):
		if(card == []):
			print("Select at least one card")
			return False
		#Check if all same card
		for j in card:
			if j != card[0]:
				print("Cards must match")
				return False
		#Check if have them all
		if self.hands[i].count(card[0]) < len(card):
			print("Don't have that card")
			return False
		#If the pile is empty, then you're good to go
		if self.pile[-1] == 'Empty':
			return True
		#Check if value of card is higher
		if self.values[card[0]] <= self.values[self.pile[-1][0]]:
			print("Value not higher")
			return False
		#Edge case, 2's trump lesser pile
		if card[0] == '2' and len(card) >= len(self.pile[-1]) - 1:
			return True
		#Check if same number of cards as pile
		if len(card) != len(self.pile[-1]):
			print("Not same number as pile")
			return False
		return True

	def putDown(self, card, i):
		for j in card:
			self.hands[i].remove(j)
		self.pile.append(card)
	
	def printHand(self, phrase, cards):
		print(phrase, end=' ')
		for i in cards:
			if i == 'E':
				print('Empty', end = ' ')
				break
			if i == 'A':
				print('\033[91m'+i+'\033[0m', end=' ')
			elif i == '2':
				print('\033[94m'+i+'\033[0m', end=' ')
			elif i in 'KQJ':
				print('\033[93m'+i+'\033[0m', end=' ')
			else:
				print('\033[92m'+i+'\033[0m', end=' ')
		print()
if __name__ == '__main__':
	Game = PresidentGame()
	Game.main()
