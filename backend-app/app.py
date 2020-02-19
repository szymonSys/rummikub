from flask import Flask, render_template, request, jsonify, json
from Player import Player
from Game import Game
from Host import Host
from Block import Block

app = Flask(__name__)
host = Host()


def _steer_round(data, start=False):
    game = host.find_game(data.get('gameKey'))
    player = game.find_player(player_key=data.get('playerKey'))
    if host.check_instance(game, Game) and host.check_instance(player, Player):
        round_data = host.menage_round(start=start, target_game=game)
        data = {'roundData': round_data}
        if start:
            player.drew_block = False
            data['drewBlock'] = player.drew_block
        return jsonify(data)
    return jsonify({'errors': 'failed to change round status'})


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# data: gameType = 'multiplayer'/'singleplayer'/'localgame',  gameName = str/None, gamePassword = str/None founderName = str,  slots = 1<int<5, founderType = 'net'/'local'
# return: gameData = {state, key, kasPassword, type, name, slots, playersData, winner}, founderData = {name, type, key, gameKey, hasCleanSet, gotBlocks}
@app.route('/create-game', methods=['POST'])
def init_game():
    data = request.get_json(silent=True, force=True)
    founder = host.create_player(
        data.get('founderName'),
        data.get('founderType')
    )
    if not host.check_instance(founder, Player):
        return jsonify({'error': 'invalid Player instance'})
    game = host.create_game(
        data.get('type'),
        founder,
        name=data.get('gameName'),
        password=data.get('gamePassword'),
        slots=int(data.get('slots'))
    )
    founder.set_game_key(game.get_key())
    if not host.check_instance(game, Game):
        return jsonify({'error': 'invalid Game instance'})
    if host.add_game(game):
        return jsonify({'founderKey': founder.get_key(), 'gameKey': game.get_key()})
        # return jsonify({
        #     'founderData': host.get_player_data(target_player=founder, target_game=game),
        #     'gameData': host.get_games_data(player_key=founder.get_key(), target_game=game)
        # })
    return jsonify({'error': 'game has not added'})

# data: gameKey, founderKey, players:[playerData: {name, type}]
# return players
@app.route('/join-everyone', methods=['POST'])
def join_everyone_to_game():
    data = request.get_json(silent=True, force=True)
    players = data.get('players')[:]
    game_key = data.get('gameKey')
    if isinstance(game_key, str):
        game = host.find_game(game_key)
        if not host.check_instance(game, Game):
            return jsonify({'errors': 'game not found'})
    if not game.check_membership(data.get('founderKey')):
        return jsonify({'errors': 'player does not belong to given game.'})
    new_players = []
    for playerData in players:
        if not isinstance(playerData.name, str):
            return jsonify({'errors': 'invalid player name'})
        new_player = host.create_player(playerData.name, playerData.type)
        if not host.check_instance(new_player, Player):
            return jsonify({'errors': 'failed to create player'})
        status = host.join_player(new_player, target_game=game)
        errors = []
        ok = True
        for key in status:
            if not status[key]:
                ok = False
                errors.append(key)
        if not ok:
            return jsonify({
                'errors': {
                    'joinStatusErrors': errors
                }
            })
        new_players.append({
            'playerKey': new_player.get_key(),
            'playerId': new_player.id,
            'playerName': new_player.name,
            'playerType': new_player.type
        })

    return jsonify({'playersData': new_players})

# return: gameList = [gameData]
@app.route('/get-games', methods=['GET'])
def get_games():
    games_data = []
    for game_data in host.get_games_data()[:]:
        if game_data.get('type') == 'multiplayer' and game_data.get('state') == 'init':
            games_data.append(game_data)
    return jsonify({'gamesData': games_data})


# data: gameKey, playerKey
# return: roundData = {playerId, number, isOngoing}
@app.route('/get-round-data', methods=['POST'])
def get_round_data():
    data = request.get_json(silent=True, force=True)
    round_data = host.get_round_data(
        player_key=data.get('playerKey'),
        game_key=data.get('gameKey')
    )
    return jsonify({'roundData': round_data})

# data: gameKey, playerKey
# return: isFinished = bool, board = {Id: str, sets: [sets]/None}
@app.route('/get-board-data', methods=['POST'])
def get_board_data():
    data = request.get_json(silent=True, force=True)
    board_data = host.get_board_data(
        player_key=data.get('playerKey'),
        game_key=data.get('gameKey')
    )
    return jsonify({'boardData': board_data})

# data: gameKey, playerKey
# return: gameData = {}
@app.route('/get-game-data', methods=['POST'])
def get_game_data():
    data = request.get_json(silent=True, force=True)
    game_data = host.get_games_data(
        player_key=data.get('playerKey'),
        game_key=data.get('gameKey')
    )
    return jsonify({'gameData': game_data})

# data: gameKey, playerKey
# return: playersData = {players, slots, gameName}
@app.route('/get-game-players', methods=['POST'])
def get_game_players():
    data = request.get_json(silent=True, force=True)
    game = host.find_game(game_key=data.get('gameKey'))
    if not host.check_membership(data.get('playerKey'), game):
        return jsonify({'errors': 'player does not belong to given game.'})
    playersData = []
    for player in game.players:
        playersData.append({'name': player.name, 'id': player.id})
    response_data = {'playersData': playersData,
                     'slots': game.slots, 'gameName': game.name}
    return jsonify(response_data)

