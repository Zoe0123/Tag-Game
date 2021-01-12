import pytest
from typing import Tuple, List
import trees
import players
import games

##### TREES #####

class TreesTest:
    def test_contains(self):
        self.tree.insert('jon', (250, 250))
        assert 'jon' in self.tree
        assert 'joe' not in self.tree

    def test_tree_contains_point(self):
        self.tree.insert('jon', (250, 250))
        assert self.tree.contains_point((250, 250))
        assert not self.tree.contains_point((250, 251))

    def test_insert_out_of_bounds(self):
        try:
            self.tree.insert('jon', (501, 250))
        except trees.OutOfBoundsError:
            return
        raise Exception('this should have raised an OutOfBoundsError')

    def test_insert_collision(self):
        self.tree.insert('jon', (250, 250))
        try:
            self.tree.insert('jon', (250, 250))
        except trees.OutOfBoundsError:
            return
        raise Exception('this should have raised an OutOfBoundsError')

    def test_remove(self):
        self.tree.insert('jon', (250, 250))
        self.tree.remove('buddy')
        assert 'jon' in self.tree
        self.tree.remove('jon')
        assert 'jon' not in self.tree

    def test_remove_point(self):
        self.tree.insert('jon', (250, 250))
        self.tree.remove_point((250, 251))
        assert 'jon' in self.tree
        self.tree.remove_point((250, 250))
        assert 'jon' not in self.tree

    def test_move(self):
        self.tree.insert('jon', (250, 250))
        self.tree.move('jon', 'N', 10)
        assert self.tree.contains_point((250, 240))

    def test_move_collision(self):
        self.tree.insert('jon', (250, 250))
        self.tree.insert('joe', (250, 240))
        try:
            self.tree.move('jon', 'N', 10)
        except trees.OutOfBoundsError:
            return
        raise Exception('this should have raised an OutOfBoundsError')

    def test_move_out_of_bounds(self):
        self.tree.insert('jon', (250, 250))
        try:
            self.tree.move('jon', 'E', 251)
        except trees.OutOfBoundsError:
            return
        raise Exception('this should have raised an OutOfBoundsError')

    def test_move_point(self):
        self.tree.insert('jon', (250, 250))
        self.tree.move_point((250, 250), 'N', 10)
        assert self.tree.contains_point((250, 240))

    def test_move_point_collision(self):
        self.tree.insert('jon', (250, 250))
        self.tree.insert('joe', (250, 240))
        try:
            self.tree.move_point((250, 250), 'N', 10)
        except trees.OutOfBoundsError:
            return
        raise Exception('this should have raised an OutOfBoundsError')

    def test_move_point_out_of_bounds(self):
        self.tree.insert('jon', (250, 250))
        try:
            self.tree.move_point((250, 250), 'E', 251)
        except trees.OutOfBoundsError:
            return
        raise Exception('this should have raised an OutOfBoundsError')

    def test_names_in_range(self):
        self.tree.insert('jon', (250, 250))
        self.tree.insert('joe', (300, 300))
        assert set(self.tree.names_in_range((200, 200), 'SE', 150)) == {'jon', 'joe'}
        assert set(self.tree.names_in_range((350, 350), 'NW', 150)) == {'jon', 'joe'}
        assert set(self.tree.names_in_range((0, 500), 'NE', 1000)) == {'jon', 'joe'}
        assert set(self.tree.names_in_range((200, 200), 'SE', 90)) == {'jon'}
        assert set(self.tree.names_in_range((350, 350), 'NW', 90)) == {'joe'}
        assert len(self.tree.names_in_range((350, 350), 'NW', 10)) == 0

    def test_is_empty(self):
        assert self.tree.is_empty()
        self.tree.insert('jon', (250, 250))
        assert not self.tree.is_empty()

    def test_is_leaf(self):
        assert self.tree.is_leaf()
        self.tree.insert('jon', (250, 250))
        assert self.tree.is_leaf()
        self.tree.insert('joe', (300, 300))
        assert not self.tree.is_leaf()

