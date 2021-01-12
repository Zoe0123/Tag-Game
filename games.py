"""CSC148 Assignment 2 - Tag You're It!

=== CSC148 Summer 2019 ===
Department of Computer Science,
University of Toronto
"""
from __future__ import annotations
import random
from typing import Dict, Union, Optional
from players import Player
from trees import QuadTree, TwoDTree


class Game:
    """ A class for a game.

    This is an abstract class. No instance should be raised.
    """

    def handle_collision(self, player1: str, player2: str) -> None:
        """ Perform some action when <player1> and <player2> collide """
        raise NotImplementedError

    def check_for_winner(self) -> Optional[str]:
        """ Return the name of the player or group of players that have
        won the game, or None if no player has won yet """
        raise NotImplementedError


class Tag(Game):
    """The class for game tag.

    In this game there is one player who is ‘it’. Every other player should
    try to avoid the player who is ‘it’. The player who is ‘it’ should try to
    tag any other player by colliding with them.
    After _duration seconds have passed, any player who is not currently ‘it’
    but has been tagged is eliminated until only the winner is left.

    === Public Attributes ===
    field: the game field represented by either a QuadTree or a TwoDTree.

    === Private Attribute ===
    _players: a dictionary with the name of the players being the key and the
    <Player> instances being the value.
    _it: the name of the player who is currently 'it'.
    _duration: the duration of the game.

    === Representation Invariants ===
    - The player who is ‘it’ should be purple, all other players should be
    green.
    - All fields will have a north-west corner at (0, 0) and a south-east corner
     at (500, 500).
    - <duration> must be a non-negative integer.
    """
    _players: Dict[str, Player]
    field: Union[QuadTree, TwoDTree]
    _it: str
    _duration: int

    def __init__(self, n_players: int,
                 field_type: Union[QuadTree, TwoDTree],
                 duration: int,
                 max_speed: int,
                 max_vision: int) -> None:
        """ Initialize this tag game.

        === Precondition ===
        - <field_type> should be a tree that have its nw corner at (0, 0)
        and se corner at (500, 500).
        - <duration> is a non-negative integer
        - <max_speed> and <max_vision> are non-negative integers.

        >>> tag = Tag(5, QuadTree((250, 250)), 5, 8, 6)
        >>> len(tag.__getattribute__('_players')) == 5
        True
        """
        self._players = {}
        self._duration = duration
        self.field = field_type
        self._it = 'p0'
        point = random.randint(0, 500), random.randint(0, 500)
        it = Player('p0', random.randint(0, max_vision),
                    random.randint(1, max_speed), self, 'purple', point)
        self.field.insert('p0', point)
        self._players['p0'] = it
        for i in range(1, n_players):
            point = random.randint(0, 500), random.randint(0, 500)
            if not self.field.contains_point(point):
                name = 'p' + str(i)
                player = Player(name, random.randint(0, max_vision),
                                random.randint(1, max_speed), self, 'green',
                                point)
                player.select_enemy('p0')
                it.select_target(name)
                self._players[name] = player
                self.field.insert(name, point)

    def handle_collision(self, player1: str, player2: str) -> None:
        """ Perform some action when <player1> and <player2> collide.

        When <player1> and <player2> collide, both players reverse the
        direction they are moving in. If one of the players is ‘it’, the other
        player becomes ‘it’ and its points increase by 1.

        === Precondition ===
        - <player1> and <player2> are in self._players

        >>> tag = Tag(5, QuadTree((250, 250)), 2, 8, 6)
        >>> tag.handle_collision('p0', 'p1')
        >>> tag.__getattribute__('_it')
        'p1'
        >>> tag.__getattribute__('_players')['p1'].get_points() > 0
        True
        """
        p1, p2 = self._players[player1], self._players[player2]
        p1.reverse_direction()
        p2.reverse_direction()
        if self._it == player1:
            self._it = player2
            p2.increase_points(1)
            p2.set_colour('purple')
            for player in self._players:
                if player != player2:
                    p2.select_target(player)
                    self._players[player].select_enemy(player2)
                if player != player1:
                    p1.ignore_target(player)
                    self._players[player].ignore_enemy(player1)
            p1.set_colour('green')
        elif self._it == player2:
            self._it = player1
            p1.increase_points(1)
            p1.set_colour('purple')
            for player in self._players:
                if player != player1:
                    p1.select_target(player)
                    self._players[player].select_enemy(player1)
                if player != player2:
                    p2.ignore_target(player)
                    self._players[player].ignore_enemy(player2)
            p2.set_colour('green')
            p2.select_enemy(player1)

    def check_for_winner(self) -> Optional[str]:
        """ Return the name of the player that have won the game, or None if no
        player has won yet.
        If more than 2 players left, all players who are not ‘it’ with at least
        1 point are removed  from the _players dictionary.
        if there is one player left, that player is the winner
        if there are two players left, the player that isn’t ‘it’ is the winner.

        === Precondition ===
        - self._players is not empty.

        >>> tag = Tag(5, QuadTree((250, 250)), 5, 8, 6)
        >>> tag.handle_collision('p0', 'p1')
        >>> tag.handle_collision('p1', 'p2')
        >>> tag.handle_collision('p2', 'p3')
        >>> tag.check_for_winner()
        >>> 'p1' in tag.__getattribute__('_players')
        False
        >>> len(tag.__getattribute__('_players'))
        3
        >>> tag.handle_collision('p3', 'p0')
        >>> tag.check_for_winner()
        >>> tag.handle_collision('p0', 'p4')
        >>> tag.check_for_winner()
        'p0'
        """
        if len(self._players) > 2:
            to_del = []
            for player in self._players:
                if self._players[player].get_points() >= 1 and \
                        self._it != player:
                    to_del.append(player)
                    self.field.remove(player)
                    self._players[self._it].ignore_target(player)
            for player in to_del:
                del self._players[player]
        elif len(self._players) == 2:
            for player in self._players:
                if player != self._it:
                    return player
        else:
            p = None
            for player in self._players:
                p = player
            return p


