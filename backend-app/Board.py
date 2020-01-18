from WithRepr import WithRepr
from WithStr import WithStr
from TypeControl import TypeControl
from Set import Set
from Block import Block


class ArgumentException(Exception):
    pass


class Board(WithRepr, WithStr, TypeControl):
    def __init__(self, sets=[]):
        self.sets = self.set_value(sets, Set)

    def get_dict(self):
        sets = [s.get_dict() for s in self.sets]
        board_dict = self.__dict__
        board_dict['sets'] = sets
        return board_dict

    def get_sets(self, as_dict=True):
        if as_dict:
            return [s.get_dict() for s in self.sets]
        else:
            return self.sets

    def find_set(self, set_id, as_dict=False):
        for s in self.sets:
            if s.id == set_id:
                if as_dict:
                    return s.get_dict()
                else:
                    return s
        return None

    def find_blocks(self, *block_ids, set_id=None, with_remove=False, as_dict=False):
        blocks = []

        def _get_blocks(blocks_set, ids=block_ids):
            for id in ids:
                block = blocks_set.find_block(id)
                if self.check_instance(block, Block):
                    blocks.append(block)
        if isinstance(set_id, int):
            found_set = self.find_set(set_id)
            if not self.check_instance(found_set, Set):
                return None
            _get_blocks(found_set)
        else:
            for s in self.sets:
                _get_blocks(s)
        if len(blocks) == len(block_ids):
            return blocks
        else:
            return None

    # actions: add/remove/replace
    def update_set(self, set_id, *blocks, action='add', block_ids=None, as_dict=False):
        if not isinstance(set_id, int):
            return None
        updating_set = self.find_set(set_id)
        if not self.check_instance(updating_set, Set):
            return None
        if action == 'add':
            if not self.check_instance(blocks, Block):
                return None
            updating_set.add_blocks(*blocks)
        elif action == 'replace':
            if len(blocks) > 2:
                return None
            for block in blocks:
                if not bool(updating_set.replace_joker(block)):
                    return None
        elif action == 'remove':
            if isinstance(block_ids, (list, tuple)):
                ids = block_ids
            else:
                ids = []
                for block in blocks:
                    ids.append(block.id)
            updating_set.remove_blocks(*ids)
        else:
            raise ArgumentException(
                "Invalid argument in <Board>.update_set method: action can has value 'add' / 'remove' / 'replace'.")
        set_index = self.sets.index(updating_set)
        self.sets[set_index] = updating_set
        if as_dict:
            return self.sets[set_index].get_dict()
        else:
            self.sets[set_index]

    def set_sets(self, new_sets, as_dict=False):
        self.sets = self.set_value(new_sets, Set)
        if as_dict:
            if self.sets:
                return self.get_sets()
            else:
                return self.set_sets

    def add_set(self, new_set):
        if self.check_instance(new_set, Set) and self.check_instance(new_set.blocks, Block):
            if bool(len(new_set.blocks)) and bool(new_set.type):
                self.sets.append(new_set)

    def remove_set(self, set_id):
        for s in self.sets:
            if s.id == set_id:
                self.sets.remove(s)
                return s