class TestQuadTree(TreesTest):
    def setup_method(self):
        self.tree = trees.QuadTree((250, 250))

    def test_height(self):
        assert self.tree.height() == 1
        self.tree.insert('jon', (250, 250))
        assert self.tree.height() == 1
        self.tree.insert('joe', (300, 300))
        assert self.tree.height() == 2
        self.tree.insert('job', (50, 50))
        assert self.tree.height() == 3

    def test_depth(self):
        self.tree.insert('jon', (250, 250))
        self.tree.insert('joe', (300, 300))
        self.tree.insert('job', (50, 50))
        jon = self.tree._nw._se
        joe = self.tree._se
        job = self.tree._nw._nw
        assert self.tree.depth(jon) == 2
        assert self.tree.depth(joe) == 1
        assert jon.depth(job) is None
        assert self.tree.depth(self.tree) is None

class Test2DTree(TreesTest):
    def setup_method(self):
        self.tree = trees.TwoDTree((0, 0), (500, 500))

    def test_height(self):
        assert self.tree.height() == 1
        self.tree.insert('jon', (250, 250))
        assert self.tree.height() == 1
        self.tree.insert('joe', (300, 300))
        assert self.tree.height() == 2
        self.tree.insert('job', (50, 50))
        assert self.tree.height() == 2

    def test_depth(self):
        self.tree.insert('jon', (250, 250))
        self.tree.insert('joe', (300, 300))
        self.tree.insert('job', (50, 50))
        self.tree.insert('minnie_mouse', (50, 100))
        jon = self.tree
        joe = self.tree._gt
        job = self.tree._lt
        minnie = job._gt
        assert jon.depth(jon) is None
        assert joe.depth(minnie) is None
        assert jon.depth(minnie) == 2
        assert job.depth(minnie) == 1

##### PLAYERS #####

class PlayersTest:
    def test_init(self):
        player = players.Player('eric', 1, 2, self.game, 'green', (100, 100))
        assert player._name == 'eric'
        assert player._vision == 1
        assert player._speed == 2
        assert player._game == self.game
        assert player._colour == 'green'
        assert player._location == (100, 100)
        assert player._points == 0
        assert player._targets == []
        assert player._enemies == []
        assert player._direction in 'NSEW'

    def test_set_colour(self):
        player = players.Player('eric', 1, 2, self.game, 'green', (100, 100))
        player.set_colour('purple')
        assert player._colour == 'purple'

    def test_increase_points(self):
        player = players.Player('eric', 1, 2, self.game, 'green', (100, 100))
        points = player._points
        player.increase_points(20)
        assert points + 20 == player._points

    def test_get_points(self):
        player = players.Player('eric', 1, 2, self.game, 'green', (100, 100))
        player._points = 33
        assert player.get_points() == 33

    def test_select_target(self):
        player = players.Player('eric', 1, 2, self.game, 'green', (100, 100))
        targets = set(player._targets)
        player.select_target('morton')
        assert set(player._targets) - targets == {'morton'}

    def test_ignore_target(self):
        player = players.Player('eric', 1, 2, self.game, 'green', (100, 100))
        player._targets = ['gill', 'eoin']
        player.ignore_target('gill')
        assert player._targets == ['eoin']

    def test_get_targets(self):
        player = players.Player('eric', 1, 2, self.game, 'green', (100, 100))
        player._targets = ['gill', 'eoin']
        assert set(player.get_targets()) == {'gill', 'eoin'}

    def test_select_enemy(self):
        player = players.Player('eric', 1, 2, self.game, 'green', (100, 100))
        enemies = set(player._enemies)
        player.select_enemy('morton')
        assert set(player._enemies) - enemies == {'morton'}

    def test_ignore_enemy(self):
        player = players.Player('eric', 1, 2, self.game, 'green', (100, 100))
        player._enemies = ['gill', 'eoin']
        player.ignore_enemy('gill')
        assert player._enemies == ['eoin']

    def test_get_enemies(self):
        player = players.Player('eric', 1, 2, self.game, 'green', (100, 100))
        player._enemies = ['gill', 'eoin']
        assert set(player.get_enemies()) == {'gill', 'eoin'}

    def test_reverse_direction(self):
        player = players.Player('eric', 1, 2, self.game, 'green', (100, 100))
        dirs = 'NSNEWE'
        direction = player._direction
        player.reverse_direction()
        assert player._direction == dirs[dirs.index(direction) + 1]

    def test_set_speed(self):
        player = players.Player('eric', 1, 2, self.game, 'green', (100, 100))
        player.set_speed(1)
        assert player._speed == 1

    def _reset_player(self, player: players.Player, loc: Tuple[int, int]):
        player._location = loc
        player._targets = []
        player._enemies = []
        player._vision = 100
        self.game.field.remove(player._name)
        self.game.field.insert(player._name, loc)

    def _move_into_starting_position(self,
                                     coords: List[Tuple[int, int]],
                                     targets: List[int],
                                     enemies: List[int]) -> Tuple[players.Player, List[players.Player]]:
        player, *others = self.game._players.values()
        self._reset_player(player, (250, 250))
        for i, (coord, other) in enumerate(zip(coords, others)):
            self._reset_player(other, coord)
            if i in targets:
                player._targets.append(other._name)
            if i in enemies:
                player._enemies.append(other._name)
        return player, others

    def test_next_direction_no_best(self):
        coords = [(50, 50), (50, 450), (450, 450), (450, 50)]
        targets = []
        enemies = []
        player, _ = self._move_into_starting_position(coords, targets, enemies)
        assert player.next_direction() == set('NSEW')
        assert player._direction in set('NSEW')

    def test_move_no_collision(self):
        coords = [(50, 50), (50, 450), (450, 450), (450, 50)]
        targets = []
        enemies = []
        player, _ = self._move_into_starting_position(coords, targets, enemies)
        player._speed = 10
        player._direction = 'E'
        player.move()
        assert player._location == (260, 250)

    def test_move_collision(self):
        coords = [(260, 250), (50, 450), (450, 450), (450, 50)]
        targets = []
        enemies = []
        player, others = self._move_into_starting_position(coords, targets, enemies)
        player._speed = 10
        player._direction = 'E'
        player.move()
        assert player._location == (250, 250)
        assert player._direction == 'W'

    def test_move_out_of_bounds(self):
        coords = [(50, 50), (50, 450), (450, 450), (450, 50)]
        targets = []
        enemies = []
        player, _ = self._move_into_starting_position(coords, targets, enemies)
        player._speed = 500
        player._direction = 'E'
        player.move()
        assert player._location == (250, 250)
        assert player._direction == 'W'

