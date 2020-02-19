import types
from WithRepr import WithRepr
from WithStr import WithStr
from TypeControl import TypeControl
from Block import Block
from KeyGenerator import KeyGenerator
import copy


class Player(WithRepr, WithStr, TypeControl):

    def __init__(self, name, player_type='net', key_generator=KeyGenerator.generate_key):
        self.id = None
        self.name = name
        self.type = player_type
        self.state = 'lobby'
        self.blocks = []
        self._game_key = None
        self._key = key_generator()
        self.has_clean_set = False
        self.got_blocks = False
        self.drew_block = False

    def get_dict(self):
        return copy.deepcopy(self.__dict__)

    def get_key(self):
        return self._key

    def get_game_key(self):
        return self._game_key

    def set_game_key(self, game_key):
        if not isinstance(game_key, str):
            return False
        self._game_key = game_key
        return True

    def change_to_game(self):
        self.state = 'game'
        return True

    def change_to_round(self):
        self.state = 'round'
        return True

    def change_to_win(self):
        self.state = 'win'

    def get_blocks(self):
        return [block.get_dict() for block in self.blocks]

    def remove_blocks(self, *blocks_ids, as_dict=False):
        if len(self.blocks) < len(blocks_ids):
            return None
        copied_blocks = self.blocks[:]
        removed_blocks = []
        for b_id in blocks_ids:
            if not isinstance(b_id, int):
                return None
            for block in copied_blocks:
                if b_id == block.id:
                    copied_blocks.remove(block)
                    removed_blocks.append(block)
        if not bool(len(removed_blocks)):
            return None
        self.blocks = copied_blocks
        if as_dict:
            return [removed.get_dict() for removed in removed_blocks]
        else:
            return removed_blocks
        return None

    def add_block(self, block):
        if not self.check_instance(block, Block):
            return None
        self.blocks.append(block)

    def add_blocks(self, blocks):
        if not self.check_instance(blocks, Block):
            return False
        for block in blocks:
            self.add_block(block)
        return True

    def find_block(self, block_id, as_dict=False):
        for block in self.blocks:
            if block.id == block_id:
                if as_dict:
                    return block.get_dict()
                else:
                    return block
        return None
