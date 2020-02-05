from flask import Flask, render_template, request, jsonify, json
from Player import Player
from Game import Game
from Host import Host
from Block import Block
from TypeControl import TypeControl

app = Flask(__name__)
host = Host()
type_control = TypeControl()

# print(json.dumps(vars(blocks[1])))
# print(json.dumps(game.get_dict()))

helloes = ['Hello, World!']


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/hello', methods=['POST', 'GET'])
def hello():
    if request.method == 'POST':
        print(request.mimetype)
        print(request.is_json)
        data = json.loads(request.get_json(silent=True, force=True))
        print(data['hello'])
        hello = data['hello']
        helloes.append(hello)
    return jsonify({'msg': helloes})

# data: gameType = 'multiplayer'/'singleplayer'/'localgame',  gameName = str/None, gamePassword = str/None founderName = str,  slots = 1<int<5, founderType = 'net'/'local'
# return: gameData = {state, key, kasPassword, type, name, slots, playersData, winner}, founderData = {name, type, key, gameKey, hasCleanSet, gotBlocks}
@app.route('/createGame')
def init_game():
    data = json.loads(request.get_json(silent=True, force=True))
    founder = host.create_player(
        data.get('founderName'),
        data.get('founderType')
    )
    if not type_control.check_instance(founder, Player):
        return jsonify({'error': 'invalid Player instance'})
    game = host.create_game(
        data.get('gameType'),
        founder,
        name=data.get('gameName'),
        password=data.get('gamePassword'),
        slots=data.get('slots')
    )
    if not type_control.check_instance(game, Game):
        return jsonify({'error': 'invalid Game instance'})
    if host.add_game(game):
        return jsonify({
            'founderData': host.get_player_data(target_player=founder, target_game=game),
            'gameData': host.get_games_data(target_game=game)
        })
    return jsonify({'error': 'game has not added'})


# return: gameList = [gameData]
@app.route('/getGames')
def get_games():
    pass

# data: gameKey, playerKey
# return: roundData = {playerId, number, isOngoing}
@app.route('/getRoundData')
def get_round_data():
    pass

# data: gameKey, playerKey
# return: isFinished = bool, board = {stateId: str, sets: [sets]/None}
@app.route('/getBoardData')
def get_board_data():
    pass

# data: gameKey, playerKey
# return: gameData = {}
@app.route('/getGameData')
def get_game_data():
    pass

# data: playerName, gameKey = str/None, gamePassword = str/None
# return: gameData = {state, key, kasPassword, type, name, slots, playersData, winner}, playerData = {name, type, key, gameKey, has_cleen_set}
@app.route('/join')
def join_to_game():
    pass

# data: gameKey, playerKey, isOngoing, gameState, boardId
# return: {game: bool, board: bool, round: bool}
@app.route('/checkUpdates')
def check_game():
    pass

# data: ids = [blocks_ids], setId = int/None, replace = bool, playerKey
# return: isFinished = bool, board = {stateId: str, sets: [sets]/None}
@app.route('/boardUpdate')
def update_board():
    pass

# data: gameKey, playerKey
# return: bool
@app.route('/giveup')
def give_up():
    pass

# data: gameKey, playerKey, playerId
# return: blockData
@app.route('/getBlock')
def get_block():
    pass

# data: gameKey, playerKey
# return: playerData (with blocks)
@app.route('/startGame')
def start_game():
    pass

# data: gameKey, playerKey
# return: roundData = {playerId, number, isOngoing}
@app.route('/finishRound')
def finish_round():
    pass

# data: gameKey, playerKey
# return: roundData = {playerId, number, isOngoing}
@app.route('/startRound')
def start_round():
    pass


if __name__ == "__main__":
    app.run(debug=True)