class TestPlayersQuadTree(PlayersTest):
    def setup_method(self):
        self.game = games.Tag(5, trees.QuadTree((250, 250)), 5, 3, 4)

class TestPlayers2DTree(PlayersTest):
    def setup_method(self):
        self.game = games.Tag(5, trees.TwoDTree((0, 0), (500, 500)), 5, 3, 4)

##### GAMES #####

### TAG ###

class TagTests:
    def test_init(self):
        game = games.Tag(10, self.tree, 5, 3, 4)
        assert len(game._players) == 10
        assert all(name in game.field for name in game._players)
        assert game._it in game._players
        assert game._players[game._it]._colour == 'purple'

    def test_handle_collision_reverse_direction(self):
        game = games.Tag(10, self.tree, 5, 3, 4)
        player1, player2 = list(game._players.values())[:2]
        dir1, dir2 = player1._direction, player2._direction
        game.handle_collision(player1._name, player2._name)
        assert dir1 != player1._direction
        assert dir2 != player2._direction

    def test_handle_collision_one_is_it(self):
        game = games.Tag(10, self.tree, 5, 3, 4)
        it = game._it
        it_points = game._players[it].get_points()
        not_it = next(p for p in game._players if p != game._it)
        game.handle_collision(it, not_it)
        assert game._it == not_it
        assert it_points + 1 == game._players[game._it].get_points()

    def test_check_for_winner_no_winner(self):
        game = games.Tag(10, self.tree, 5, 3, 4)
        assert game.check_for_winner() is None

    def test_check_for_winner_one_left(self):
        game = games.Tag(1, self.tree, 5, 3, 4)
        assert game.check_for_winner() == list(game._players)[0]

    def test_check_for_winner_two_left(self):
        game = games.Tag(2, self.tree, 5, 3, 4)
        winner = next(p for p in game._players if p != game._it)
        assert game.check_for_winner() == winner

class TestTagQuadTree(TagTests):
    def setup_method(self):
        self.tree = trees.QuadTree((250, 250))

class TestTag2dTree(TagTests):
    def setup_method(self):
        self.tree = trees.TwoDTree((0, 0), (500, 500))