# data: playerName, playerType, gameKey = str/None, gamePassword = str/None
# return: gameData = {state, key, hasPassword, type, name, slots, playersData, winner}, playerData = {name, type, key, gameKey, has_cleen_set}
@app.route('/join', methods=['POST'])
def join_to_game():
    data = request.get_json(silent=True, force=True)
    player_name = data.get('playerName')
    password = data.get('gamePassword')
    game_key = data.get('gameKey')
    if not isinstance(player_name, str):
        return jsonify({'errors': 'invalid player name'})
    player = host.create_player(player_name, data.get('playerType'))
    if not host.check_instance(player, Player):
        return jsonify({'errors': 'failed to create player'})
    if isinstance(game_key, str):
        game = host.find_game(game_key)
        if not host.check_instance(game, Game):
            return jsonify({'errors': 'game not found'})
        if not game.verify_password(password):
            return jsonify({'errors': 'invalid password'})
    else:
        print('else')
        # game = dobieranie gry na zasadzie 'tam gdzie wiecej graczy'
    status = host.join_player(player, target_game=game, password=password)
    errors = []
    ok = True
    for key in status:
        if not status[key]:
            ok = False
            errors.append(key)
    if not ok:
        return jsonify({
            'errors': {
                'joinStatusErrors': errors
            }
        })
    player_data = host.get_player_data(
        target_player=player, player_key=player.get_key(), target_game=game)
    game_data = host.get_games_data(
        player_key=player.get_key(), target_game=game)
    if player_data == None or game_data == None:
        return jsonify({'errors': 'incorrect data'})
    return jsonify({
        'playerData': player_data,
        'gameData': game_data
    })


# data: gameKey, playerKey, gameState, boardId
# return: {game: bool, board: bool, round: bool}
@app.route('/check-updates', methods=['POST'])
def check_game():
    data = request.get_json(silent=True, force=True)
    data_status = host.check_data(
        data.get('gameState'),
        data.get('boardId'),
        data.get('playerKey'),
        game_key=data.get('gameKey')
    )
    return jsonify(data_status)


# data: ids = [blocks_ids], setId = int/None, replace = bool, playerKey, gameKey
# return: isUpdated = bool, board = {stateId: str, sets: [sets]/None}
@app.route('/update-board', methods=['POST'])
def update_board():
    data = request.get_json(silent=True, force=True)
    is_updated = host.update_board(
        data.get('gameKey'),
        *data.get('blocksIds'),
        target_set_id=data.get('setId'),
        replace=data.get('replace')
    )
    # if is_updated:
    board_data = host.get_board_data(
        player_key=data.get('playerKey'),
        game_key=data.get('gameKey')
    )
    return jsonify({
        'isUpdated': is_updated,
        'boardData': board_data
    })
    # return jsonify({'isUpdated': is_updated, 'errors': 'failed to update the board'})


# data: gameKey, playerKey
# return: bool
@app.route('/give-up')
def give_up():
    # data = request.get_json(silent=True, force=True)
    pass

# data: gameKey, playerKey
# return: blocksData
@app.route('/get-block', methods=['POST'])
def get_block():
    data = request.get_json(silent=True, force=True)
    game = host.find_game(game_key=data.get('gameKey'))
    if not host.check_instance(game, Game):
        return jsonify({'errors': 'game not found'})
    player = game.find_player(player_key=data.get('playerKey'))
    if not host.check_instance(player, Player):
        return jsonify({'errors': 'player not found'})
    if player.drew_block:
        return jsonify({'blocks': player.get_blocks(), 'drewBlock': player.drew_block})
    if game.add_player_random_block(player=player) or game.state == 'end':
        player.drew_block = True
        return jsonify({'blocks': player.get_blocks(), 'drewBlock': player.drew_block})
    return jsonify({'blocks': player.get_blocks(), 'errors': 'failed to draw the block'})

# data: gameKey, playerKey
# return: playerData (with blocks)
@app.route('/get-player-data', methods=['POST'])
def get_player_data():
    data = request.get_json(silent=True, force=True)
    game = host.find_game(game_key=data.get('gameKey'))
    if host.check_instance(game, Game):
        player = game.find_player(player_key=data.get('playerKey'))
        if host.check_instance(player, Player) and game.state == 'run':
            player_data = host.get_player_data(
                target_player=player,
                target_game=game
            )
            return jsonify({'playerData': player_data})
    return jsonify({'errors': 'unable to get game data'})

# data: gameKey, playerKey
# return: roundData = {playerId, number, isOngoing}
@app.route('/finish-round', methods=['POST'])
def finish_round():
    data = request.get_json(silent=True, force=True)
    return _steer_round(data)

# data: gameKey, playerKey
# return: roundData = {playerId, number, isOngoing}
@app.route('/start-round', methods=['POST'])
def start_round():
    data = request.get_json(silent=True, force=True)
    return _steer_round(data, start=True)


if __name__ == "__main__":
    app.run(debug=True)
