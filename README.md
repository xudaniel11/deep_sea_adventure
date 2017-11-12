# Setup

* Clone repo

	`git clone https://github.com/xudaniel11/deep_sea_adventure.git`

* Required dependencies - Python 2.7+ and JSON

* Link to game rules (note game rules are slightly different than the Japanese Version for players who drop treasure when they die): https://tesera.ru/images/items/1058647/deep-sea-adventure-rulesf.pdf


* Run game

	`python ~/deep_sea_adventure/deepsea_board.py`


# DeepSea AI Interface Docs

A human or AI Player object can take

# To Do List

## Front End and UX

* Allow humans to perform actions within DeepSea AI using command line input

* Create Web UI for the DeepSea Game

## Infrastructure

* Move game run loop functions from deepsea_board.py to deepsea_engine.py

* Replace STRING PASSING action paradigm with enums

* Create WebServer for DeepSea Game

* Save past game state into output JSON so that it can be replayed and debugged

## AI

* Write AI Interface Docs

* Write heuristic based AI for deepsea_ai.py

* Allow human players and AI players to play against one another (command line)

## Testing + QA

* Add additional integration test JSON for Phase 2 and Phase 3 of game

* Add unit tests for each class

* Think about way to separate testing from Game Engine code. Ideally they should be separate