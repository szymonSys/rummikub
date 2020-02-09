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

    def __init__(self, game_id, game_type, founder, name='', password=None, slots=4, board=Board(), key_generator=KeyGenerator.generate_key):
        self.id = game_id
        # init / ready / run / end
        self.state = 'init'
        self.name = name
        self.round_data = {
            'playerKey': None,
            'playerId': None,
            'number': 0,
            'isOngoing': False
        }
        self.founder = self.set_value(founder, Player)
        if self.check_instance(founder, Player):
            founder.id = self._next_player_id
            self._next_player_id += 1
        self.is_finished = False
        self.errors = []
        self._password = password
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

    def verify_password(self, password_provider):
        return self._password == password_provider

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

    def remove_player(self, player_key):
        player = self.find_player(player_key=player_key)
        if not self.check_instance(player, Player):
            return False
        self.players.remove(player)
        return True

    def find_player(self, player_id=None, player_key=None, as_dict=False):
        for player in self.players:
            if player.id == player_id or player._key == player_key:
                if as_dict:
                    return player.get_dict()
                else:
                    return player
        return None

    def remove_player_blocks(self, p_id, blocks_ids):
        if not isinstance(p_id, int):
            return None
        player = self.find_player(player_id=p_id)
        if not self.check_instance(player, Player):
            return None
        removed_blocks = player.remove_blocks(*blocks_ids)
        return removed_blocks

    def add_player_blocks(self, p_id, blocks):
        player = self.find_player(player_id=p_id)
        if not self.check_instance(player, Player):
            return False
        is_added = player.add_blocks(blocks)
        return is_added

    def find_blocks_from_players(self, *blocks_ids):
        if not isinstance(blocks_ids, (list, tuple)) or not bool(len(blocks_ids)):
            return None
        blocks = []
        for player in self.players:
            for block in player.blocks:
                for b_id in blocks_ids:
                    if b_id == block.id:
                        blocks.append(block)
        return blocks

    def get_blocks_from_all(self, *blocks_ids):
        found_blocks_from_board = self.board.find_blocks(*blocks_ids)
        found_blocks_from_players = self.find_blocks_from_players(*blocks_ids)
        board_blocks_status = self.check_instance(
            found_blocks_from_board, Block)
        players_blocks_status = self.check_instance(
            found_blocks_from_players, Block)
        if board_blocks_status:
            if players_blocks_status:
                return found_blocks_from_board + found_blocks_from_players
            return found_blocks_from_board
        if players_blocks_status:
            return found_blocks_from_players
        return None

    def add_player(self, new_player):
        if self.check_instance(new_player, Player) and len(self.players) < self.slots:
            new_player.id = self._next_player_id
            self._next_player_id += 1
            self.players.append(new_player)
            return True
        return False
        #     if self.check_is_ready():
        #         if self._update_to_ready():
        #             self.start_game()
        #     return True
        # else:
        #     return False

    def add_player_random_block(self, player_id=None, player=None):
        if self.check_instance(player, Player):
            this_player = player
        elif isinstance(player_id, int) or self.check_instance(player, Player):
            this_player = self.find_player(player_id)
            if not self.check_instance(player, Player):
                return False
        else:
            return False
        random_block = random.choice(self.unused_blocks)
        random_block.set_membership(player_id=player.id)
        this_player.add_block(random_block)
        self.unused_blocks.remove(random_block)
        return True

    def set_players_blocks(self, quantity=14):
        players_quantity = len(self.players)
        if self.players_has_set_blocks and self.state == 'ready' and players_quantity > 1 and players_quantity <= 4:
            return False
        for _ in range(0, quantity):
            for player in self.players:
                self.add_player_random_block(player=player)
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

    def _update_to_ready(self):
        if self.state == 'init':
            self.state = 'ready'
            return True
        return False

    def check_is_ready(self):
        if self.slots == len(self.players):
            return True
        if self.slots < len(self.players):
            raise SlotsExtension(
                'There are too many players in Game: can only be 2-4 slots.')
        return False

    def start_game(self):
        if self.state == 'ready' and len(self.players) == self.slots:
            self.set_players_blocks()
            random_sequence = [(player._key, player.id)
                               for player in self.players]
            random.shuffle(random_sequence)
            self._players_queue = random_sequence
            self.round_data['player_key'] = self._players_queue[0][0]
            self.round_data['player_id'] = self._players_queue[0][1]
            self.round_data['number'] = 1
            self.round_data['is_ongoing'] = True
            self.state = 'run'
            for player in self.players:
                player.change_to_game()
            return True
        return False

    def check_game(self, prev_state):
        has_change = False
        if prev_state == 'init' or prev_state == 'ready' or prev_state == 'run' or prev_state == 'end':
            if self.state != prev_state:
                has_change = True
        return has_change

    def check_round(self, player_key):
        if isinstance(player_key, str):
            if not self.check_instance(self.find_player(player_key), Player):
                return None
            return self.round_data.get('isOngoing')

    def check_board(self, board_id):
        has_change = False
        if isinstance(board_id, str) and self.board.state_id != board_id:
            has_change = True
        return has_change

    def update_round_data(self, is_ongoing, as_dict=True):
        if not isinstance(is_ongoing, bool) or self.round_data.get('isOngoing') == is_ongoing:
            return None
        if is_ongoing and not self.round_data.get('isOngoing'):
            next_player = self._next_player()
            if not bool(next_player):
                return None
            self.round_data['number'] += 1
            self._set_winner_if_finished(self.round_data.get('playerKey'))
            self.round_data['playerKey'] = next_player[0]
            self.round_data['playerId'] = next_player[1]
        self.round_data['isOngoing'] = is_ongoing
        if as_dict:
            return self.get_round_data()
        return self.round_data

    def _next_player(self):
        return self._handle_queue()

    def get_round_data(self):
        round_data = {}
        for key in self.round_data.keys():
            if key == 'playerKey':
                continue
            else:
                round_data[key] = self.round_data[key]
        return round_data

    def _set_winner_if_finished(self, p_key):
        if self.state == 'run':
            print(p_key)
            player = self.find_player(player_key=p_key)
            if not bool(len(player.blocks)):
                self.is_finished = True
                self.state = 'end'
                self.winner = {'name': player.name,
                               'id': player.id, 'key': player.get_key()}
                return self.winner
        return None

    def _handle_queue(self):
        index = -1
        for player in self._players_queue:
            if player[0] == self.round_data.get('playerKey'):
                index = self._players_queue.index(player)
                break
        if index == -1:
            return None
        if index == len(self._players_queue) - 1:
            index = 0
        else:
            index += 1
        return self._players_queue[index]
