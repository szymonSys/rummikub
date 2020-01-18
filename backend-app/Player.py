from WithRepr import WithRepr
from WithStr import WithStr
from TypeControl import TypeControl
from Block import Block


class Player(WithRepr, WithStr, TypeControl):

    def __init__(self, name, player_type='net', state='in_lobby', blocks=[], game_id=None, game_key=None):
        self.id = None
        self.name = name
        self.type = player_type
        self.state = state
        self.blocks = self.set_value(blocks, Block)
        self.game_id = game_id
        self.game_key = game_key

    def get_dict(self):
        return self.__dict__

    def get_blocks(self):
        return [block.get_dict() for block in self.blocks]

    def remove_block(self, block_id, as_dict=False):
        print('remove block method')

    def add_block(self, block):
        print('add block method')

    def find_block(self, block_id, as_dict=False):
        for block in self.blocks:
            if block.id == block_id:
                if as_dict:
                    return block.get_dict()
                else:
                    return block
        return None
