class Treasure:
	# numDots = 0 --> Treasure Marker
	def __init__(self, numDots, value):
		self.numDots = numDots
		self.value = value
		self.isTreasureStack = False
		self.isTreasure = True

	def getNumDots(self):
		return self.numDots

	def getValue(self):
		return self.value

	def __repr__(self):
		return "Treasure: (%s, %s)" % (self.numDots, self.value)

	def __str__(self):
		return "Treasure: (%s, %s)" % (self.numDots, self.value)

	def testCompare(self, other): 
		return self.__dict__ == other.__dict__


class TreasureStack:
	def __init__(self, treasureSet):
		self.treasureSet = treasureSet
		self.isTreasureStack = True
		self.isTreasure = False

	def getNumDots(self):
		return None

	def getValue(self):
		totalValue = 0
		for treasure in self.treasureSet:
			totalValue += treasure.getValue()

		return totalValue

	def getExpectedValue(self):
		expectedValue = 0
		for treasure in self.treasureSet:
			expectedValue += treasure.getExpectedValue()

		return expectedValue

	def __repr__(self):
		outputStrList = []
		for treasure in self.treasureSet:
			outputStrList.append(treasure.__str__())

		return "[%s]" % ", ".join(outputStrList)

	def __str__(self):
		outputStrList = []
		for treasure in self.treasureSet:
			outputStrList.append(treasure.__str__())

		return "[%s]" % ", ".join(outputStrList)

	def testCompare(self, other): 
		return self.__dict__ == other.__dict__
