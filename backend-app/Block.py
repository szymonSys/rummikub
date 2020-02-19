from WithRepr import WithRepr
from WithStr import WithStr
import copy


class Block(WithRepr, WithStr):
    def __init__(self, block_id, color, value, set_id=None, player_id=None):
        self.id = block_id
        self.color = color
        self.value = value
        self.set_id = set_id
        self.player_id = player_id
        self.membership = None
        self.set_membership()

    def set_membership(self, set_id=None, player_id=None):
        if isinstance(set_id, int):
            self.set_id = set_id
            self.membership = 'set'
        elif isinstance(player_id, int):
            self.player_id = player_id
            self.membership = 'player'
        else:
            self.membership = None

    def get_dict(self):
        return copy.deepcopy(self.__dict__)