### ZOMBIE TAG ###

class ZombieTagTests:
    def test_init(self):
        game = games.ZombieTag(10, self.tree, 5, 3, 4)
        assert len(game._humans) == 10
        assert all(name in game.field for name in game._zombies)
        assert all(name in game.field for name in game._humans)
        assert len(game._zombies.keys() & game._humans.keys()) == 0
        assert all(player._colour == 'green' for _, player in game._humans.items())
        assert len(game._zombies) == 1
        assert game._zombies.popitem()[1]._colour == 'purple'

    def test_handle_collision_reverse_direction(self):
        game = games.ZombieTag(10, self.tree, 5, 3, 4)
        player1, player2 = list(game._humans.values())[:2]
        dir1, dir2 = player1._direction, player2._direction
        game.handle_collision(player1._name, player2._name)
        assert dir1 != player1._direction
        assert dir2 != player2._direction

    def test_handle_collision_zombie_attack(self):
        game = games.ZombieTag(10, self.tree, 5, 3, 4)
        human = list(game._humans.values())[0]
        zombie = list(game._zombies.values())[0]
        game.handle_collision(human._name, zombie._name)
        assert zombie._name in game._zombies
        assert human._name in game._zombies
        assert human._name not in game._humans

    def test_check_for_winner_humans_win(self):
        game = games.ZombieTag(2, self.tree, 5, 3, 4)
        assert game.check_for_winner() == 'humans'

    def test_check_for_winner_zombies_win(self):
        game = games.ZombieTag(1, self.tree, 5, 3, 4)
        human = list(game._humans.values())[0]
        zombie = list(game._zombies.values())[0]
        game.handle_collision(human._name, zombie._name)
        assert game.check_for_winner() == 'zombies'

class TestZombieTagQuadTree(ZombieTagTests):
    def setup_method(self):
        self.tree = trees.QuadTree((250, 250))

class TestZombieTag2dTree(ZombieTagTests):
    def setup_method(self):
        self.tree = trees.TwoDTree((0, 0), (500, 500))

### ELIMINATION TAG ###

class EliminationTagTests:
    def test_init(self):
        game = games.EliminationTag(10, self.tree, 3, 4)
        assert len(game._players) == 10
        assert all(name in game.field for name in game._players)
        assert all(player._colour == 'random' for _, player in game._players.items())
        player = list(game._players.values())[0]
        players = set()
        while player not in players:
            players.add(player)
            player = game._players[player.get_targets()[0]]
        # check to make sure that all players are targeting each other correctly
        assert len(players) == 10

    def test_handle_collision_do_not_eliminate(self):
        game = games.EliminationTag(10, self.tree, 3, 4)
        player1 = list(game._players)[0]
        player2 = next(name for name, p in game._players.items() if player1 not in p.get_targets())
        dir1 = game._players[player1]._direction
        dir2 = game._players[player2]._direction
        game.handle_collision(player1, player2)
        assert player1 in game._players
        assert player2 in game._players

    def test_handle_collision_one_is_target(self):
        game = games.EliminationTag(10, self.tree, 3, 4)
        player1 = list(game._players)[0]
        player2 = game._players[player1].get_targets()[0]
        p2targets = game._players[player2].get_targets()
        points = game._players[player1].get_points()
        game.handle_collision(player1, player2)
        assert player1 in game._players
        assert player2 not in game._players
        assert game._players[player1].get_targets()[0] == p2targets[0]
        assert game._players[player1].get_points() - 1 == points

    def test_check_for_winner_no_winner(self):
        game = games.EliminationTag(10, self.tree, 3, 4)
        assert game.check_for_winner() is None

    def test_check_for_winner_one_winner(self):
        game = games.EliminationTag(10, self.tree, 3, 4)
        player1 = list(game._players)[0]
        game._players[player1].increase_points(1)
        assert game.check_for_winner() == player1

class TestEliminationTagQuadTree(EliminationTagTests):
    def setup_method(self):
        self.tree = trees.QuadTree((250, 250))

class TestEliminationTag2dTree(EliminationTagTests):
    def setup_method(self):
        self.tree = trees.TwoDTree((0, 0), (500, 500))

if __name__ == '__main__':
    pytest.main(['tests.py'])
