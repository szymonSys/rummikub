from WithRepr import WithRepr
from WithStr import WithStr
from TypeControl import TypeControl
from Block import Block


class Set(WithRepr, WithStr, TypeControl):
    def __init__(self, set_id, blocks=[]):
        self.id = set_id
        self.is_full = False
        self.blocks = []
        self.type = self.add_blocks(*self.set_value(blocks, Block))

    def get_dict(self):
        blocks = [block.get_dict() for block in self.blocks]
        dict_set = self.__dict__
        dict_set['blocks'] = blocks
        return dict_set

    def get_blocks(self):
        return [block.get_dict() for block in self.blocks]

    def find_block(self, block_id, as_dict=False):
        for block in self.blocks:
            if block.id == block_id:
                if as_dict:
                    return block.get_dict()
                else:
                    return block
        return None

    def replace_joker(self, new_block):
        joker = None
        has_joker = False
        if(not self.check_instance(new_block, Block)):
            return joker
        for block in self.blocks:
            if block.value == 0:
                index = self.blocks.index(block)
                has_joker = True
                break
        if has_joker:
            for block in self.blocks:
                if new_block.color == block.color:
                    has_joker = False
                    break
        if self.blocks[0].value == 0 and self.blocks[1].value - new_block.value == 1 and new_block.color == self.blocks[0].color and not has_joker:
            has_joker = True
            index = 0
        elif self.blocks[len(self.blocks)-1].value == 0 and new_block.value - self.blocks[len(self.blocks)-2].value == 1 and new_block.color == self.blocks[len(self.blocks)-1].color and not has_joker:
            has_joker = True
            index = len(self.blocks)-1
        elif not has_joker:
            index = 1
            while index < len(self.blocks) - 1:
                if self.blocks[index].value == 0 and self.blocks[index+1].value - new_block.value == 1 and new_block.value - self.blocks[index-1].value == 1 and new_block.color == self.blocks[index - 1].color:
                    has_joker = True
                    break
                index += 1
        if has_joker:
            joker = self.blocks[index]
            new_block.set_id == self.id
            new_block.set_membership(set_id=self.id)
            self.blocks[index] = new_block
        return joker

    def check_type(self, blocks, length=0):
        if self.check_instance(blocks, Block):
            if (self._check_collection(blocks)):
                self.type = 'collection'
                return self.type
            if (self._check_series(blocks)):
                self.type = 'series'
                return self.type
            self.type = None
            return None

    def _check_series(self, blocks):
        if len(blocks) >= 3 and len(blocks) <= 13:
            zeroes_quantity = 0
            for block in blocks:
                if block.value > 0:
                    zeroes_quantity = blocks.index(block)
                    break
            i = zeroes_quantity
            while i < len(blocks) - 1:
                if blocks[i+1].value - blocks[i].value != 1 or blocks[i+1].color != blocks[i].color:
                    if blocks[i+1].value - blocks[i].value == 2:
                        if zeroes_quantity > 0:
                            removing = blocks[zeroes_quantity - 1]
                            blocks.remove(removing)
                            blocks.insert(i, removing)
                            zeroes_quantity -= 1
                        else:
                            return False
                    elif blocks[i+1].value - blocks[i].value > 2:
                        return False
                i += 1
            return True
        else:
            return False

    def _set_blocks_membership(self, blocks):
        for block in blocks:
            block.set_id = self.id
            block.set_membership(self.id)

    def _check_collection(self, blocks):
        if len(blocks) >= 3 and len(blocks) <= 4:
            colors = []
            for block in blocks:
                if block.color != 'purple':
                    colors.append(block.color)
            i = 0
            j = 1
            while i < len(colors):
                while j < len(colors):
                    if colors[i] == colors[j]:
                        return False
                    j += 1
                i += 1
            i = 0
            while i < len(blocks) - 1:
                if blocks[i+1].value != blocks[i].value and blocks[i].value != 0:
                    return False
                i += 1
            return True
        else:
            return False

    def set_type(self, blocks):
        self.type = self.check_type(blocks)
        return self.type

    def remove_blocks(self, *block_ids, as_dict=False):
        if len(self.blocks) - len(block_ids) < 3:
            return None
        new_blocks = self.blocks
        removed_blocks = []
        for b_id in block_ids:
            if not isinstance(b_id, int):
                return None
            for block in self.blocks:
                if b_id == block.id:
                    new_blocks.remove(block)
                    removed_blocks.append(block)
        if not bool(len(removed_blocks)):
            return None
        new_blocks_type = self.check_type(new_blocks)
        if new_blocks_type == 'series' or new_blocks_type == 'collection':
            self.is_full = False
            self.blocks = new_blocks
            # if len(removed_blocks) != len(block_ids):
            #     return None
            if as_dict:
                return [removed.get_dict() for removed in removed_blocks]
            else:
                return removed_blocks
        return None

    def add_blocks(self, *blocks, update=False):
        if self.is_full:
            print('set is full')
            return False
        blocks_list = list(blocks)
        if self.check_instance(blocks_list, Block):
            self._set_blocks_membership(blocks_list)
            blocks_list.extend(self.blocks)
            blocks_list.sort(key=lambda block: block.value)
            s_type = self.check_type(blocks_list, len(self.blocks))
            if(s_type == 'collection' or s_type == 'series'):
                self.blocks = blocks_list
            if (len(self.blocks) == 4 and s_type == 'collection') or (len(self.blocks) == 13 and s_type == 'series'):
                self.is_full = True
            return s_type
        else:
            return None
