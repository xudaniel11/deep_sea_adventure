from deepsea_ai import AI
from deepsea_treasure import Treasure
from deepsea_treasure import TreasureStack

class Player:
	def __init__(self, playerID, board):
		self.playerID = playerID
		self.board = board
		self.location = -1
		self.diving = True
		self.treasure_unrevealed = set()
		self.treasure_revealed = set()
		self.escaped = False
		self.AI = AI()

	def pickUpTreasure(self, treasure):
		self.treasure_unrevealed.add(treasure)		

	def putDownTreasure(self, treasure):
		self.treasure_unrevealed.remove(treasure)

	def escape(self):
		self.treasure_revealed = self.treasure_revealed.union(self.treasure_unrevealed)
		self.treasure_unrevealed = set()
		self.escaped = True
		self.location = -1

	def drown(self):
		treasureBuckets = self.AI.optimalDrown(self, self.board)
		treasureStackList = []

		for stack in treasureBuckets:
			treasureStackList.append(TreasureStack(stack))

		self.treasure_unrevealed = set()

		return treasureStackList

	def resetRound(self):
		self.location = -1
		self.diving = True
		self.escaped = False
		self.treasure_unrevealed = set()

	def setLocation(self, location):
		self.location = location

	def getLocation(self):
		return self.location

	def getUnrevealedTreasure(self):
		return self.treasure_unrevealed


	def getRevealedTreasure(self):
		return self.treasure_revealed

	def getID(self):
		return self.playerID

	def getNumberTreasure(self):
		return len(self.treasure_unrevealed)

	def hasEscaped(self):
		return self.escaped

	def __repr__(self):
		return "PLAYER %s: {location: %s, diving: %s, treasure revealed: %s, treasure unrevealed: %s}" % (self.playerID, self.location, self.diving, self.treasure_revealed, self.treasure_unrevealed)

	def __str__(self):
		return "PLAYER %s: {location: %s, diving: %s, treasure revealed: %s, treasure unrevealed: %s}" % (self.playerID, self.location, self.diving, self.treasure_revealed, self.treasure_unrevealed)


	def testCompare(self, other):
		if (self.playerID != other.playerID): 
			print "ID Mismatch"
			return False

		if (self.location != other.location): 
			print "Location Mismatch"
			return False

		if (self.diving != other.diving): 
			print "Diving Mismatch"
			return False

		# SUPER HACKY SET COMPARATOR IMPLEMENTATION. POTENTIAL FOR STRING MATCH REPRESENTATION BUG IS HIGH
		if (sorted(self.treasure_unrevealed.__str__()) != sorted(other.treasure_unrevealed.__str__())): 
			print "Treasure_Unrevealed Mismatch"
			return False

		if (sorted(self.treasure_revealed.__str__()) != sorted(other.treasure_revealed.__str__())): 
			print "Treasure_Revealed Mismatch"
			return False

		if (self.escaped != other.escaped): 
			print "Escaped Mismatch"
			return False

		return True