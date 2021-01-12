"""CSC148 Assignment 2 - Tag You're It!

=== CSC148 Summer 2019 ===
Department of Computer Science,
University of Toronto
"""
from __future__ import annotations
import random
from typing import List, Tuple, Optional, Set
from trees import OutOfBoundsError


class Player:
    """ A class for players.

    === Private Attribute ===
    _name: The name of the player
    _location: The current location of the player on the field
    _color: The colour used to draw the player object
    _vision: The distance a player can see in any direction
    _speed: The number of steps a player can move in a single turn
    _game: A reference to an instance of a Game class
    _points: The number of points the player has
    _targets: A list of player names that this player should move towards
    _enemies: A list of player names that this player should avoid
    _direction: A string indicating the direction the player is currently moving

    === Representation Invariants ===
    - The _location of a player must fall within the boundaries set by the
    _game.field attribute
    - _vision, _points and _speed must be positive or zero
    - The _colour attribute must be one of purple, green, or random
    - _points should be zero immediately after the class is initialized
    - No string that appears in _targets should also appear in _enemies
    - No string that appears in _enemies should also appear in _targets
    - _direction should be one of ('N', 'S', 'E', 'W')
    - When implementing these methods, if one of the representation invariants
    would be violated, methods should always fail silently.
    """
    _name: str
    _location: Tuple[int, int]
    _colour: str
    _vision: int
    _speed: int
    _game: 'Game'
    _points: int
    _targets: List[str]
    _enemies: List[str]
    _direction: str

    def __init__(self, name: str, vision: int, speed: int, game: 'Game',
                 colour: str, location: Tuple[int, int]) -> None:
        """ Initialize this player.

        >>> player = Player('p0', 3, 1, 'Game (a valid game class)',\
        'purple', (50, 100))

        """
        self._name = name
        self._location = location
        self._colour = colour
        self._vision = vision
        self._speed = speed
        self._game = game
        self._points = 0
        self._targets = []
        self._enemies = []
        self._direction = random.choice(('N', 'S', 'E', 'W'))

    def set_colour(self, colour: str) -> None:
        """ Change the colour of self

        >>> player = Player('p0', 3, 1, 'Game (a valid game class)',\
        'purple', (50, 100))
        >>> player._colour
        'purple'
        >>> player.set_colour('green')
        >>> player._colour
        'green'
        """
        self._colour = colour

    def increase_points(self, points: int) -> None:
        """ Increase <self>'s points by <points>.

        === Precondition ===
        - <points> must be a non-negative integer.

        >>> player = Player('p0', 3, 1, 'Game (a valid game class)',\
        'purple', (50, 100))
        >>> player.get_points()
        0
        >>> player.increase_points(1)
        >>> player.get_points()
        1
        """
        self._points += points

    def get_points(self) -> int:
        """ Return the number of points <self> currently has.

        >>> player = Player('p0', 3, 1, 'Game (a valid game class)',\
        'purple', (50, 100))
        >>> player.get_points()
        0
        >>> player.increase_points(1)
        >>> player.get_points()
        1
        """
        return self._points

    def select_target(self, name: str) -> None:
        """ Add a target to <self>'s target list.

        === Precondition ===
        - Name should not be in self._targets

        >>> player = Player('p0', 3, 1, 'Game (a valid game class)',\
        'purple', (50, 100))
        >>> player.select_target('p1')
        >>> player.get_targets()
        ['p1']
        """
        if name not in self._targets:
            self._targets.append(name)

    def ignore_target(self, name: str) -> None:
        """ Remove a target from <self>'s target list

        === Precondition ===
        - Name should be in self._targets

        >>> player = Player('p0', 3, 1, 'Game (a valid game class)',\
        'purple', (50, 100))
        >>> player.select_target('p1')
        >>> player.ignore_target('p1')
        >>> player.get_targets()
        []
        """
        if name in self._targets:
            self._targets.remove(name)

    def get_targets(self) -> List[str]:
        """ Return a copy of the list of target names.

        >>> player = Player('p0', 3, 1, 'Game (a valid game class)',\
        'purple', (50, 100))
        >>> player.get_targets()
        []
        >>> player.select_target('p1')
        >>> player.get_targets()
        ['p1']
        """
        return self._targets[:]

    def select_enemy(self, name: str) -> None:
        """ Add an enemy to <self>'s target list.

        === Precondition ===
        - name should not be in self._enemies

        >>> player = Player('p0', 3, 1, 'Game (a valid game class)',\
        'purple', (50, 100))
        >>> player.select_enemy('p1')
        >>> player.get_enemies()
        ['p1']
        """
        if name not in self._enemies:
            self._enemies.append(name)

    def ignore_enemy(self, name: str) -> None:
        """ Remove an enemy from <self>'s enemy list

        === Precondition ===
        - name should be in self._enemies

        >>> player = Player('p0', 3, 1, 'Game (a valid game class)',\
        'purple', (50, 100))
        >>> player.select_enemy('p1')
        >>> player.ignore_enemy('p1')
        >>> player.get_enemies()
        []
        """
        if name in self._enemies:
            self._enemies.remove(name)

    def get_enemies(self) -> List[str]:
        """ Return a copy of the list of enemy names.

        >>> player = Player('p0', 3, 1, 'Game (a valid game class)',\
        'purple', (50, 100))
        >>> player.get_enemies()
        []
        >>> player.select_enemy('p1')
        >>> player.get_enemies()
        ['p1']
        """
        return self._enemies[:]

    def reverse_direction(self) -> None:
        """ Update the direction so that <self> will move in the opposite
        direction.

        >>> player = Player('p0', 3, 1, 'Game (a valid game class)',\
        'purple', (50, 100))
        >>> player.__setattr__('_direction', 'N')
        >>> player.reverse_direction()
        >>> player.__getattribute__('_direction') == 'S'
        True
        """
        if self._direction == 'N':
            self._direction = 'S'
        elif self._direction == 'S':
            self._direction = 'N'
        elif self._direction == 'E':
            self._direction = 'W'
        else:
            self._direction = 'E'

    def set_speed(self, speed: int) -> None:
        """ Update <self>'s speed to <speed>

        === Precondition ===
        - <speed> must be a non-negative integer.

        >>> player = Player('p0', 3, 1, 'Game (a valid game class)',\
        'purple', (50, 100))
        >>> player.set_speed(5)
        >>> player.__getattribute__('_speed')
        5
        """
        self._speed = speed

    def next_direction(self) -> Set[str]:
        """ Update the direction to move the next time self.move is called. This
        direction should be determined by the relative number of visible targets
        and enemies.
        This function considers the number of targets this player is moving
        towards and the number of enemies this player is moving away from and
        determines the direction to move towards most targets and away from most
        enemies.

        Return a set of all equally good directions to move towards.
        This method should call the names_in_range Tree method exactly twice.
        This method should set self._direction to a subset of:
        ('N', 'S', 'E', 'W')

        >>> player = Player('p0', 3, 1, 'Game (a valid game class)',\
        'purple', (50, 100))
        # Assume there are 2 targets and 3 enemies in the NE direction;
        # Assume there is 1 target and 2 enemies in the SE direction.
        # Assume <player> randomly chose to look in <'NE'> and <'SE'>
        >>> player.next_direction()
        {'W'}
        >>> player.__getattribute__('_direction')
        'W'
        """
        nw = []
        ne = []
        sw = []
        se = []
        directions = random.sample(['NE', 'SE', 'NE', 'SW'], 2)
        if 'NW' in directions:
            nw.extend(self._game.field.names_in_range(self._location, 'NW',
                                                      self._vision))
        if 'NE' in directions:
            ne.extend(self._game.field.names_in_range(self._location, 'NE',
                                                      self._vision))
        if 'SW' in directions:
            sw.extend(self._game.field.names_in_range(self._location, 'SW',
                                                      self._vision))
        if 'SE' in directions:
            se.extend(self._game.field.names_in_range(self._location, 'SE',
                                                      self._vision))
        n, w, s, e = self._help_next(nw, ne, sw, se)
        result = []
        if n == max(n, w, s, e):
            result.append('N')
        if w == max(n, w, s, e):
            result.append('W')
        if s == max(n, w, s, e):
            result.append('S')
        if e == max(n, w, s, e):
            result.append('E')
        self._direction = random.choice(result)
        return set(result)

    def _help_next(self, nw: List[str], ne: List[str], sw: List[str],
                   se: List[str]) -> tuple:
        """ Split the self.next_direction function. This function evaluates
        the score to move in each directins.
        """
        n = 0
        w = 0
        s = 0
        e = 0
        for name in nw:
            if name in self._enemies:
                s += 1
                e += 1
            if name in self._targets:
                n += 1
                w += 1
        for name in ne:
            if name in self._enemies:
                s += 1
                w += 1
            if name in self._targets:
                n += 1
                e += 1
        for name in sw:
            if name in self._enemies:
                n += 1
                e += 1
            if name in self._targets:
                s += 1
                w += 1
        for name in se:
            if name in self._enemies:
                n += 1
                w += 1
            if name in self._targets:
                s += 1
                e += 1
        return n, w, s, e

    def move(self) -> None:
        """ Move <self> in the direction described by self._direction by the
        number of steps described by self._speed. Make sure to keep track of the
        updated location of self.
        If the movement would move self out of bounds, move self in the opposite
        direction instead. self should continue to move in this new direction
        until next_direction is called again.

        >>> player = Player('p0', 3, 1, 'Game (a valid game class)',\
        'purple', (50, 100))
        >>> player.move()
        >>> loc = player.__getattribute__('_location')
        >>> loc in [(51, 100), (49, 100), (50, 101), (50, 99)]
        True
        """
        try:
            loc = self._game.field.move_point(
                self._location, self._direction, self._speed)
            if loc is not None:
                self._location = loc
        except OutOfBoundsError:
            self.reverse_direction()


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(
        config={'extra-imports': ['typing', 'random', 'games', 'trees'],
                'disable': ['R0913', 'R0902', 'W0611', 'R1710', 'R1702']})
