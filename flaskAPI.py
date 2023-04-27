from flask import Flask, jsonify
from flask_restful import Api, abort
from flask_sqlalchemy import SQLAlchemy
from automaticWar import automaticWar
from peace import Peace
from underdog import Underdog

from war import War


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///war.db'
db = SQLAlchemy(app)

class WarGame(db.Model):
    id = db.Column(db.Integer, primary_key = True) # unique identifier
    playerA = db.Column(db.String(100)) # playerA's name
    playerB = db.Column(db.String(100)) # playerB's name
    winner = db.Column(db.String(100), nullable=False) # MUST take some sort of information
    # variation = db.Column(db.Integer) # variation type. Defaults to normal War if unspecified

    def __init__(self, id, playerA, playerB, winner):
        self.id = id
        self.playerA = playerA
        self.playerB = playerB
        self.winner = winner

    def __repr__(self):
        return f"War(player A = {self.playerA}, Player B = {self.playerB}, winner = {self.winner})"

class Player(db.Model):
    name = db.Column(db.String(100), primary_key = True)
    wins = db.Column(db.Integer, nullable = False)
    losses = db.Column(db.Integer)

    def __init__(self, name, wins, losses):
        self.name = name
        self.wins = wins
        self.losses = losses
    
    def __repr__(self):
        return f"Player {self.name}: {self.wins} wins, {self.losses} losses."

# Create the database tables

db.create_all()
# with app.app_context():
#     db.create_all()

'''
Functions:
0. help (GET) (not really GET but this is the only way I know how to show it)
1. runGame (POST)
2. getPlayerStats (GET)
3. getGame (GET)
'''
@app.route('/help', methods = ['GET'])
def help():
    helpMenu = {
        "/help": "Display menu options.",
        "/runGame/nameA/nameB": "Runs a full game of war between players A and B. Updates the WarGame and Player databases.",
        "/playerStats/name": "Pull's a player's stats from the database.",
        "/getGame/gameID": "Pull a game's information from the database."
    }
    return jsonify(helpMenu)


@app.route('/runGame/<int:var>/<string:A>/<string:B>', methods = ['POST'])
def runGame(var, A, B):
    gameID = WarGame.query.count() + 1
    if (var == 0):
        g = War(A, B)
    elif (var == 1):
        g = Peace(A, B)
    elif (var == 2):
        g = automaticWar(A, B)
    elif (var == 3):
        g = Underdog(A, B)
    else:
        abort(404, message = "Specified variation does not exist.")
    gWinner = g.play()

    gSetup = WarGame(id = gameID, playerA = A, playerB = B, winner = gWinner)
    db.session.add(gSetup)

    pA = Player.query.filter_by(name = A).first()
    if not pA:
        playerA = Player(A, 0, 0)
        db.session.add(playerA)
    else:
        if gWinner == A:
            pA.wins += 1
        else:
            pA.losses += 1
    
    pB = Player.query.filter_by(name = B).first()
    if not pB:
        playerB = Player(B, 0, 0)
        db.session.add(playerB)
    else:
        if gWinner == B:
            pB.wins += 1
        else:
            pB.losses += 1
    
    db.session.commit()

    result = {
        "gameID" : gameID,
        "variation" : var,
        "playerA": A,
        "playerB": B,
        "winner" : gWinner
    }
    return jsonify(result), 201


@app.route('/getStats/<string:playerName>', methods = ['GET'])
def getStats(playerName):
    p = Player.query.filter_by(name = playerName).first()
    if not p:
        abort(404, message = "No player exists under that name.")
    result = {
        "Name": p.name,
        "Number of lifetime wins" : p.wins,
        "Number of lifetime losses" : p.losses
    }
    return jsonify(result)



@app.route('/getGame/<int:gameID>', methods = ['GET'])
def getGame(gameID):
    g = WarGame.query.filter_by(id = gameID).first()
    if not g:
        abort(404, message = "No game exists under that ID.")
    result = {
        "ID": g.id,
        "player A" : g.playerA,
        "player B" : g.playerB,
        "winner" : g.winner
    }
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)

