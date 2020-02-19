from WithRepr import WithRepr
from WithStr import WithStr
from TypeControl import TypeControl
from Set import Set
from Block import Block
from KeyGenerator import KeyGenerator
import copy


class ArgumentException(Exception):
    pass


class Board(WithRepr, WithStr, TypeControl):
    _next_set_id = 1

    def __init__(self, sets=[], key_gen=KeyGenerator):
        self._key_gen = key_gen()
        self.state_id = self._key_gen.generate_key()
        self.sets = self.set_value(sets, Set)

    def get_dict(self):
        sets = [s.get_dict() for s in self.sets]
        board_dict = copy.deepcopy(self.__dict__)
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

    def _update_state_id(self):
        self.state_id = self._key_gen.generate_key()

    def find_blocks(self, *block_ids, set_id=None):
        blocks = []

        def _get_blocks(blocks_set, source=blocks, ids=block_ids):
            for b_id in ids:
                block = blocks_set.find_block(b_id)
                if self.check_instance(block, Block):
                    source.append(block)
        if isinstance(set_id, int):
            found_set = self.find_set(set_id)
            if not self.check_instance(found_set, Set):
                return None
            _get_blocks(found_set)
        else:
            for s in self.sets:
                _get_blocks(s)
        return blocks

    # actions: add/remove/replace

    def update_set(self, *blocks, action='add', set_id=None, block_ids=None, player=None):
        if not isinstance(set_id, int):
            return False
        updating_set = self.find_set(set_id)
        if not self.check_instance(updating_set, Set):
            return False
        if action == 'add':
            if not self.check_instance(blocks, Block):
                return False
            if not bool(updating_set.add_blocks(*blocks)):
                return False
        elif action == 'replace':
            if len(blocks) > 2:
                return False
            for block in blocks:
                if not bool(updating_set.replace_joker(block, player)):
                    return False
        elif action == 'remove':
            if isinstance(block_ids, (list, tuple)):
                ids = block_ids
            else:
                ids = []
                for block in blocks:
                    ids.append(block.id)
            if not bool(updating_set.remove_blocks(*ids)):
                return False
        else:
            raise ArgumentException(
                "Invalid argument in <Board>.update_set method: action can has value 'add' / 'remove' / 'replace'.")
        set_index = self.sets.index(updating_set)
        self.sets[set_index] = updating_set
        return True

    def set_sets(self, new_sets):
        sets = self.set_value(new_sets, Set)
        if not isinstance(self.sets, list) or not self.check_instance(sets, Set):
            return False
        return True

    def add_set(self, blocks, SetClass=Set):
        status = [None, False]
        if self.check_instance(blocks, Block) and isinstance(blocks, (list, tuple)) and len(blocks) >= 3:
            new_set = SetClass(self._next_set_id, blocks)
            if self.check_instance(new_set, Set):
                if bool(new_set.type):
                    self.sets.append(new_set)
                    status[0] = self._next_set_id
                    self._next_set_id += 1
                    status[1] = True
        print('status:', status)
        return status

    def remove_set(self, set_id):
        for s in self.sets:
            if s.id == set_id:
                self.sets.remove(s)
                return s
        return None
