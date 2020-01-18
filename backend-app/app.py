from flask import Flask, render_template, request, jsonify, json
from Host import Host
from Game import Game
from Board import Board
from Player import Player
from Block import Block
from Set import Set

app = Flask(__name__)
host = Host()


# https://www.w3schools.com/python/module_random.asp
# https://docs.python.org/3/library/random.html#random.random

players = [Player('szymon'), Player('barbara'), Player('arkadiusz')]
game = Game('local', players)
blocks = game.make_blocks()
blocks_set = Set(1, [Block(1, 'green', 5), Block(2, 'blue', 5),
                     Block(3, 'yellow', 5)])
blocks_set.add_blocks(
    *[Block(6, 'purple', 0)], update=True)

blocks_set.replace_joker(Block(104, 'red', 5, 1))

blocks_set2 = Set(
    2, [Block(10, 'green', 8), Block(22, 'purple', 0), Block(9, 'green', 7), Block(103, 'green', 5), Block(32, 'green', 4), Block(99, 'green', 9)])

blocks_set2.add_blocks(Block(97, 'green', 10),
                       Block(95, 'green', 3), update=True)
joker = blocks_set2.replace_joker(Block(106, 'green', 6))

game.board.add_set(blocks_set)
game.board.add_set(blocks_set2)


for s in game.board.sets:
    print('set: ', s.id)
    for block in s.blocks:
        print(block.get_dict())

print('-----------------------------------------')

game.board.update_set(2, action='remove', block_ids=[95, 97, 32, 103])
game.board.update_set(1, action='remove', block_ids=[3])

for s in game.board.sets:
    for block in s.blocks:
        print(block.get_dict())
    print('-------------------------------------------')

game.board.update_set(
    2, *[Block(84, 'green', 4), Block(79, 'purple', 0)], action='add')
game.board.update_set(1, *[Block(69, 'purple', 0)], action='add')

for s in game.board.sets:
    for block in s.blocks:
        print(block.get_dict())
    print('-------------------------------------------')

game.board.update_set(2, *[Block(82, 'green', 5)], action='replace')
game.board.update_set(1, *[Block(87, 'yellow', 5)], action='replace')

for s in game.board.sets:
    for block in s.blocks:
        print(block.get_dict())
    print('-------------------------------------------')

# print('---------------------------------------')
# print([(vars(block)['id'], vars(block)['value'], vars(block)['color'])
#        for block in game.unused_blocks])
# print('---------------------------------------')
# print(blocks_set.get_blocks())
# blocks_set.replace_joker(Block(104, 'red', 5))
# print('---------------------------------------')
# print(blocks_set.get_blocks())
# print('---------------------------------------')


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

# data: game_name, player_name, password, slots, type
# return: game_id, game_key, players, admin_id, game_name
@app.route('/newgame')
def init_game():
    print('init game')

# return: game_list = { game_key, game_id, game_name, free_slots, slots }
@app.route('/games')
def get_games():
    print('get games')

# return: board_is_updated=True/False, round_is_updated=True/False, is_finished, winner, players, current_player
@app.route('/round')
def check_state():
    print('check state')

# data: player_name, game_name, game_password
# return: game_id, game_key, game_name
@app.route('/join')
def join_to_game():
    print('join to game')

# data: game_id, game_key
# return: game_state, players
@app.route('/gamestatus')
def check_game():
    print('check game state')

# data: action = add/remove/replace, set = {set_id, set_type, set_status blocks = {block_id, value, color}, valid = True/False
# return: ok = True/False, is_finished = True/False, board = {sets={set_id, set_type, set_status, blocks={color, value, block_id}}}/None
@app.route('/update')
def update_board():
    print('update board')

# data: game_key, game_id, player_key, player_id, player_name
# return: players
@app.route('/giveup')
def give_up():
    print('give up')

# data: game_key, game_id, player_id, player_key
# return: block = {block_id, color, value}
@app.route('/getblock')
def get_block():
    print('get block')

# data: game_key, game_id, player_id, player_name
# return: players, current_player, is_finished, winner
@app.route('/nextround')
def next_round():
    print('next round')


if __name__ == "__main__":
    app.run(debug=True)
