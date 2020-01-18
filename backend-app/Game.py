import random
from WithRepr import WithRepr
from WithStr import WithStr
from TypeControl import TypeControl
from Board import Board
from Player import Player
from Block import Block


class Game(WithRepr, WithStr, TypeControl):
    def __init__(self, game_type, players, key=None, board=Board()):
        self.id = None
        self.state = 'init'
        self.round_data = {'player_key': None, 'number': 0, 'time': None}
        self.is_finished = False
        self.errors = []
        self.type = game_type
        self.board = self.set_value(board, Board)
        self.players = self.set_value(players, Player)
        self.unused_blocks = self.make_blocks()
        self.key = key
        self.winner = None
        self.admin = None

    def get_dict(self):
        board = self.get_board()
        players = self.get_players()
        blocks = self.get_blocks()
        game_dict = self.__dict__
        game_dict['board'] = board
        game_dict['players'] = players
        game_dict['unused_blocks'] = blocks
        return game_dict

    def change_state(self, new_state):
        if self.state == new_state:
            return False

    def _check_round_data(self, current_state):
        print('')

    def _update_game_data(self, new_game_data):
        print('')

    def _change_player(self, next_player):
        print('')

    def _finish_game(self):
        print('')

    def get_players(self):
        return [player.get_dict() for player in self.players]

    def get_blocks(self):
        return [block.get_dict() for block in self.unused_blocks]

    def get_board(self):
        return self.board.get_dict()

    def get_block(self, block_id, as_dict=False):
        for block in self.unused_blocks:
            if block.id == block_id:
                if as_dict:
                    return block.get_dict()
                else:
                    return block
        return None

    def get_player(self, player_id, as_dict=False):
        for player in self.players:
            if player.id == player_id:
                if as_dict:
                    return player.get_dict()
                else:
                    return player
        return None

    def get_random_block(self):
        print('draw block method')

    def set_players_blocks(self):
        print('set players blocks')

    def start_game(self):
        print('start game - change game state, make and set blocks for players')

    def make_blocks(self, quantity=13, repeat=2, colors=['red', 'green', 'blue', 'yellow'], BlockClass=Block):
        _blocks = []
        i = 1
        while i <= repeat:
            for color in colors:
                for block_value in range(1, quantity + 1):
                    color_blocks = [BlockClass(
                        len(_blocks) + 1, color, block_value)]
                    _blocks.extend(color_blocks)
            _blocks.append(BlockClass(len(_blocks) + 1, 'purple', 0))
            i += 1
        return _blocks
