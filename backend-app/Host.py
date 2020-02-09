from WithRepr import WithRepr
from WithStr import WithStr
from TypeControl import TypeControl
from Game import Game
from Player import Player
from Block import Block
from Set import Set


class SingletonException(Exception):
    pass


class Host(WithStr, WithRepr, TypeControl):
    _has_instance = False
    _next_game_id = 1

    def __init__(self):
        self._players_queue = []
        self._games = {}
        Host.add_instance()

    @staticmethod
    def add_instance():
        if Host._has_instance:
            raise SingletonException(
                ' <Host> class can has only one instance.')
        else:
            Host._has_instance = True

    def get_games(self, as_dict=False):
        if as_dict:
            games = {}
            for key in self._games.keys():
                games[key] = self._games[key].get_dict()
            return games
        return self._games

    def check_data(self, prev_state, board_id, player_key, game_key=None, target_game=None):
        data_status = None
        if isinstance(game_key, str):
            game = self.find_game(game_key)
        else:
            game = target_game
        if not self.check_instance(game, Game):
            return data_status
        data_status = {'gameIsChanged': game.check_game(prev_state), 'boardIsChanged': game.check_board(board_id), 'roundIsOngoing': game.check_round(
            player_key)}
        return data_status

    def menage_round(self, start=False, game_key=None, target_game=None):
        if isinstance(game_key, str):
            game = self.find_game(game_key)
        else:
            game = target_game
        if not self.check_instance(game, Game):
            return None
        return game.update_round_data(start)

    def _set_game_data(self, game):
        game_data = None
        if not self.check_instance(game, Game):
            return game_data
        has_password = bool(game._password)
        game_data = {
            'state': game.state,
            'hasPassword': has_password,
            'type': game.type,
            'key': game._key,
            'name': game.name,
            'slots': game.slots,
            'winner': game.winner,
            # 'boardId': game.board.state_id
        }
        game_data['playersData'] = [{'name': player.name, 'id': player.id, 'blocksQuantity': len(
            player.blocks)} for player in game.players]
        return game_data

    def get_player_data(self, target_player=None, player_key=None, player_id=None, game_key=None, target_game=None):
        if isinstance(game_key, str):
            game = self.find_game(game_key)
        else:
            game = target_game
        if not self.check_instance(game, Game):
            return None
        if isinstance(player_key, str):
            player = game.find_player(player_key=player_key)
        elif isinstance(player_id, int):
            player = game.find_player(player_id=player_id)
        else:
            player = target_player
            p_key = player.get_key()
        if not self.check_instance(player, Player):
            return None
        data = {
            'blocks': [],
            'id': player.id,
            'name': player.name,
            'type': player.type,
            'gameKey': player._game_key,
            'hasCleanSet': player.has_clean_set
        }
        if bool(player_key) or bool(p_key):
            data['playerKey'] = player.get_key()
            if game.state == 'run' and not player.got_blocks:
                data['blocks'].extend(self.get_player_blocks_data(player))
                player.got_blocks = True
        else:
            data['blockQuantity'] = len(player.blocks)
        return data

    def get_player_blocks_data(self, player):
        if not self.check_instance(player, Player):
            return None
        blocks = []
        for block in player.blocks:
            blocks.append(block.get_dict())
        return blocks

    def get_board_data(self, player_key, game_key=None, target_game=None):
        data = None
        if isinstance(game_key, str):
            game = self.find_game(game_key)
        else:
            game = target_game
        if not self.check_instance(game, Game) or not isinstance(player_key, str):
            return data
        game_has_player = False
        for key in game._players_queue:
            if key == player_key:
                game_has_player = True
                break
        if game_has_player:
            data = {'stateId': game.board.state_id, 'sets': []}
            for board_set in game.board.sets:
                dict_set = board_set.get_dict()
                data['sets'].append(dict_set)
        return data

    def get_round_data(self, player_key, game_key=None, target_game=None):
        data = None
        if isinstance(game_key, str):
            game = self.find_game(game_key)
        else:
            game = target_game
        if not self.check_instance(game, Game) or not isinstance(player_key, str):
            return data
        game_has_player = False
        for key in game._players_queue:
            if key == player_key:
                game_has_player = True
                break
        if game_has_player:
            data = game.round_data
        return data

    def get_games_data(self, player_key=None, game_key=None, target_game=None):
        if not isinstance(game_key, str) and not self.check_instance(target_game, Game):
            games_data = []
            for key in self._games:
                game = self._games[key]
                if self.check_instance(game, Game):
                    games_data.append(self._set_game_data(game))
            return games_data
        if bool(target_game):
            game = target_game
        elif isinstance(game_key, str):
            game = self.find_game(game_key)
        if not self.check_instance(game, Game):
            return None
        if not isinstance(player_key, str):
            return None
        player = game.find_player(player_key=player_key)
        if self.check_instance(player, Player):
            game_data = self._set_game_data(game)
            return game_data
        print(game.players[0]._key)
        return None

    def find_game(self, game_key, as_dict=False):
        found_game = None
        if not isinstance(game_key, str):
            return found_game
        found_game = self._games.get(game_key)
        if as_dict:
            return found_game.get_dict()
        return found_game

    def find_set(self, set_id, game_key):
        if not isinstance(set_id, int) or not isinstance(game_key, int):
            return None
        game = self.find_game(game_key)
        found_set = game.find_set(set_id)
        return found_set

    def update_board(self, game_key, *blocks_ids, target_set_id=None, replace=False):
        if not isinstance(game_key, str) or not isinstance(blocks_ids, (list, tuple)):
            return False
        game = self.find_game(game_key)
        if not self.check_instance(game, Game):
            return False
        blocks = game.get_blocks_from_all(*blocks_ids)
        if not bool(blocks):
            return False
        if not self.check_instance(blocks, Block):
            return False
        current_player_id = game.round_data['player_id']
        if replace and bool(target_set_id):
            if not bool(len(blocks)):
                return False
            rep_player = game.find_player(player_id=current_player_id)
            if not self.check_instance(rep_player, Player):
                return False
            replacers = blocks[:]
            is_replaced = game.board.update_set(
                *replacers, action="replace", set_id=target_set_id, player=rep_player)
            status = rep_player.remove_blocks(
                *[block.id for block in replacers])
            return is_replaced
        source_sets = {}
        source_player = {}
        has_own_block = False
        for block in blocks:
            if block.membership == 'set':
                if not has_own_block and block.player_id == current_player_id:
                    has_own_block = True
                if block.set_id not in source_sets:
                    source_sets[block.set_id] = [block]
                else:
                    source_sets[block.set_id].append(block)
            elif block.membership == 'player':
                if current_player_id != block.player_id:
                    return False
                has_own_block = True
                if block.player_id not in source_player:
                    source_player[block.player_id] = [block]
                else:
                    source_player[block.player_id].append(block)
            else:
                return False
        if not has_own_block:
            return False
        updating_blocks = []
        for key in source_sets.keys():
            updating_blocks += source_sets[key][:]
        if current_player_id in source_player:
            updating_blocks += [block for block in source_player[current_player_id]]
        if isinstance(target_set_id, int):
            is_added = game.board.update_set(
                *updating_blocks, action='add', set_id=target_set_id)
        else:
            status = game.board.add_set(updating_blocks)
            added_set_id = status[0]
            is_added = status[1]
        if not is_added:
            return False
        is_removed = False
        removed = {}
        for key in source_sets.keys():
            removed_blocks = source_sets[key][:]
            is_removed = game.board.update_set(
                *removed_blocks, action='remove', set_id=key)
            if is_removed:
                removed[key] = source_sets[key][:]
            else:
                for r_key in removed.keys():
                    game.board.update_set(
                        *removed[r_key], action='add', set_id=r_key)
                if isinstance(target_set_id, int):
                    game.board.update_set(
                        *updating_blocks, action='remove', set_id=target_set_id)
                else:
                    game.board.remove_set(added_set_id)
                is_removed = False
                break
        b_ids = [block.id for block in source_player[current_player_id]]
        is_removed = game.remove_player_blocks(
            current_player_id, b_ids)
        if not is_removed:
            game.add_player_blocks(
                current_player_id, source_player[current_player_id])
            return False
        game.board._update_state_id()
        return True

    def create_game(self, game_type, founder, name=None, password=None, slots=4, GameClass=Game):
        if not self.check_instance(founder, Player):
            return None
        if not bool(name):
            game_name = 'game-'
            game_name += str(self._next_game_id)
        elif isinstance(name, str):
            game_name = name
        else:
            return None
        game = Game(self._next_game_id, game_type,
                    founder, name=game_name, password=password, slots=slots)
        if not self.check_instance(game, Game):
            return None
        # self.add_game(game)
        return game

    def add_game(self, game):
        if not self.check_instance(game, Game):
            return False
        self._games[game.get_key()] = game
        self._next_game_id += 1
        return True

    def join_player(self, player, game_key=None, target_game=None, password=None):
        if self.check_instance(target_game, Game):
            game = target_game
            g_key = game.get_key()
        elif isinstance(game_key, str):
            game = self.find_game(game_key)
            g_key = game_key
        else:
            return None
        if not self.check_instance(game, Game) or not self.check_instance(player, Player):
            return None
        verified = True
        joined = False
        if bool(game._password):
            if game._password != password:
                verified = False
        if verified:
            joined = game.add_player(player)
        print('is ready: ', game.check_is_ready())
        if verified and joined and player.set_game_key(g_key) and game.check_is_ready():
            if game._update_to_ready():
                game.start_game()
        return {
            "verified": verified,
            "joined": joined,
            "state": game.state
        }

    def check_winner(self, game_key):
        game = self.find_game(game_key=game_key)
        if not self.check_instance(game, Game):
            return None
        return game.is_finished

    def remove_player(self, player_key, game_key):
        game = self._games[game_key]
        if not self.check_instance(game, Game):
            return False
        is_removed = game.remove_player(player_key)
        game._players_queue.remove(player_key)
        return is_removed

    def remove_game(self, game_key):
        if not isinstance(game_key, str):
            return False
        self._games.pop(game_key)
        return True

    def make_match(self):
        games = [self._games[key] for key in self._games.keys()]
        games.sort(key=lambda game: game.slots - len(games.players))
        for player in self._players_queue:
            is_matched = self.match_player(player, games[0])
            if len(games[0].players) == games[0].slots:
                games.remove(games[0])
        return is_matched

    def create_player(self, player_name, player_type='net', PlayerClass=Player):
        player = PlayerClass(player_name, player_type=player_type)
        if not self.check_instance(player, Player):
            return None
        return player

    def new_player(self, player_name, player_type='net', PlayerClass=Player):
        player = PlayerClass(player_name, player_type=player_type)
        if not self.check_instance(player, Player):
            return False
        self._players_queue.append(player)
        return True

    def match_player(self, player, game):
        if not self.check_instance(player, Player) or not self.check_instance(game, Game):
            return False
        adding_status = self.join_player(player, target_game=game)
        if adding_status[0] and adding_status[1]:
            return True
        return False
