import types
import random
from WithRepr import WithRepr
from WithStr import WithStr
from TypeControl import TypeControl
from Board import Board
from Player import Player
from Block import Block
from KeyGenerator import KeyGenerator


class SlotsExtension(Exception):
    pass


class Game(WithRepr, WithStr, TypeControl):
    _next_player_id = 1

    def __init__(self, game_id, game_type, founder, slots=4, board=Board(), key_generator=KeyGenerator.generate_key):
        self.id = game_id
        # init / ready / run / end
        self.state = 'init'
        self.round_data = {'player_key': None,
                           'number': 0, 'is_ongoing': False}
        self.founder = self.set_value(founder, Player)
        if self.check_instance(founder, Player):
            founder.id = self._next_player_id
            self._next_player_id += 1
        self.is_finished = False
        self.errors = []
        # multiplayer / singleplayer / localgame
        self.type = game_type
        self.board = self.set_value(board, Board)
        self.players = [self.set_value(founder, Player)]
        self.unused_blocks = self.make_blocks()
        self._key = key_generator()
        self.winner = None
        if slots > 1 and slots <= 4:
            self.slots = slots
        else:
            self.slots = None
            raise SlotsExtension('There can be 2-4 slots in the Game.')
        self.players_has_set_blocks = False
        self._players_queue = []

    def get_dict(self):
        board = self.get_board()
        players = self.get_players()
        blocks = self.get_blocks()
        game_dict = self.__dict__
        game_dict['board'] = board
        game_dict['players'] = players
        game_dict['unused_blocks'] = blocks
        return game_dict

    def get_key(self):
        return self._key

    def change_state(self, new_state):
        if self.state == new_state:
            return False

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

    def find_player(self, player_id=None, player_key=None, as_dict=False):
        for player in self.players:
            if (bool(player_id) and player.id == player_id) or (bool(player_key) and self._key == player_key):
                if as_dict:
                    return player.get_dict()
                else:
                    return player
        return None

    def add_player(self, new_player):
        if self.check_instance(new_player, Player) and len(self.players) < self.slots:
            new_player.id = self._next_player_id
            self._next_player_id += 1
            self.players.append(new_player)
            return True
        else:
            return False

    def add_player_block(self, player_id):
        if not isinstance(player_id, int):
            return None
        player = self.find_player(player_id)
        if not self.check_instance(player, Player):
            return None
        random_block = random.choice(self.unused_blocks)
        player.add_block(random_block)
        self.unused_blocks.remove(random_block)
        return random_block

    def set_players_blocks(self, quantity=14):
        players_quantity = len(self.players)
        if self.players_has_set_blocks and self.state == 'ready' and players_quantity > 1 and players_quantity <= 4:
            return False
        for _ in range(0, quantity):
            for player in self.players:
                if not self.check_instance(player, Player):
                    return False
                random_block = random.choice(self.unused_blocks)
                random_block.set_membership(player_id=player.id)
                player.add_block(random_block)
                self.unused_blocks.remove(random_block)
        return True

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

    def _check_is_ready(self):
        if self.slots < len(self.players):
            raise SlotsExtension(
                'There are too many players in Game: can only be 2-4 slots.')
        if self.slots == len(self.players):
            self.state = 'ready'
            self._start_game()

    def _start_game(self):
        if self.state == 'ready' and len(self.players) == self.slots:
            self.set_players_blocks()
            self.state = 'run'
            self._players_queue = [
                player.key for player in random.choice(self.players)]
            self.round_data['player_key'] = self._players_queue[0]
            self.round_data['number'] = 1
            self.round_data['is_ongoing'] = True
        return self.state

    def check_data(self, prev_state, is_ongoing):
        has_changes = {'game': False, 'round': False}
        if prev_state == 'init' or prev_state == 'ready' or prev_state == 'run' or prev_state == 'end':
            if self.state != prev_state:
                has_changes['game'] = True
        if isinstance(is_ongoing, bool) and self.round_data['is_ongoing'] != is_ongoing:
            has_changes['round'] = True
        return has_changes

    def _update_round_data(self, is_ongoing):
        if not isinstance(is_ongoing, bool) and self.round_data['is_ongoing'] == is_ongoing:
            return None
        self.round_data['number'] += 1
        if not is_ongoing:
            self._set_winner_if_finished(self.round_data['player_key'])
            self.round_data['player_key'] = self._next_player()
        self.round_data['is_ongoing'] = is_ongoing
        return self.round_data

    def _next_player(self):
        return self._handle_queue()

    def _set_winner_if_finished(self, p_key):
        if self.state == 'run':
            player = self.find_player(player_key=p_key)
            if not bool(len(player.blocks)):
                self.is_finished = True
                self.state = 'end'
                self.winner = player
                return self.winner
        return None

    def _handle_queue(self):
        for player_key in self._players_queue:
            if player_key == self.round_data['player_key']:
                index = self._players_queue.index(player_key)
                break
        if index == len(self._players_queue) - 1:
            index = 0
        else:
            index += 1
        return self._players_queue[index]
