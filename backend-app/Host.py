from WithRepr import WithRepr
from WithStr import WithStr
from TypeControl import TypeControl
from Game import Game
from Player import Player


class SingletonException(Exception):
    pass


class Host(WithStr, WithRepr, TypeControl):
    _has_instance = False

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
        print('')

    def find_game(self, game_key):
        print('')

    def get_player(self, player_id, as_dict=False):
        print('')

    def get_palyers(self, as_dict=False):
        print('')

    def add_game(self):
        print('')

    def add_player(self):
        print('')

    def remove_player(self):
        print('')

    def remove_game(self):
        print('')

    def make_match(self):
        print('')

    def match_player(self, player_id, game_id=None):
        print('')
