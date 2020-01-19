import types
from WithRepr import WithRepr
from WithStr import WithStr
from TypeControl import TypeControl
from Block import Block
from KeyGenerator import KeyGenerator


class Player(WithRepr, WithStr, TypeControl):

    def __init__(self, name, player_type='net', state='in_lobby', blocks=[], game_id=None, game_key=None, key_generator=KeyGenerator.generate_key):
        self.id = None
        self.name = name
        self.type = player_type
        self.state = state
        self.blocks = self.set_value(blocks, Block)
        self.game_id = game_id
        self._key = key_generator()
        self.has_clean_set = False

    def get_dict(self):
        return self.__dict__

    def get_key(self):
        return self._key

    def get_blocks(self):
        return [block.get_dict() for block in self.blocks]

    def remove_blocks(self, block_ids, as_dict=False):
        if len(self.blocks) < len(block_ids):
            return None
        new_blocks = self.blocks
        removed_blocks = []
        for b_id in block_ids:
            if not isinstance(b_id, int):
                return None
            for block in new_blocks:
                if b_id == block.id:
                    new_blocks.remove(block)
                    removed_blocks.append(block)
        if not bool(len(removed_blocks)):
            return None
        if as_dict:
            return [removed.get_dict() for removed in removed_blocks]
        else:
            return removed_blocks
        return None

    def add_block(self, block):
        if not self.check_instance(block, Block):
            return None
        self.blocks.append(block)

    def find_block(self, block_id, as_dict=False):
        for block in self.blocks:
            if block.id == block_id:
                if as_dict:
                    return block.get_dict()
                else:
                    return block
        return None
