from deepsea_treasure import Treasure
from deepsea_treasure import TreasureStack
import random

class AI:
	def optimalDirection(self, currentPlayer, board, direction=""):
		if direction == "UP":
			currentPlayer.diving = False
			return "UP"
		elif direction == "DOWN":
			return "DOWN"

		if currentPlayer.diving == False:
			return "UP"
		else:
			#if random.random() < 0.1 and (len(currentPlayer.getUnrevealedTreasure()) >= 1) and (currentPlayer.getLocation() != 0):
			if (len(currentPlayer.getUnrevealedTreasure()) >= 2):
				print "PLAYER %s GOING UP" % currentPlayer.getID()
				return "UP"
			print "PLAYER %s GOING DOWN" % currentPlayer.getID()				
			return "DOWN"

	def optimalAction(self, currentPlayer, board, action=""):
		if action != "":
			return (action, None)

		if currentPlayer.diving == False:
			return ("NONE", None)
		else:
			if random.random() < 0.999:
				if board.getTreasureMap()[currentPlayer.getLocation()].getNumDots() != 0:
					print "PLAYER %s PICKING UP TREASURE" % currentPlayer.getID()
					return ("PICK UP", None)
			return ("NONE", None)


	# Unrevealed Treasures may contain Treasure Stacks. These need to be "unwrapped" into regular treasure before being put into new treasure stacks
	def extractAllTreasure(self, unrevealedTreasureList):
		treasureList = []
		for treasure in unrevealedTreasureList:
			if treasure.isTreasureStack:
				for stackedTreasure in treasure.treasureSet:
					treasureList.append(stackedTreasure)
			else:
				treasureList.append(treasure)

		return treasureList


	def optimalDrown(self, currentPlayer, board):
		tempList = []
		treasureStackList = []

		unrevealedTreasureList = self.extractAllTreasure(currentPlayer.getUnrevealedTreasure())
		#print "PLAYER %s FULL TREASURE LIST: %s" % unrevealedTreasureList

		for unrevealedTreasure in unrevealedTreasureList:
			if len(tempList) == 3:
				treasureStackList.append(tempList[:])
				tempList = []
			tempList.append(unrevealedTreasure)

		#print "REMAINING TREASURE: %s" % tempList
		if len(tempList) > 0:
			treasureStackList.append(tempList)

		#print "PLAYER %s DROWN TREASURE LIST: %s" % (currentPlayer.getID(), treasureStackList)
		return treasureStackList

	def __eq__(self, other): 
		return self.__dict__ == other.__dict__
