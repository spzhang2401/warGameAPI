# warGameAPI

This is a implementation of a simulation of the popular card game War, with multiple variant options. This code uses
flask to create a RESTful API that runs the game logic from war.py (or the variations) and stores game and player information using SQLAlchemy inside of flaskAPI.py. test.http was used to test the requests locally with the REST client VScode extension.

To set up, download the contents of this repo into a local folder and run the following command:

pip install -r requirements.txt

Afterwards, use the terminal to run:

python3 flaskAPI.py

The server should be up and running at this point. 

As for requests to the server, I have the following endpoints:

1. GET '/help' -- this lists out the other possible endpoints.

2. POST '/runGame/<int:var>/<string:A>/<string:B>' -- this takes in a variation number (see below), player A's name, and player B's name, and simulates the game depending upon the corresponding variation.

3. GET '/getStats/<string:playerName>' -- this takes a player's unique name and returns their lifetime wins and losses.

4. GET '/getGame/<int:gameID>' -- this takes a gameID and returns the game's variation number, players, and the winner.

For variation numbers, refer to the following:

0. War (original)
1. Peace: the card with the lower number wins.
2. automaticWar: placing a card of rank 2 triggers war as well.
3. Underdog: The losing player of a War steals the victory if one of their discard cards is a Jack.

Given more time, I would have loved to implement more complex, multi-player variants of the game. I would have also loved to implement a GUI for this project. I've learned just this semester how to do so with a Java back-end and a TypeScript front-end, but figured I may need more time to learn how the same principles work with a language like Python. 