class ZombieTag(Game):
    """ A class for zombie tag game.
    In this game, one person starts out as a zombie and everyone else starts out
     as a human. All zombies try to chase humans and convert them into zombies.
    All humans try to avoid the zombies and not get converted. At the end of
    the game, if there are any humans left, the humans win. Otherwise the
    zombies win.

    === Public Attributes ===
    field: the game field represented by either a QuadTree or a TwoDTree.

    === Private Attribute ===
    _humans: a dictionary with the name of the human players being the key and
    the <Player> instances being the value.
    _zombies: a dictionary with the name of the zombie players being the key and
    the <Player> instances being the value.
    _duration: the duration of the game.

    === Representation Invariants ===
    - All zombies should be purple, all humans should be green.
    - All fields will have a north-west corner at (0, 0) and a south-east corner
     at (500, 500).
     - <duration> must be a non-negative integer.
    """
    _humans: Dict[str, Player]
    _zombies: Dict[str, Player]
    field: Union[QuadTree, TwoDTree]
    _duration: int

    def __init__(self, n_players: int,
                 field_type: Union[QuadTree, TwoDTree],
                 duration: int,
                 max_speed: int,
                 max_vision: int) -> None:
        """ Initialize this zombie tag game.

        === Precondition ===
        - <field_type> should be a tree that have its nw corner at (0, 0)
        and se corner at (500, 500).
        - <duration> is a non-negative integer
        - <max_speed> and <max_vision> are non-negative integers.

        >>> zombie_tag = ZombieTag(5, QuadTree((250, 250)), 5, 8, 6)
        >>> len(zombie_tag.__getattribute__('_humans')) == 5
        True
        """
        self._humans = {}
        self._zombies = {}
        self.field = field_type
        self._duration = duration
        point = random.randint(0, 500), random.randint(0, 500)
        it = Player('p0', max_vision, 1, self, 'purple', point)
        self.field.insert('p0', point)
        self._zombies['p0'] = it
        for i in range(1, n_players + 1):
            point = random.randint(0, 500), random.randint(0, 500)
            if not self.field.contains_point(point):
                name = 'p' + str(i)
                player = Player(name, random.randint(0, max_vision),
                                random.randint(1, max_speed), self, 'green',
                                point)
                player.select_enemy('p0')
                it.select_target(name)
                self._humans[name] = player
                self.field.insert(name, point)

    def handle_collision(self, player1: str, player2: str) -> None:
        """ Perform some action when <player1> and <player2> collide.

        Both players should reverse the direction they are moving in.
        if one player is a zombie and the other is a human, the human
        becomes a zombie.

        === Precondition ===
        - player1 and player2 are in either self._humans or self._zombies

        >>> zombie_tag = ZombieTag(4, QuadTree((250, 250)), 5, 8, 6)
        >>> zombie_tag.handle_collision('p0', 'p1')
        >>> len(zombie_tag.__getattribute__('_zombies')) == 2
        True
        >>> len(zombie_tag.__getattribute__('_humans')) == 3
        True
        """
        if player1 in self._zombies and player2 in self._humans:
            p1, p2 = self._zombies[player1], self._humans[player2]
            p1.reverse_direction()
            p2.reverse_direction()
            p2.set_colour('purple')
            p2.set_speed(1)
            for zombie in self._zombies:
                p2.ignore_enemy(zombie)
                self._zombies[zombie].ignore_target(player2)
            self._zombies[player2] = p2
            del self._humans[player2]
            for human in self._humans:
                self._humans[human].select_enemy(player2)
                p2.select_target(human)
        elif player2 in self._zombies and player1 in self._humans:
            p1, p2 = self._humans[player1], self._zombies[player2]
            p2.reverse_direction()
            p1.reverse_direction()
            p1.set_colour('purple')
            p1.set_speed(1)
            for zombie in self._zombies:
                p1.ignore_enemy(zombie)
                self._zombies[zombie].ignore_target(player1)
            self._zombies[player1] = p1
            del self._humans[player1]
            for human in self._humans:
                self._humans[human].select_enemy(player1)
                p1.select_target(human)
        elif player1 in self._zombies and player2 in self._zombies:
            self._zombies[player1].reverse_direction()
            self._zombies[player2].reverse_direction()
        else:
            self._humans[player1].reverse_direction()
            self._humans[player2].reverse_direction()

    def check_for_winner(self) -> Optional[str]:
        """ Return the group of players (i.e. humans or zombies) that have won
        the game, if there are any humans left, humans win, otherwise, zombies
        win.

        >>> zombie_tag = ZombieTag(1, QuadTree((250, 250)), 5, 8, 6)
        >>> zombie_tag.check_for_winner()
        'humans'
        >>> zombie_tag.handle_collision('p0', 'p1')
        >>> zombie_tag.check_for_winner()
        'zombies'
        """
        if self._humans:
            return 'humans'
        else:
            return 'zombies'


