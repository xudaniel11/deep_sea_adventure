import json

with open("test_moves_4_player.txt", 'rb') as inputFile:
	# a = json.loads(inputFile.read())
	# print a
	for line in inputFile:
		a = json.loads(line)
		print a