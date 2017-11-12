# Setup

* Clone repo

	`git clone https://github.com/xudaniel11/deep_sea_adventure.git`

* Required dependencies - Python 2.7+ and JSON

* Link to game rules (note game rules are slightly different than the Japanese Version for players who drop treasure when they die): https://tesera.ru/images/items/1058647/deep-sea-adventure-rulesf.pdf


* Run game

	`python ~/deep_sea_adventure/deepsea_board.py`


# DeepSea AI Interface Docs

Over the course of the game, a human or AI Player object can perform the following actions.

* optimalDirection: Prior to rolling the dice, decide to go UP or DOWN (player must hold at least one treasure before he / she is allowed to return)

* optimalAction: After rolling the dice, decide to PICK UP, PUT DOWN, or DO NOTHING with his / her treasure after landing on a new destination

* optimalDrown: After drowning, select the order with which to place the dropped treasure at the end of the map

Actions are passed to the Game Engine / Board using Strings (todo: switch to Enums)

The above functions have default (dumb) behavior for testing purposes. Custom written AI's should override the above functions while maintaining the action passing interface. 


# To Do List

## Front End and UX

* Allow humans to perform actions within DeepSea AI using command line input

* Create Web UI for the DeepSea Game

## Infrastructure

* Move game run loop functions from deepsea_board.py to deepsea_engine.py

* Replace STRING PASSING action paradigm with enums.

* Encapsulate action passing with an Action class (this way we can describe which items we are dropping and the order)

* Create WebServer for DeepSea Game

* Save past game state into output JSON so that it can be replayed and debugged

* OPTIONAL - Implement all Treasure as TreasureStack Objects (single Treasure would just be a Stack with one Treasure)

## AI

* Write AI Interface Docs

* Write AI Interface Class (should be deepsea_ai.py)

* Move current AI Implementation to AIDummy class (AIDummy)

* Write full heuristic based AI for deepsea_ai.py (AIDefault)

* Allow human players and AI players to play against one another (command line)

## Testing + QA

* Add additional integration test JSON for Phase 2 and Phase 3 of game

* Add unit tests for each class

* Think about way to separate testing from Game Engine code. Ideally they should be separate