class EliminationTag(Game):
    """ A class for the game elimination tag.
    Every player has exactly one other player they are trying to tag.
    Once a player tags their target, their target is eliminated and they now try
    to tag their target’s target.

    When there is eventually only two players left, the winner is decided as the
    player who has eliminated the most other players. If both players have
    eliminated the same number, the game ends in a tie.

    === Public Attributes ===
    field: the game field represented by either a QuadTree or a TwoDTree.

    === Private Attribute ===
    _players: a dictionary with the name of the players being the key and
    the <Player> instances being the value.

    === Representation Invariants ===
    - Every players is randomly coloured.
    - All fields will have a north-west corner at (0, 0) and a south-east corner
     at (500, 500).
    """
    _players: Dict[str, Player]
    field: Union[QuadTree, TwoDTree]

    def __init__(self, n_players: int,
                 field_type: Union[QuadTree, TwoDTree],
                 max_speed: int,
                 max_vision: int) -> None:
        """Initialize this elimination tag game.

        === Precondition ===
        - <field_type> should be a tree that have its nw corner at (0, 0)
        and se corner at (500, 500).
        - <duration> is a non-negative integer
        - <max_speed> and <max_vision> are non-negative integers.

        >>> e_tag = EliminationTag(5, QuadTree((250, 250)), 5, 8)
        >>> len(e_tag.__getattribute__('_players')) == 5
        True
        """
        self._players = {}
        self.field = field_type
        point0 = random.randint(0, 500), random.randint(0, 500)
        p0 = Player('p0', random.randint(0, max_vision),
                    random.randint(1, max_speed), self, 'random', point0)
        self.field.insert('p0', point0)
        self._players['p0'] = p0
        p0.select_enemy('p' + str(n_players - 1))
        p0.select_target('p1')
        point_n = random.randint(0, 500), random.randint(0, 500)
        while point_n == point0:
            point_n = random.randint(0, 500), random.randint(0, 500)
        n_name = 'p' + str(n_players - 1)
        pn = Player(n_name, random.randint(0, max_vision),
                    random.randint(1, max_speed), self, 'random', point_n)
        self.field.insert(n_name, point_n)
        self._players[n_name] = pn
        pn.select_target('p0')
        pn.select_enemy('p' + str(n_players - 2))
        for i in range(1, n_players - 1):
            point = random.randint(0, 500), random.randint(0, 500)
            if not self.field.contains_point(point):
                name = 'p' + str(i)
                player = Player(name, random.randint(0, max_vision),
                                random.randint(1, max_speed), self, 'random',
                                point)
                player.select_enemy('p' + str(i - 1))
                player.select_target('p' + str(i + 1))
                self._players[name] = player
                self.field.insert(name, point)

    def handle_collision(self, player1: str, player2: str) -> None:
        """ Perform some action when <player1> and <player2> collide.
        Both players reverses the direction they are moving in.
        If neither player is the other’s target: both players reverses the
        direction they are moving in.
        if player B is the target of player A: player B’s target becomes player
        A’s target, eliminate player B and increase player A’s points by 1.

        === Precondition ===
        - player1 and player2 are in self._players

        >>> e_tag = EliminationTag(5, QuadTree((250, 250)), 5, 8)
        >>> t1 = e_tag.__getattribute__('_players')['p1'].get_targets()
        >>> e_tag.handle_collision('p0', 'p1')
        >>> t0 = e_tag.__getattribute__('_players')['p0'].get_targets()
        >>> 'p1' in e_tag.__getattribute__('_players')
        False
        >>> t0 == t1
        True
        """
        p1 = self._players[player1]
        p2 = self._players[player2]
        if player2 in p1.get_targets():
            p1.ignore_target(player2)
            new_target = p2.get_targets()[0]
            p1.select_target(new_target)
            self._players[new_target].ignore_enemy(player2)
            self._players[new_target].select_enemy(player1)
            del self._players[player2]
            self.field.remove(player2)
            p1.increase_points(1)
        elif player1 in p2.get_targets():
            p2.ignore_target(player1)
            new_target = p1.get_targets()[0]
            p2.select_target(new_target)
            self._players[new_target].ignore_enemy(player1)
            self._players[new_target].select_enemy(player2)
            del self._players[player1]
            self.field.remove(player1)
            p2.increase_points(1)
        else:
            p1.reverse_direction()
            p2.reverse_direction()

    def check_for_winner(self) -> Optional[str]:
        """ Return the name of the player that have won the game, or None if no
        player has won yet.
        Return the name of the player with the most points.
        if there are multiple players tied for most points, return None.

        >>> e_tag = EliminationTag(5, QuadTree((250, 250)), 5, 8)
        >>> e_tag.handle_collision('p0', 'p1')
        >>> e_tag.handle_collision('p0', 'p2')
        >>> e_tag.handle_collision('p3', 'p4')
        >>> e_tag.check_for_winner()
        'p0'
        """
        point = 0
        winner = []
        for player in self._players:
            point1 = self._players[player].get_points()
            if point1 > point:
                winner = [player]
                point = point1
            elif point1 == point:
                winner.append(player)
        if len(winner) == 1:
            return winner[0]


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(
        config={'extra-imports': ['random', 'typing', 'players', 'trees'],
                'disable': ['R0913', 'R0902', 'W0611', 'R1710', 'R1702']})
