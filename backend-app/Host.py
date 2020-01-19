from WithRepr import WithRepr
from WithStr import WithStr
from TypeControl import TypeControl
from Game import Game
from Player import Player


class SingletonException(Exception):
    pass


class Host(WithStr, WithRepr, TypeControl):
    _has_instance = False
    _next_game_id = 1

    def __init__(self):
        self._players_queue = {}
        self._games = []
        Host.add_instance()

    @staticmethod
    def add_instance():
        if Host._has_instance:
            raise SingletonException(
                ' <Host> class can has only one instance.')
        else:
            Host._has_instance = True

    def get_games(self, as_dict=False):
        pass

    def find_game(self, game_key):
        pass

    def find_player(self, player_key, as_dict=False):
        pass

    def find_board(self, game_key):
        pass

    def find_set(self, set_id, game_key): pass

    def get_palyers(self, as_dict=False):
        pass

    def update_board(self, game_key, sets=[
                     {'set_id': None, 'action': None, 'blocks': [None]}]): pass

    def add_game(self, name, game_type, founder, GameClass=Game):
        game = Game(self._next_game_id, game_type, founder=founder)
        if not self.check_instance(game, Game):
            return False
        self._games.append(game)
        self._next_game_id += 1

    def add_player(self, player, game_key):
        pass

    def remove_player(self, player_key, game_key):
        pass

    def remove_game(self, game_key):
        pass

    def make_match(self):
        pass

    def match_player(self, player_key, game_id=None):
        pass
