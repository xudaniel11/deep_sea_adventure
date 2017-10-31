from deepsea_player import Player
from deepsea_ai import AI
from deepsea_treasure import Treasure
from deepsea_treasure import TreasureStack

import random
import time
import json

import sys

"""
Rules: https://tesera.ru/images/items/1058647/deep-sea-adventure-rulesf.pdf
"""

class Board:
	def __init__(self, numberPlayers, testEventFile=""):
		self.players = self.initPlayers(numberPlayers)
		self.air = 25
		self.treasureMap = self.initTreasureMap()
		self.numRounds = 3
		self.AI = AI()
		self.testEventFile = testEventFile
		self.testEventStream = self.parseTestEventFile(testEventFile)
		self.expectedValueTreasureDict = {
			0: 0,
			1: 1.5,
			2: 5.5,
			3: 9.5,
			4: 13.5
		}

	def testCompare(self, other): 
		return self.__dict__ == other.__dict__

	def parseTestEventFile(self, testEventFile):
		eventStream = []

		if testEventFile == "":
			return eventStream

		with open(testEventFile, 'rb') as inputFile:
			eventStream = inputFile.read().split("\n")

		return eventStream

	def initPlayers(self, numberPlayers):
		playerList = []
		for i in range(numberPlayers):
			playerList.append(Player(i, self))

		return playerList

	def initTreasureMap(self, treasureMapList=""):
		if treasureMapList != "":
			outputTreasureMap = []
			for treasureDict in treasureMapList:
				outputTreasureMap.append(Treasure(int(treasureDict["numDots"]), int(treasureDict["value"])))
			return outputTreasureMap

		oneDotTreasureList = [0,0,1,1,2,2,3,3]
		twoDotTreasureList = [4,4,5,5,6,6,7,7]
		threeDotTreasureList = [8,8,9,9,10,10,11,11]
		fourDotTreasureList = [12,12,13,13,14,14,15,15]

		map(random.shuffle, [oneDotTreasureList, twoDotTreasureList, threeDotTreasureList, fourDotTreasureList])

		joinedTreasureMap = oneDotTreasureList + twoDotTreasureList + threeDotTreasureList + fourDotTreasureList
		outputTreasureMap = []

		count = 0
		for value in joinedTreasureMap:
			outputTreasureMap.append(Treasure(count / 8 + 1, value))
			count += 1

		return outputTreasureMap

	def getTreasureExpectedValue(self, treasure):
		numDots = treasure.getNumDots()

		totalValueDotTreasure = self.expectedValueTreasureDict[numDots] * 8
		numRevealedTreasure = 0
		for player in self.players:
			for currentTreasure in player.getRevealedTreasure():
				if treasure.getNumDots() == numDots:
					totalValueDotTreasure -= treasure.getValue()
					numRevealedTreasure += 1

		expectedValue = totalValueDotTreasure * 1.0 / (8 - numRevealedTreasure)
		return expectedValue

	def getRemainingAir(self):
		return self.air

	def getNumberBlankChips(self):
		numBlank = 0
		for treasure in self.treasureMap:
			if treasure.numDots() == 0:
				numBlank += 1

		return numBlank

	def getTreasureMap(self):
		return self.treasureMap

	def getNumberTreasureChips(self):
		return len(self.treasureMap) - self.getNumberBlankChips()

	def getAllPlayerLocations(self):
		playerLocations = {}
		for player in self.players:
			playerLocations[player.getID()] = player.getLocation()

		return playerLocations

	"""
	1,1 = 2
	1,2 = 3
	2,1 = 3
	2,2 = 4
	3,1 = 4
	1,3 = 4
	2,3 = 5
	3,2 = 5
	3,3 = 6

	4 possibilities for each unique tuple, for a total of 36 possibilites

	Expected Roll = 4
	Min Roll = 2
	Max Roll = 6
	Roll STDEV = 1.1547
	"""
	def rollDice(self, roll=""):
		if roll != "":
			return int(roll)
		return random.sample([2,3,3,4,4,4,5,5,6], 1)[0]

	def allPlayersEscaped(self):
		for player in self.players:
			if player.hasEscaped() == False:
				return False

		return True

	def getPlayersPointDistribution(self):
		playerPointDict = {}
		for player in self.players:
			playerPoints = 0

			for treasure in player.getRevealedTreasure():
				playerPoints += treasure.getValue()

			playerPointDict[player.getID()] = playerPoints

		return playerPointDict

	def movePlayer(self, currentPlayer, direction, numMoves):
		print "NUM MOVES: %s" % numMoves
		if direction == "UP":
			playerLocations = self.getAllPlayerLocations()
			desiredLocation = currentPlayer.getLocation() - numMoves

			numberJumps = 0
			for playerLocation in sorted(playerLocations.values(), reverse=True):
				if playerLocation != currentPlayer.getLocation():
					if (currentPlayer.getLocation() > playerLocation) and (playerLocation >= desiredLocation):
						desiredLocation -= 1
						numberJumps += 1
			print "NUM JUMPS: %s" % numberJumps

			if desiredLocation < 0:
				currentPlayer.escape()
				print "PLAYER ESCAPE: %s" % currentPlayer.getID()
			else:
				currentPlayer.setLocation(desiredLocation)

		else:
			print "MOVING DOWN"
			playerLocations = self.getAllPlayerLocations()
			desiredLocation = currentPlayer.getLocation() + numMoves

			print "DESIRED LOCATION: %s" % desiredLocation

			numberJumps = 0
			for playerLocation in sorted(playerLocations.values()):
				if playerLocation != currentPlayer.getLocation():
					if (currentPlayer.getLocation() < playerLocation) and (playerLocation <= desiredLocation):
						desiredLocation += 1
						numberJumps += 1
			print "NUM JUMPS: %s" % numberJumps

			if desiredLocation >= len(self.treasureMap):
				desiredLocation = len(self.treasureMap) - 1

				while True:
					if desiredLocation in playerLocations.values():
						desiredLocation -= 1
					else:
						break
			
			print "FINAL DESIRED LOCATION: %s" % desiredLocation

			currentPlayer.setLocation(desiredLocation)


	def clearTreasureMapBlankChips(self):
		self.treasureMap = filter(lambda x: x.getNumDots() != 0, self.treasureMap)

	def endRound(self, playerIndex):
		self.clearTreasureMapBlankChips()
		self.air = 25

		# If everyone got out, the most recent player to get out is the one who will go first next round
		if self.allPlayersEscaped():
			playerIndex = (playerIndex - 1) % len(self.players)

		# If players did not all get out, then the deepest player is the one who will go first next round. 
		# All players who do not get out drown
		else:
			stackDepthDict = {}
			deepestPlayerID = None
			deepestLocation = 0
			
			for player in self.players:
				if player.hasEscaped() == False:
					playerLocation = player.getLocation()
					playerID = player.getID()
					if deepestLocation < playerLocation:
						deepestPlayerID = playerID

					# Need to figure out how to drown the player with a specific dropped treasure stack
					print "PLAYER DROWN: %s" % player.getID()
					droppedTreasureStacks = player.drown()
					
					stackDepthDict[playerLocation] = droppedTreasureStacks

			for depth in sorted(stackDepthDict.keys()):
				droppedTreasureStacks = stackDepthDict[depth]
				print "PLAYER DROWN DEPTH + STACK: %s, %s" % (depth,droppedTreasureStacks)
				self.treasureMap += droppedTreasureStacks

		for player in self.players:
			player.resetRound()

		return playerIndex

	"""
	Does not handle players picking up TreasureStacks in the test_moves file yet
	"""
	def checkCurrentStatus(self, checkStatusEvent):
		checkStatusEventDict = json.loads(checkStatusEvent)
		playersDict = checkStatusEventDict['players']
		treasureMapDict = checkStatusEventDict['board']['treasureMap']
		air = int(checkStatusEventDict['board']['air'])

		checksPassed = True

		if air != self.air:
			print "ERROR AIR COUNT DOES NOT MATCH"
			print "EXPECTED %s" % air
			print "GOT %s" % self.air
			print "\n\n"

			checksPassed = False

		testTreasureMap = []
		for treasureDict in treasureMapDict:
			testTreasure = Treasure(treasureDict['numDots'], treasureDict['value'])
			testTreasureMap.append(testTreasure)

		testTreasureIndex = 0
		for testTreasure in testTreasureMap:
			if testTreasure.testCompare(self.treasureMap[testTreasureIndex]):
				print "ERROR TREASURE_MAP DOES NOT MATCH"
				print "EXPECTED %s" % testTreasureMap
				print "GOT %s" % self.treasureMap
				print "\n\n"

				checksPassed = False
				break

			testTreasureIndex += 1

		for testPlayerDict in playersDict:
			testPlayerID = int(testPlayerDict['id'])
			testPlayer = Player(testPlayerID, self)
			testPlayer.setLocation(int(testPlayerDict['location']))
			testPlayer.diving = eval(testPlayerDict['diving'])
			#print testPlayer.diving, testPlayerDict['diving']
			testPlayer.hasEscaped = bool(testPlayerDict['hasEscaped'])

			for treasureDict in testPlayerDict['unrevealed_treasure']:
				testTreasure = Treasure(treasureDict['numDots'], treasureDict['value'])
				testPlayer.pickUpTreasure(testTreasure)

			for treasureDict in testPlayerDict['revealed_treasure']:
				testTreasure = Treasure(treasureDict['numDots'], treasureDict['value'])
				testPlayer.revealed_treasure.append(testTreasure)


			if testPlayer.testCompare(self.players[testPlayerID]) == False:
				print "ERROR PlAYER DOES NOT MATCH"
				print "EXPECTED %s" % testPlayer
				print "GOT %s" % self.players[testPlayerID]
				print "\n\n"

				checksPassed = False

		if checksPassed == False:
			print "\n\n\n----------TEST SYSTEM CHECKS FAILED----------\n\n\n"
			time.sleep(200)
		else:
			print "\n\n\n----------TEST SYSTEM CHECKS PASSED----------\n\n\n"

		return checksPassed

	def parseInitializeEvent(self):
		print "INSTANTIATING TEST BOARD"

		initializeEvent = self.testEventStream.pop(0)
		currentEventDict = json.loads(initializeEvent)

		if currentEventDict["eventtype"] != "INSTANTIATE_BOARD":
			print "ERROR INITIALIZING BOARD"

		self.players = self.initPlayers(int(currentEventDict["numPlayers"]))
		self.treasureMap = self.initTreasureMap(currentEventDict["treasureMap"])

	def parseSystemEvent(self, systemEventString):
		if len(self.testEventStream) == 0:
			return

		currentEvent = self.testEventStream.pop(0)
		print "CURRENT EVENT: %s" % currentEvent

		if systemEventString not in currentEvent:
			print "\n\n\nERROR UNEXPECTED EVENT: EXPECTED %s EVENT\n\n\n" % systemEventString

		if systemEventString == "CHECK_STATUS":
			self.checkCurrentStatus(currentEvent)

	def parseGameEvent(self):
		currentEventDict = {
			"direction": "",
			"action": "",
			"roll": ""
		}

		if len(self.testEventStream) > 0:
			currentEvent = self.testEventStream.pop(0)

			print currentEvent
			if "PLAYER" in currentEvent:
				currentEventDict = json.loads(currentEvent)
			else:
				print "\n\n\nERROR UNEXPECTED EVENT: EXPECTED PLAYER EVENT\n\n\n"

		return currentEventDict


	def play(self):
		playerIndex = 0

		if self.testEventStream != None and self.testEventStream:
			self.parseInitializeEvent()

		for roundNumber in range(self.numRounds):
			print 'STARTING ROUND: %s \n\n\n' % roundNumber

			self.parseSystemEvent("START_ROUND")

			while (self.air >= 0) and (self.allPlayersEscaped() == False):
				currentPlayer = self.players[playerIndex]
				playerIndex = (playerIndex + 1) % len(self.players)

				currentEventDict = self.parseGameEvent()

				#If the player has escaped already, don't allow them to move
				if currentPlayer.hasEscaped():
					continue

				self.air -= currentPlayer.getNumberTreasure()
				print "AMOUNT OF AIR: %s" % self.air

				direction = self.AI.optimalDirection(currentPlayer, self, currentEventDict["direction"])
				# Dice roll could be less than the total amount of treasure, don't allow player to go backwards
				numMoves = max(self.rollDice(currentEventDict["roll"]) - currentPlayer.getNumberTreasure(), 0)

				self.movePlayer(currentPlayer, direction, numMoves)

				# If the player has escaped after moving, don't allow them to pick up anymore treasure
				if currentPlayer.hasEscaped():
					continue

				action, dropTreasure = self.AI.optimalAction(currentPlayer, self, currentEventDict["action"])

				if action == "PICK UP":
					currentPlayer.pickUpTreasure(self.treasureMap[currentPlayer.getLocation()])
					self.treasureMap[currentPlayer.getLocation()] = Treasure(0,0)

				elif action == "PUT DOWN":
					currentPlayer.putDownTreasure(dropTreasure)
					self.treasureMap[currentPlayer.getLocation()] = dropTreasure

				print currentPlayer
				print "TREASURE_MAP: %s" % self.treasureMap
				print "\n\n\n"

				# time.sleep(0.1)

			self.parseSystemEvent("CHECK_STATUS")
			self.parseSystemEvent("END_ROUND")
			playerIndex = self.endRound(playerIndex)
			print 'ENDING ROUND: %s \n\n\n' % roundNumber


		playerPointDict = self.getPlayersPointDistribution()
		return playerPointDict

testEventFile = "test_moves_4_player.txt"

deepsea_board = Board(4, testEventFile)
pointDict = deepsea_board.play()

for player in pointDict.keys():
	print "PLAYER %s: %s" % (player, pointDict[player])
