"""CSC148 Assignment 2 - Tag You're It!

=== CSC148 Summer 2019 ===
Department of Computer Science,
University of Toronto
"""
from __future__ import annotations
from typing import Optional, List, Tuple, Dict


class OutOfBoundsError(Exception):
    """
    An Exception class describes the OutOfBoundsError.  The OutOfBoundsError is
    raised to interrupt the code when the client try to let a point out of
    bound or create duplicate points.
    """
    pass


class Tree:
    """
    A tree to keep track of the positions of the players on the field.

    This is an abstract class. Only subclasses should be instantiated.

    === Representation Invariants ===
    - When a method takes a name or point argument, if a player
    with that name or at that point does not exist in the tree, the method
    fail silently without making any changes to the tree.
    - Each tree represents a rectangle.
    - If a node X is a child of another node Y, the subtree with X as its root
    describes a rectangle that is completely contained by the rectangle
    described by the tree with Y as its root.
    - if two nodes are children of the same parent, the rectangles described by
    their subtrees do not overlap.
    """

    def __contains__(self, name: str) -> bool:
        """ Return True if a player named <name> is stored in this tree.

        Runtime: O(n)
        """
        raise NotImplementedError

    def contains_point(self, point: Tuple[int, int]) -> bool:
        """ Return True if a player at location <point> is stored in this tree.

        Runtime: O(log(n))
        """
        raise NotImplementedError

    def insert(self, name: str, point: Tuple[int, int]) -> None:
        """Insert a player named <name> into this tree at point <point>.

        Raise an OutOfBoundsError if <point> is out of bounds.

        Raise an OutOfBoundsError if moving the player would place the player at
        exactly the same coordinates of another player in the Tree (before
        moving the player).

        Runtime: O(log(n))
        """
        raise NotImplementedError

    def remove(self, name: str) -> None:
        """ Remove information about a player named <name> from this tree.

        if a player with the <name> does not exist in the tree, the method
        fail silently without making any changes to the tree.

        Runtime: O(n)
        """
        raise NotImplementedError

    def remove_point(self, point: Tuple[int, int]) -> None:
        """ Remove information about a player at point <point> from this tree.

        if a player with at the <point> does not exist in the tree, the method
        fail silently without making any changes to the tree.

        Runtime: O(log(n))
        """
        raise NotImplementedError

    def move(self, name: str, direction: str, steps: int) -> \
            Optional[Tuple[int, int]]:
        """ Return the new location of the player named <name> after moving it
        in the given <direction> by <steps> steps.

        if a player with the <name> does not exist in the tree, the method
        fail silently without making any changes to the tree.

        Raise an OutOfBoundsError if this would move the player named
        <name> out of bounds (before moving the player).

        Raise an OutOfBoundsError if moving the player would place the player at
        exactly the same coordinates of another player in the Tree (before
        moving the player).

        Runtime: O(n)

        === precondition ===
        direction in ['N', 'S', 'E', 'W']
        """
        raise NotImplementedError

    def move_point(self, point: Tuple[int, int], direction: str, steps: int) \
            -> Optional[Tuple[int, int]]:
        """ Return the new location of the player at point <point> after moving
        it in the given <direction> by <steps> steps.

        if a player with at the <point> does not exist in the tree, the method
        fail silently without making any changes to the tree.

        Raise an OutOfBoundsError if this would move the player at point
        <point> out of bounds (before moving the player).

        Raise an OutOfBoundsError if moving the player would place the player at
        exactly the same coordinates of another player in the Tree (before
        moving the player).

        Moving a point may require the tree to be reorganized. This method
        should do the minimum amount of tree reorganization possible to move the
        given point properly. (if the new point will be added to the same node
        that the old point removed from, change the _point attribute of this
        node directly.)

        Runtime: O(log(n))

        === precondition ===
        direction in ['N', 'S', 'E', 'W']

        """
        raise NotImplementedError

    def names_in_range(self, point: Tuple[int, int], direction: str,
                       distance: int) -> List[str]:
        """ Return a list of names of players whose location is in the
        <direction> relative to <point> and whose location is within <distance>
        along both the x and y axis.

        For example: names_in_range((100, 100), 'SE', 10) should return the
        names of all the players south east of (100, 100) and within 10 steps in
        either direction.
        In other words, find all players whose location is in the box with
        corners at (include corner points): (100, 100) (110, 100) (100, 110)
        (110, 110)

        Runtime: faster than O(n) when distance is small(Only check the
        subtrees which the box included.)

        === precondition ===
        direction in ['NE', 'SE', 'NE', 'SW']
        """
        raise NotImplementedError

    def size(self) -> int:
        """ Return the number of nodes in <self>. For an empty tree, it still
        has size of 1.

        Runtime: O(n)
        """
        raise NotImplementedError

    def height(self) -> int:
        """ Return the height of <self>

        Height is measured as the number of nodes in the path from the root of
        this tree to the node at the greatest depth in this tree.

        Runtime: O(n)
        """
        raise NotImplementedError

    def depth(self, tree: Tree) -> Optional[int]:
        """ Return the depth of the subtree <tree> relative to <self>. Return
        None if <tree> is not a descendant of <self> and <tree> is <self>.

        Runtime: O(log(n))
        """
        raise NotImplementedError

    def is_leaf(self) -> bool:
        """ Return True if <self> has no children

        Runtime: O(1)
        """
        raise NotImplementedError

    def is_empty(self) -> bool:
        """ Return True if <self> or any of its descendants do not store any
        information about the location of any players.

        Runtime: O(1)
        """
        raise NotImplementedError


class QuadTree(Tree):
    """
    A tree storing positional information of players, and divides a rectangle
    into four equally sized sub-rectangles.

    === Private Attributes ===
    _center: the x/y coordinates describing the centre point of this rectangle
    _name: the name of a player
    _point: the x/y coordinates of the player
    _ne: a quad-tree that represents the north-east quadrant of the current
    rectangle, or None if this quadrant doesn't contain any point.
    _nw: a quad-tree that represents the north-west quadrant of the current
    rectangle, or None if this quadrant doesn't contain any point.
    _se: a quad-tree that represents the south_east quadrant of the current
    rectangle, or None if this quadrant doesn't contain any point.
    _sw: a quad-tree that represents the south-west quadrant of the current
    rectangle, or None if this quadrant doesn't contain any point.

    === Representation Invariants ===
    - only leaf nodes can have a non-None _name and _point attribute
    - every leaf node must have a non-None _name and _point attribute unless
    it also has no parents
    - every non-None _point and _center attribute must contain integers >= 0.
    - if the exact centre of rectangle is not an integer, the values in _centre
    should be rounded down to the nearest integer.
    - if _point is not None, then _point[0] <= 2*_centre[0], and _point[1] <=
    2*_centre[1]
    - if d._point is not None for some descendant d of p, then:
    d must be in the _nw or _sw subtrees if d._point[0] <= p._centre[0]
    and in one of the other subtrees otherwise.
    d must be in the _nw or _ne subtrees if d._point[1] <= p._centre[1]
    and in one of the other subtrees otherwise.
    """
    _centre: Tuple[int, int]
    _name: Optional[str]
    _point: Optional[Tuple[int, int]]
    _ne: Optional[QuadTree]
    _nw: Optional[QuadTree]
    _se: Optional[QuadTree]
    _sw: Optional[QuadTree]

    def __init__(self, centre: Tuple[int, int]) -> None:
        """Initialize this QuadTree instance.

        === Precondition ===
        - <centre> must contain only positive integers or zero.

        >>> tree = QuadTree((100, 100))
        >>> tree.__getattribute__('_centre') == (100, 100)
        True
        >>> tree.is_empty()
        True

        Runtime: O(1)
        """
        self._centre = int(centre[0]), int(centre[1])
        self._name = None
        self._point = None
        self._ne = None
        self._nw = None
        self._se = None
        self._sw = None

    def __contains__(self, name: str) -> bool:
        """ Return True if a player named <name> is stored in this tree.

        >>> tree = QuadTree((100, 100))
        >>> tree.insert('a', (150, 150))
        >>> 'a' in tree
        True

        Runtime: O(n)
        """
        if self._name == name:
            return True
        elif self._ne and name in self._ne:
            return True
        elif self._nw and name in self._nw:
            return True
        elif self._se and name in self._se:
            return True
        elif self._sw and name in self._sw:
            return True
        else:
            return False

    def contains_point(self, point: Tuple[int, int]) -> bool:
        """ Return True if a player at location <point> is stored in this tree.

        >>> tree = QuadTree((100, 100))
        >>> tree.insert('a', (150, 150))
        >>> tree.contains_point((150, 150))
        True

        Runtime: O(log(n))
        """
        x, y = self._centre
        x1, y1 = point
        if self.is_empty():
            return False
        elif self._point == point:
            return True
        elif x1 < 0 or y1 < 0 or x1 > 2 * x or y1 > 2 * y:
            return False
        else:
            subtree = self._point_position(point)[0]
            if subtree and subtree.contains_point(point):
                return True
            else:
                return False

    def _point_position(self, point: Tuple[int, int]) -> Tuple[QuadTree, str]:
        """ Return the subtree in the direction that <point> is in.

        Runtime: O(log(n))
        """
        x, y = self._centre
        x1, y1 = point
        if x1 <= x and y1 <= y:
            return self._nw, 'nw'
        elif x1 > x and y1 <= y:
            return self._ne, 'ne'
        elif x1 <= x and y1 > y:
            return self._sw, 'sw'
        else:
            return self._se, 'se'

    def insert(self, name: str, point: Tuple[int, int]) -> None:
        """Insert a player named <name> into this tree at point <point>. This
        point is inserted to a leaf node in this tree.

        Raise an OutOfBoundsError if <point> is out of bounds.

        Raise an OutOfBoundsError if moving the player would place the player
        at exactly the same coordinates of another player in the Tree (before
        moving the player).

        Runtime: O(log(n))
        >>> tree = QuadTree((100, 100))
        >>> tree.insert('a', (90, 90))
        >>> tree.insert('b', (150, 150))
        >>> 'a' in tree and 'b' in tree
        True
        >>> tree.contains_point((90, 90)) and tree.contains_point((150, 150))
        True
        >>> tree.__getattribute__('_nw') is not None
        True
        >>> tree.__getattribute__('_se') is not None
        True
        """
        x, y = self._centre
        x1, y1 = point
        if x1 > 2 * x or y1 > 2 * y or x1 < 0 or y1 < 0 or \
                self.contains_point(point):
            raise OutOfBoundsError
        self._help_insert(point, (0, 0), name)

    def _help_insert(self, point: Tuple[int, int], o_point: Tuple[int, int],
                     name: str) -> None:
        """
        Insert a player named <name> into this tree at point <point>, and this
        tree has original point at <o_point>.
        === Precondition ===
        - The point <point> is in bound
        - The point <point> is not in this tree before insert.
        """
        x0, y0 = o_point
        x, y = self._centre
        if self.is_empty():
            self._name, self._point = name, point
        elif self.is_leaf():
            self._help_insert1(self._point, (x0, y0), self._name)
            self._name, self._point = None, None
            self._help_insert(point, (x0, y0), name)
        else:
            subtree, pos = self._point_position(point)
            if subtree:
                if pos == 'nw':
                    subtree._help_insert(point, (x0, y0), name)
                elif pos == 'ne':
                    subtree._help_insert(point, (x, y0), name)
                elif pos == 'sw':
                    subtree._help_insert(point, (x0, y), name)
                else:
                    subtree._help_insert(point, (x, y), name)
            else:
                self._help_insert1(point, (x0, y0), name)

    def _help_insert1(self, point: Tuple[int, int], o_point: Tuple[int, int],
                      name: str) -> None:
        """
        Insert a player named <name> into this tree at point <point>,  this tree
        has original point at <o_point> and we need to build a new subtree
        before adding this point.

        === Precondition ===
        - The point <point> is in bound
        - The point <point> is not in this tree before insert.
        """
        x0, y0 = o_point
        x, y = self._centre
        x1, y1 = point
        length_x = x - x0
        length_y = y - y0
        if length_x < 2:
            length_x = 2
        if length_y < 2:
            length_y = 2
        if x1 <= x and y1 <= y:
            self._nw = QuadTree((int(1 / 2 * length_x) + x0,
                                 int(1 / 2 * length_y) + y0))
            self._nw._point = x1, y1
            self._nw._name = name
        elif x1 <= x and y < y1:
            self._sw = QuadTree((int(1 / 2 * length_x) + x0,
                                 int(3 / 2 * length_y) + y0))
            self._sw._point = x1, y1
            self._sw._name = name
        elif x < x1 and y1 <= y:
            self._ne = QuadTree((int(3 / 2 * length_x) + x0,
                                 int(1 / 2 * length_y) + y0))
            self._ne._point = x1, y1
            self._ne._name = name
        else:
            self._se = QuadTree((int(3 / 2 * length_x) + x0,
                                 int(3 / 2 * length_y) + y0))
            self._se._point = x1, y1
            self._se._name = name

    def remove(self, name: str) -> None:
        """ Remove information about a player named <name> from this tree.
        if self contains a tree with only one leaf subtree, the name
        and point of this subtree is promoted to the parent node.
        if a player with the name <name> does not exist in the tree, the method
        fail silently without making any changes to the tree.

        Runtime: O(n)

        >>> tree = QuadTree((100, 100))
        >>> tree.insert('a', (90, 90))
        >>> tree.insert('b', (150, 150))
        >>> 'a' in tree
        True
        >>> tree.remove('a')
        >>> 'a' in tree
        False
        >>> tree.contains_point((90, 90))
        False
        >>> 'b' in tree
        True
        >>> tree.is_leaf()
        True
        """
        if self._name == name:
            self._name, self._point = None, None
        elif self._nw and name in self._nw:
            self._nw.remove(name)
            if self._nw.is_empty():
                self._nw = None
            self._check_one_child()
        elif self._sw and name in self._sw:
            self._sw.remove(name)
            if self._sw.is_empty():
                self._sw = None
            self._check_one_child()
        elif self._ne and name in self._ne:
            self._ne.remove(name)
            if self._ne.is_empty():
                self._ne = None
            self._check_one_child()
        else:
            if self._se:
                self._se.remove(name)
                if self._se.is_empty():
                    self._se = None
                self._check_one_child()

    def _check_one_child(self) -> None:
        """
        Check if self only has one leaf subtree, and promote the name and point
        of this subtree to the parent node, then change this subtree to None.
        """
        if self._nw and self._nw.is_leaf() and not self._sw and not self._ne \
                and not self._se:
            self._name, self._point = self._nw._name, self._nw._point
            self._nw = None
        elif self._sw and self._sw.is_leaf() and not self._nw and not self._ne \
                and not self._se:
            self._name, self._point = self._sw._name, self._sw._point
            self._sw = None
        elif self._ne and self._ne.is_leaf() and not self._sw and not self._nw \
                and not self._se:
            self._name, self._point = self._ne._name, self._ne._point
            self._ne = None
        else:
            if self._se and self._se.is_leaf() and not self._sw and not \
                    self._ne and not self._nw:
                self._name, self._point = self._se._name, self._se._point
                self._se = None

    def remove_point(self, point: Tuple[int, int]) -> None:
        """ Remove information about a player at point <point> from this tree.
        if self contains a tree with only one leaf subtree, the name
        and point of this subtree is promoted to the parent node.
        if a player with at that point does not exist in the tree, the method
        fail silently without making any changes to the tree.

        Runtime: O(log(n))
        >>> tree = QuadTree((100, 100))
        >>> tree.insert('a', (90, 90))
        >>> tree.insert('b', (150, 150))
        >>> tree.contains_point((150, 150))
        True
        >>> tree.remove_point((150, 150))
        >>> tree.contains_point((150, 150))
        False
        >>> 'b' in tree
        False
        >>> 'a' in tree
        True
        >>> tree.is_leaf()
        True
        """
        x, y = self._centre
        x1, y1 = point
        if self._point == point:
            self._name, self._point = None, None
        elif 0 <= x1 <= 2 * x and 0 <= y1 <= 2 * y:
            if x1 <= x and y1 <= y and self._nw and \
                    self._nw.contains_point(point):
                self._nw.remove_point(point)
                if self._nw.is_empty():
                    self._nw = None
                self._check_one_child()
            elif x1 <= x and y < y1 and self._sw and \
                    self._sw.contains_point(point):
                self._sw.remove_point(point)
                if self._sw.is_empty():
                    self._sw = None
                self._check_one_child()
            elif x < x1 and y1 <= y and self._ne and \
                    self._ne.contains_point(point):
                self._ne.remove_point(point)
                if self._ne.is_empty():
                    self._ne = None
                self._check_one_child()
            else:
                if self._se and self._se.contains_point(point):
                    self._se.remove_point(point)
                    if self._se.is_empty():
                        self._se = None
                    self._check_one_child()

    def move(self, name: str, direction: str, steps: int) -> \
            Optional[Tuple[int, int]]:
        """ Return the new location of the player named <name> after moving it
        in the given <direction> by <steps> steps.
        if a player with the <name> does not exist in the tree, the method
        fail silently without making any changes to the tree.

        Raise an OutOfBoundsError if this would move the player named
        <name> out of bounds (before moving the player).

        Raise an OutOfBoundsError if moving the player would place the player
        at exactly the same coordinates of another player in the Tree (before
        moving the player).

        Runtime: O(n)

        === precondition ===
        direction in ['N', 'S', 'E', 'W']

        >>> tree = QuadTree((100, 100))
        >>> tree.insert('a', (90, 90))
        >>> tree.insert('b', (150, 150))
        >>> 'a' in tree
        True
        >>> tree.move('a', 'S', 15)
        (90, 105)
        >>> 'a' in tree
        True
        >>> tree.contains_point((90, 105))
        True
        >>> tree.__getattribute__('_sw') is not None
        True
        >>> tree.__getattribute__('_nw') is None
        True
        """
        if name in self:
            x0, y0 = self._find_point(name)
            if steps == 0:
                return x0, y0
            if direction == 'N':
                y0 -= steps
            elif direction == 'S':
                y0 += steps
            elif direction == 'E':
                x0 += steps
            else:
                x0 -= steps
            x, y = self._centre
            if x0 > 2 * x or y0 > 2 * y or x0 < 0 or y0 < 0 \
                    or self.contains_point((x0, y0)):
                raise OutOfBoundsError
            self.remove(name)
            self.insert(name, (x0, y0))
            return x0, y0

    def _find_point(self, name: str) -> Tuple[int, int]:
        """
        Return the point of the player with the name <name> located at in this
        tree.

        === precondition ===
        - <name> is in this tree.
        """
        if self.is_leaf():
            return self._point
        elif self._nw and name in self._nw:
            return self._nw._find_point(name)
        elif self._sw and name in self._sw:
            return self._sw._find_point(name)
        elif self._ne and name in self._ne:
            return self._ne._find_point(name)
        else:
            return self._se._find_point(name)

    def move_point(self, point: Tuple[int, int], direction: str, steps: int) \
            -> Optional[Tuple[int, int]]:
        """ Return the new location of the player at point <point> after moving
        it in the given <direction> by <steps> steps.
        if a player with at the <point> does not exist in the tree, the method
        fail silently without making any changes to the tree.

        Raise an OutOfBoundsError if this would move the player at point
        <point> out of bounds (before moving the player).
        Raise an OutOfBoundsError if moving the player would place the player at
        exactly the same coordinates of another player in the Tree (before
        moving the player).

        Moving a point may require the tree to be reorganized. This method
        should do the minimum amount of tree reorganization possible to move
        the given point properly. (if the new point will be added to the same
        node that the old point removed from, change the _point attribute of
        this node directly.)

        Runtime: O(log(n))

        === precondition ===
        direction in ['N', 'S', 'E', 'W']

        >>> tree = QuadTree((100, 100))
        >>> tree.insert('a', (90, 90))
        >>> tree.insert('b', (150, 150))
        >>> 'b' in tree
        True
        >>> tree.move_point((150, 150), 'N', 55)
        (150, 95)
        >>> 'b' in tree
        True
        >>> tree.contains_point((150, 95))
        True
        >>> tree.__getattribute__('_ne') is not None
        True
        >>> tree.__getattribute__('_se') is None
        True
        """
        if self.contains_point(point):
            x0, y0 = point
            if steps == 0:
                return point
            if direction == 'N':
                y0 -= steps
            elif direction == 'S':
                y0 += steps
            elif direction == 'E':
                x0 += steps
            else:
                x0 -= steps
            x, y = self._centre
            if x0 > 2 * x or y0 > 2 * y or x0 < 0 or y0 < 0 \
                    or self.contains_point((x0, y0)):
                raise OutOfBoundsError
            point_tree = self._find_point_tree(point)
            name = point_tree._name
            if self._check_bound(point_tree, (x0, y0)):
                point_tree._point = x0, y0
            else:
                self.remove_point(point)
                self.insert(name, (x0, y0))
            return x0, y0

    def _find_point_tree(self, point: Tuple[int, int]) -> QuadTree:
        """ Return a leaf QuadTree within self that the point <point> is
        located at.

        === Precondition ===
        - The point <point> is in self.

        Runtime: O(log(n))
        """
        sub = self._point_position(point)[0]
        if sub is None:
            return self
        else:
            return sub._find_point_tree(point)

    def _check_bound(self, tree: QuadTree, point: Tuple[int, int]) -> bool:
        """ Return True if <point> is within the bound of the <tree>.

        === Precondition ===
        - <tree> is a subtree of self.
        - This function is only to be called on the root QuadTree.

        Runtime: O(log(n))
        """
        dep = self.depth(tree)
        if dep is not None:
            length = self._centre[0] // 2 ** dep
            return (tree._centre[0] - length < point[0] <= tree._centre[
                0] + length
                    and tree._centre[1] - length < point[1] <=
                    tree._centre[1] + length)
        else:
            return 0 < point[0] <= tree._centre[0] * 2 and 0 < point[1] <= \
                   tree._centre[1] * 2

    def names_in_range(self, point: Tuple[int, int], direction: str,
                       distance: int) -> List[str]:
        """ Return a list of names of players whose location is in the
        <direction> relative to <point> and whose location is within <distance>
        along both the x and y axis.

        For example: names_in_range((100, 100), 'SE', 10) should return the
        names of all the players south east of (100, 100) and within 10 steps in
        either direction.
        In other words, find all players whose location is in the box with
        corners at (include corner points): (100, 100) (110, 100) (100, 110)
        (110, 110).

        Runtime: faster than O(n) when distance is small (Only check the
        subtrees which the box included.)

        === precondition ===
        direction in ['NE', 'SE', 'NE', 'SW']

        >>> tree = QuadTree((100, 100))
        >>> tree.insert('a', (90, 90))
        >>> tree.insert('b', (120, 120))
        >>> tree.names_in_range((80, 80), 'SE', 50)
        ['a', 'b']
        """
        if self.is_empty():
            return []
        else:
            x0, y0 = point
            a, b = self._centre
            if direction == 'NW':
                x = max(x0 - distance, 0)
                y = max(y0 - distance, 0)
            elif direction == 'SW':
                x = max(x0 - distance, 0)
                y = min(y0 + distance, 2 * b)
            elif direction == 'NE':
                x = min(x0 + distance, 2 * a)
                y = max(y0 - distance, 0)
            else:
                x = min(x0 + distance, 2 * a)
                y = min(y0 + distance, 2 * b)
            left, top, right, bottom = min(x0, x), min(y0, y), max(x0, x), max(
                y0, y)
            return self._name_in_range(left, top, right, bottom)

    def _name_in_range(self, left: int, top: int, right: int,
                       bottom: int) -> List[str]:
        """ Return a list of names that is within the frame constructed by the
        four boundaries <left>, <top>, <right>, <bottom>. Only check the
        subtrees which the frame included.

        === Precondition ===
        - This function is only to be called on the root QuadTree.
        """
        lst = []
        if self.is_leaf():
            if left <= self._point[0] <= right and \
                    top <= self._point[1] <= bottom:
                return [self._name]
        else:
            a, b = self._centre
            if a >= left and b >= top and self._nw:
                lst.extend(self._nw._name_in_range(left, top, right, bottom))
            if a <= right and b >= top and self._ne:
                lst.extend(self._ne._name_in_range(left, top, right, bottom))
            if a >= left and b <= bottom and self._sw:
                lst.extend(self._sw._name_in_range(left, top, right, bottom))
            if a <= right and b <= bottom and self._se:
                lst.extend(self._se._name_in_range(left, top, right, bottom))
        return lst

    def size(self) -> int:
        """ Return the number of nodes in <self>. For an empty tree, it still
        has size of 1.

        Runtime: O(n)

        >>> tree = QuadTree((100, 100))
        >>> tree.size()
        1
        >>> tree.insert('a', (90, 90))
        >>> tree.insert('b', (120, 120))
        >>> tree.size()
        3
        """
        if self.is_leaf():
            return 1
        else:
            size = 1
            if self._nw:
                size += self._nw.size()
            if self._sw:
                size += self._sw.size()
            if self._ne:
                size += self._ne.size()
            if self._se:
                size += self._se.size()
            return size

    def height(self) -> int:
        """ Return the height of <self>

        Height is measured as the number of nodes in the path from the root of
        this tree to the node at the greatest depth in this tree.

        Runtime: O(n)

        >>> tree = QuadTree((100, 100))
        >>> tree.height()
        1
        >>> tree.insert('a', (90, 90))
        >>> tree.height()
        1
        >>> tree.insert('b', (30, 30))
        >>> tree.height()
        3
        """
        if self.is_leaf():
            return 1
        else:
            h = 1
            if self._nw:
                h = max(h, 1 + self._nw.height())
            if self._sw:
                h = max(h, 1 + self._sw.height())
            if self._ne:
                h = max(h, 1 + self._ne.height())
            if self._se:
                h = max(h, 1 + self._se.height())
            return h

    def depth(self, tree: Tree) -> Optional[int]:
        """ Return the depth of the subtree <tree> relative to <self>. Return
        None if <tree> is not a descendant of <self> and if <tree> is <self>.

        Runtime: O(log(n))
        >>> tree = QuadTree((100, 100))
        >>> tree.insert('a', (90, 90))
        >>> tree.insert('b', (150, 150))
        >>> tree1 = tree.__getattribute__('_nw')
        >>> tree.depth(tree1)
        1
        """
        if isinstance(tree, QuadTree):
            if tree is self or self.is_leaf() or tree.is_empty():
                return None
            x, y = self._centre
            x1, y1 = tree._centre
            if x1 > 2 * x or y1 > 2 * y or x1 < 0 or y1 < 0:
                return None
            subtree = self._point_position(tree._centre)[0]
            if subtree:
                dep = subtree._help_depth(tree)
                if dep is not None:
                    return 1 + dep

    def _help_depth(self, tree: QuadTree) -> Optional[int]:
        """
        Return the depth of the subtree <tree> relative to <self>. Return
        None if <tree> is not a descendant of <self>,  if <tree> is <self>
        return 0.
        === Precondition ===
        - This function is only called to the trees other than the root
        QuadTree.
        """
        if self.is_leaf():
            if tree is self:
                return 0
            else:
                return None
        else:
            subtree = self._point_position(tree._centre)[0]
            if subtree:
                dep = subtree._help_depth(tree)
                if dep is not None:
                    return 1 + dep

    def is_leaf(self) -> bool:
        """ Return True if <self> has no children.

        Runtime: O(1)
        >>> tree = QuadTree((100, 100))
        >>> tree.is_leaf()
        True
        >>> tree.insert('a', (90, 90))
        >>> tree.is_leaf()
        True
        >>> tree.insert('b', (120, 120))
        >>> tree.is_leaf()
        False
        """
        return not self._ne and not self._se and not self._nw and not self._sw

    def is_empty(self) -> bool:
        """ Return True if <self> or any of its descendants do not store any
        information about the location of any players.

        Runtime: O(1)
        >>> tree = QuadTree((100, 100))
        >>> tree.is_empty()
        True
        >>> tree.insert('a', (90, 90))
        >>> tree.is_empty()
        False
        """
        return self.is_leaf() and not self._name and not self._point


class TwoDTree(Tree):
    """
    A tree storing positional information of players, and divides each rectangle
    into two rectangles centred on a point.

    === Private Attributes ===
    _name: the name of a player
    _point: the x/y coordinates of the player, also the dividing point of the
    rectangle
    _nw: the x/y coordinates of the north west corner of the rectangle described
    by this root tree. None for non-root node in this tree.
    _se: the x/y coordinates of the south east corner of the rectangle described
    by this root tree. None for non-root node in this tree.
    _lt: a 2D-tree that represents the either the north-most or west-most
    section of the rectangle. None if the section does not store points.
    _gt: a 2D-tree that represents the either the south-most or east-most
    section of the rectangle. None if the section does not store points.
    _split_type: a string indicating whether this rectangle should be split
    vertically or horizontally.

    === Representation Invariants ===
    - all nodes must have _name and _point attributes unless they have no
    descendants and no parents.
    - a non-root node should have a value of None for both its _nw and _se
    attributes. and a root node should not have a value of None for them.
    - a node with no parents must have a _split_type == 'x'
    - a node must not have a parent or any children with the same _split_type.
    - for a given node p, if _split_type == 'x' then:
    all descendants d of p must be in p._lt if d._point[0] <= p._point[0] and
    be in p._gt otherwise
    - for a given node p, if _split_type == 'y' then:
    all descendants d of p must be in p._lt if d._point[1] <= p._point[1] and
    be in p._gt otherwise
    - _split_type should be string of x or y, indicates the rectangle be split
    along the x axis, dividing into two side-by-side smaller rectangles, or
    split along the y axis, dividing into two smaller rectangles, one above
    the other.
    """
    _name: Optional[str]
    _point: Optional[Tuple[int, int]]
    _nw: Optional[Tuple[int, int]]
    _se: Optional[Tuple[int, int]]
    _lt: Optional[TwoDTree]
    _gt: Optional[TwoDTree]
    _split_type: str

    def __init__(self, nw: Optional[Tuple[int, int]],
                 se: Optional[Tuple[int, int]]) -> None:
        """Initialize a new Tree instance.

        === Precondition ===
        - a non-root node should have a value of None for both nw and se when
        initialized.
        - a root node should not have a value of None for both nw and se when
        initialized.

        Runtime: O(1)
        >>> tree = TwoDTree((0, 0), (500, 500))
        >>> tree.__getattribute__('_nw')
        (0, 0)
        >>> tree.__getattribute__('_se')
        (500, 500)
        >>> tree.__getattribute__('_split_type')
        'x'
        >>> tree.is_empty()
        True
        """
        self._name = None
        self._point = None
        self._nw = nw
        self._se = se
        self._lt = None
        self._gt = None
        self._split_type = 'x'

    def __contains__(self, name: str) -> bool:
        """ Return True if a player named <name> is stored in this tree.

        Runtime: O(n)
        >>> tree = TwoDTree((0, 0), (500, 500))
        >>> tree.insert('a', (250, 250))
        >>> 'a' in tree
        True
        >>> 'b' in tree
        False
        """
        if self._name == name:
            return True
        elif self._lt and name in self._lt:
            return True
        elif self._gt and name in self._gt:
            return True
        else:
            return False

    def contains_point(self, point: Tuple[int, int]) -> bool:
        """ Return True if a player at location <point> is stored in this tree.

        Runtime: O(log(n))
        >>> tree = TwoDTree((0, 0), (500, 500))
        >>> tree.insert('a', (250, 250))
        >>> tree.contains_point((250, 250))
        True
        """
        if self.is_leaf():
            return self._point == point
        else:
            x, y = self._point
            x1, y1 = point
            if self._point == point:
                return True
            elif self._split_type == 'x':
                if x1 <= x:
                    if self._lt:
                        return self._lt.contains_point(point)
                    else:
                        return False
                else:
                    if self._gt:
                        return self._gt.contains_point(point)
                    else:
                        return False
            else:
                if y1 <= y:
                    if self._lt:
                        return self._lt.contains_point(point)
                    else:
                        return False
                else:
                    if self._gt:
                        return self._gt.contains_point(point)
                    else:
                        return False

    def insert(self, name: str, point: Tuple[int, int]) -> None:
        """Insert a player named <name> into this tree at point <point>.

        Raise an OutOfBoundsError if <point> is out of bounds.

        Raise an OutOfBoundsError if moving the player would place the player at
        exactly the same coordinates of another player in the Tree (before
        moving the player).

        Runtime: O(log(n))

        >>> tree = TwoDTree((0, 0), (500, 500))
        >>> tree.insert('a', (250, 250))
        >>> 'a' in tree
        True
        >>> tree.contains_point((250, 250))
        True
        >>> tree.insert('b', (100, 150))
        >>> 'b' in tree
        True
        >>> tree.contains_point((100, 150))
        True
        >>> tree.__getattribute__('_lt') is not None
        True
        """
        x1, y1 = point
        if x1 < self._nw[0] or x1 > self._se[0] or y1 < self._nw[1] or \
                y1 > self._se[1] or self.contains_point(point):
            raise OutOfBoundsError
        self._help_insert(name, point)

    def _help_insert(self, name: str, point: Tuple[int, int]) -> None:
        """
        Insert a player named <name> into this tree at point <point>.

        === Precondition ===
        - The point <point> is in bound
        - The point <point> is not in this tree before insert.
        """
        x1, y1 = point
        if self.is_empty():
            self._name, self._point = name, point
        else:
            x, y = self._point
            if self._split_type == 'x':
                if x1 <= x:
                    if not self._lt:
                        self._lt = TwoDTree(None, None)
                        self._lt._name, self._lt._point = name, point
                        self._lt._split_type = 'y'
                    else:
                        self._lt._help_insert(name, point)
                else:
                    if not self._gt:
                        self._gt = TwoDTree(None, None)
                        self._gt._name, self._gt._point = name, point
                        self._gt._split_type = 'y'
                    else:
                        self._gt._help_insert(name, point)
            else:
                if y1 <= y:
                    if not self._lt:
                        self._lt = TwoDTree(None, None)
                        self._lt._name, self._lt._point = name, point
                        self._lt._split_type = 'x'
                    else:
                        self._lt._help_insert(name, point)
                else:
                    if not self._gt:
                        self._gt = TwoDTree(None, None)
                        self._gt._name, self._gt._point = name, point
                        self._gt._split_type = 'x'
                    else:
                        self._gt._help_insert(name, point)

    def remove(self, name: str) -> None:
        """ Remove information about a player named <name> from this tree.
        There is no empty node within this tree after remove (If the root of a
        non_leaf node is removed, the root will be replaced by a closet point
        found its descendants).

        if a player with that name does not exist in the tree, the method
        fail silently without making any changes to the tree.

        Runtime: O(n)
        >>> tree = TwoDTree((0, 0), (500, 500))
        >>> tree.insert('a', (250, 250))
        >>> tree.insert('b', (100, 150))
        >>> tree.insert('c', (150, 100))
        >>> 'a' in tree
        True
        >>> tree.remove('a')
        >>> 'a' in tree
        False
        >>> tree.contains_point((250, 250))
        False
        >>> 'b' in tree
        True
        >>> 'c' in tree
        True
        >>> tree.__getattribute__('_point')
        (150, 100)
        """
        if name in self:
            if self.is_leaf():
                self._name, self._point = None, None
            else:
                point = self._find_point(name)
                self.remove_point(point)

    def _find_point(self, name: str) -> Tuple[int, int]:
        """
        Return the point of the player with the name <name> located at in this
        tree.

        === precondition ===
        - <name> is in this tree.
        """
        if self._name == name:
            return self._point
        elif self._lt and name in self._lt:
            return self._lt._find_point(name)
        else:
            if self._gt and name in self._gt:
                return self._gt._find_point(name)

    def remove_point(self, point: Tuple[int, int]) -> None:
        """ Remove information about a player at point <point> from this tree.
        There is no empty node within this tree after remove (If the root of a
        non_leaf node is removed, the root will be replaced by a closet point
        found its descendants).

        if a player with at that point does not exist in the tree, the method
        fail silently without making any changes to the tree.
        Runtime: O(log(n))

        >>> tree = TwoDTree((0, 0), (500, 500))
        >>> tree.insert('a', (250, 250))
        >>> tree.insert('b', (100, 150))
        >>> tree.insert('c', (150, 100))
        >>> tree.insert('d', (300, 300))
        >>> 'b' in tree
        True
        >>> tree.remove_point((100, 150))
        >>> 'b' in tree
        False
        >>> tree.contains_point((100, 150))
        False
        >>> 'a' in tree
        True
        >>> 'c' in tree
        True
        >>> 'd' in tree
        True
        >>> tree1 = tree.__getattribute__('_lt')
        >>> tree1.__getattribute__('_point')
        (150, 100)
        """
        if self.contains_point(point):
            x1, y1 = point
            x, y = self._point
            if self._point == point:
                self._remove_root()
            elif self._split_type == 'x':
                if x1 <= x:
                    self._lt.remove_point(point)
                    if self._lt.is_empty():
                        self._lt = None
                else:
                    self._gt.remove_point(point)
                    if self._gt.is_empty():
                        self._gt = None
            else:
                if y1 <= y:
                    self._lt.remove_point(point)
                    if self._lt.is_empty():
                        self._lt = None
                else:
                    self._gt.remove_point(point)
                    if self._gt.is_empty():
                        self._gt = None

    def _remove_root(self) -> None:
        """
        Remove the root of this tree. If this tree is not a leaf, the root will
        be replaced by a closet point found in its descendants, so the
        _lt and _gt relationship of the descendants will be maintained.
        """
        if self.is_leaf():
            self._point, self._name = None, None
        elif self._split_type == 'x':
            if self._lt:
                if self._lt.is_leaf():
                    self._point, self._name = self._lt._point, self._lt._name
                    self._lt = None
                else:
                    root_node = self._lt._find_root(self._lt, 'x', 'l')
                    self._point, self._name = root_node._point, root_node._name
                    if root_node.is_leaf():
                        self._lt._remove_node(root_node)
                    else:
                        root_node._remove_root()
            else:
                if self._gt.is_leaf():
                    self._point, self._name = self._gt._point, self._gt._name
                    self._gt = None
                else:
                    root_node = self._gt._find_root(self._gt, 'x', 'g')
                    self._point, self._name = root_node._point, root_node._name
                    if root_node.is_leaf():
                        self._gt._remove_node(root_node)
                    else:
                        root_node._remove_root()
        else:
            if self._lt:
                if self._lt.is_leaf():
                    self._point, self._name = self._lt._point, self._lt._name
                    self._lt = None
                else:
                    root_node = self._lt._find_root(self._lt, 'y', 'l')
                    self._point, self._name = root_node._point, root_node._name
                    if root_node.is_leaf():
                        self._lt._remove_node(root_node)
                    else:
                        root_node._remove_root()
            else:
                if self._gt.is_leaf():
                    self._point, self._name = self._gt._point, self._gt._name
                    self._gt = None
                else:
                    root_node = self._gt._find_root(self._gt, 'y', 'g')
                    self._point, self._name = root_node._point, root_node._name
                    if root_node.is_leaf():
                        self._gt._remove_node(root_node)
                    else:
                        root_node._remove_root()

    def _find_root(self, root_node: TwoDTree, split: str, j: str) -> TwoDTree:
        """
        Find the point in the descendants of self that closet to the point
        represented by <root_node> (find closet x if split == 'x', find closet
        y if split == 'y', and j == 'l' means the biggest point will be the
        closet one, j == 'g' means the smallest point will be the
        closet one)
        """
        if split == 'x':
            i = 0
        else:
            i = 1
        cha_p = root_node._point
        if self.is_leaf():
            if j == 'l' and self._point[i] > cha_p[i]:
                root_node = self
            elif j == 'g' and self._point[i] < cha_p[i]:
                root_node = self
        elif self._split_type != split:
            if self._lt and self._gt:
                root_node = self._lt._find_root(root_node, split, j)
                root_node = self._gt._find_root(root_node, split, j)
            elif self._lt:
                root_node = self._lt._find_root(root_node, split, j)
            else:
                root_node = self._gt._find_root(root_node, split, j)
        else:
            if j == 'l' and self._gt:
                root_node = self._gt._find_root(root_node, split, j)
            elif j == 'g' and self._lt:
                root_node = self._lt._find_root(root_node, split, j)
        return root_node

    def _remove_node(self, node: TwoDTree) -> None:
        """
        Remove the <node> in self.

        === Precondition ===
        - The <node> is leaf node
        - The point of <node> is already been used to replace another root node
        point above it.
        """
        x, y = self._point
        x1, y1 = node._point
        if self._split_type == 'x':
            if x1 <= x:
                if self._lt is node:
                    self._lt = None
                elif self._lt:
                    self._lt._remove_node(node)
            else:
                if self._gt is node:
                    self._gt = None
                elif self._gt:
                    self._gt._remove_node(node)
        else:
            if y1 <= y:
                if self._lt is node:
                    self._lt = None
                elif self._gt:
                    self._lt._remove_node(node)
            else:
                if self._gt is node:
                    self._gt = None
                elif self._gt:
                    self._gt._remove_node(node)

    def move(self, name: str, direction: str, steps: int) -> \
            Optional[Tuple[int, int]]:
        """
        Return the new location of the player named <name> after moving it
        in the given <direction> by <steps> steps.

        Raise an OutOfBoundsError if this would move the player named
        <name> out of bounds (before moving the player).
        Raise an OutOfBoundsError if moving the player would place the player at
        exactly the same coordinates of another player in the Tree (before
        moving the player).

        if a player with that name does not exist in the tree, the method
        fail silently without making any changes to the tree.

        Runtime: O(n)

        === precondition ===
        direction in ['N', 'S', 'E', 'W']

        >>> tree = TwoDTree((0, 0), (500, 500))
        >>> tree.insert('a', (250, 250))
        >>> tree.insert('b', (200, 150))
        >>> tree.insert('c', (300, 300))
        >>> 'a' in tree
        True
        >>> tree.move('a', 'W', 100)
        (150, 250)
        >>> 'a' in tree
        True
        >>> tree.contains_point((150, 250))
        True
        >>> tree.__getattribute__('_point')
        (200, 150)
        >>> tree.__getattribute__('_name')
        'b'
        >>> tree1 = tree.__getattribute__('_lt')
        >>> tree1.__getattribute__('_point')
        (150, 250)
        >>> tree1.__getattribute__('_name')
        'a'
        """
        if name in self:
            x0, y0 = self._find_point(name)
            if steps == 0:
                return x0, y0
            if direction == 'N':
                y0 -= steps
            elif direction == 'S':
                y0 += steps
            elif direction == 'E':
                x0 += steps
            else:
                x0 -= steps
            if x0 < self._nw[0] or x0 > self._se[0] or y0 < self._nw[1] or \
                    y0 > self._se[1] or self.contains_point((x0, y0)):
                raise OutOfBoundsError
            self.remove(name)
            self.insert(name, (x0, y0))
            return x0, y0

    def move_point(self, point: Tuple[int, int], direction: str, steps: int) \
            -> Optional[Tuple[int, int]]:
        """ Return the new location of the player at point <point> after moving
        it in the given <direction> by <steps> steps.

        Raise an OutOfBoundsError if this would move the player at point
        <point> out of bounds (before moving the player).

        Raise an OutOfBoundsError if moving the player would place the player at
        exactly the same coordinates of another player in the Tree (before
        moving the player).

        Moving a point may require the tree to be reorganized. This method
        should do the minimum amount of tree reorganization possible to move the
        given point properly. (if the new point will be added to the same node
        that the old point removed from, change the _point attribute of this
        node directly.)

        if a player with at that point does not exist in the tree, the method
        fail silently without making any changes to the tree.

        Runtime: O(log(n))

        === precondition ===
        direction in ['N', 'S', 'E', 'W']

        >>> tree = TwoDTree((0, 0), (500, 500))
        >>> tree.insert('a', (250, 250))
        >>> tree.insert('b', (150, 150))
        >>> 'a' in tree
        True
        >>> tree.move_point((250, 250), 'N', 50)
        (250, 200)
        >>> 'a' in tree
        True
        >>> tree.contains_point((250, 200))
        True
        >>> tree.__getattribute__('_point')
        (250, 200)
        """
        if self.contains_point(point):
            name = self._find_name(point)
            x2, y2 = point
            if steps == 0:
                return point
            if direction == 'N':
                y2 -= steps
            elif direction == 'S':
                y2 += steps
            elif direction == 'E':
                x2 += steps
            else:
                x2 -= steps
            if x2 < self._nw[0] or x2 > self._se[0] or y2 < self._nw[1] or \
                    y2 > self._se[1] or self.contains_point((x2, y2)):
                raise OutOfBoundsError
            check = self._check_side(point[0], point[1], x2, y2, name)
            if not check:
                self.remove_point(point)
                self.insert(name, (x2, y2))
            return x2, y2

    def _check_side(self, x1: int, y1: int, x2: int, y2: int, name: str) -> \
            bool:
        """
        Return true if the new point (<x2>, <y2>) will be added to the same node
        that the old point (<x1>, <y1>) removed from, and change the _point
        attribute of this node to (<x2>, <y2>), change _name to <name>, else,
        return False, change nothing.

        === Precondition ===
        - (<x1>, <y1>) is in self.
        - (<x2>, <y2>) is within the bound of self.
        """
        if self.is_leaf():
            self._name, self._point = name, (x2, y2)
            return True
        elif self._split_type == 'x':
            if self._point == (x1, y1):
                if x1 == x2:
                    self._name, self._point = name, (x2, y2)
                    return True
                else:
                    return False
            else:
                x = self._point[0]
                if x1 <= x and x2 <= x:
                    return self._lt._check_side(x1, y1, x2, y2, name)
                elif x1 > x and x2 > x:
                    return self._gt._check_side(x1, y1, x2, y2, name)
                else:
                    return False
        else:
            if self._point == (x1, y1):
                if y1 == y2:
                    self._name, self._point = name, (x2, y2)
                    return True
                else:
                    return False
            else:
                y = self._point[1]
                if y1 <= y and y2 <= y:
                    return self._lt._check_side(x1, y1, x2, y2, name)
                elif y1 > y and y2 > y:
                    return self._gt._check_side(x1, y1, x2, y2, name)
                else:
                    return False

    def _find_name(self, point: Tuple[int, int]) -> str:
        """
        Return the name of the player at the point <point> located at in this
        tree.

        === precondition ===
        - <point> is in this tree.
        """
        if self._point == point:
            return self._name
        elif self._split_type == 'x':
            if point[0] <= self._point[0] and self._lt:
                return self._lt._find_name(point)
            else:
                if self._gt:
                    return self._gt._find_name(point)
        else:
            if point[1] <= self._point[1] and self._lt:
                return self._lt._find_name(point)
            else:
                if self._gt:
                    return self._gt._find_name(point)

    def names_in_range(self, point: Tuple[int, int], direction: str,
                       distance: int) -> List[str]:
        """ Return a list of names of players whose location is in the
        <direction> relative to <point> and whose location is within <distance>
        along both the x and y axis.

        For example: names_in_range((100, 100), 'SE', 10) should return the
        names of all the players south east of (100, 100) and within 10 steps in
        either direction.
        In other words, find all players whose location is in the box with
        corners at (include corner points): (100, 100) (110, 100) (100, 110)
        (110, 110)

        Runtime: faster than O(n) when distance is small (Only check the
        subtrees which the box included.)

        === precondition ===
        direction in ['NE', 'SE', 'NE', 'SW']
        >>> tree = TwoDTree((0, 0), (500, 500))
        >>> tree.insert('a', (200, 200))
        >>> tree.insert('b', (150, 150))
        >>> tree.names_in_range((120, 120), 'SE', 100)
        ['a', 'b']
        """
        if self.is_empty():
            return []
        else:
            x0, y0 = point
            if direction == 'NW':
                x = x0 - distance
                y = y0 - distance
            elif direction == 'SW':
                x = x0 - distance
                y = y0 + distance
            elif direction == 'NE':
                x = x0 + distance
                y = y0 - distance
            else:
                x = x0 + distance
                y = y0 + distance
            left, top, right, bottom = min(x0, x), min(y0, y), max(x0, x), max(
                y0, y)
            return self._name_in_range(left, top, right, bottom)

    def _name_in_range(self, left: int, top: int, right: int,
                       bottom: int) -> List[str]:
        """
        Return a list of names that is within the frame constructed by the
        four boundaries <left>, <top>, <right>, <bottom>. Only check the
        subtrees which the frame included.

        === Precondition ===
        - This function is only to be called on the root QuadTree.
        """
        if self.is_empty():
            return []
        elif self.is_leaf():
            if left <= self._point[0] <= right and \
                    top <= self._point[1] <= bottom:
                return [self._name]
            else:
                return []
        else:
            result = []
            x, y = self._point
            if left <= x <= right and top <= y <= bottom:
                result.append(self._name)
            if self._split_type == 'x':
                if x < right and self._gt:
                    result.extend(self._gt._name_in_range(left, top, right,
                                                          bottom))
                if x >= left and self._lt:
                    result.extend(self._lt._name_in_range(left, top, right,
                                                          bottom))
            else:
                if y < bottom and self._gt:
                    result.extend(self._gt._name_in_range(left, top, right,
                                                          bottom))
                if y >= top and self._lt:
                    result.extend(self._lt._name_in_range(left, top, right,
                                                          bottom))
            return result

    def size(self) -> int:
        """ Return the number of nodes in <self>. For an empty tree, it still
        has size of 1.

        Runtime: O(n)
        >>> tree = TwoDTree((0, 0), (500, 500))
        >>> tree.size()
        1
        >>> tree.insert('a', (250, 250))
        >>> tree.insert('b', (150, 150))
        >>> tree.size()
        2
        """
        if self.is_leaf():
            return 1
        else:
            s = 1
            if self._lt:
                s += self._lt.size()
            if self._gt:
                s += self._gt.size()
            return s

    def height(self) -> int:
        """ Return the height of <self>.

        Height is measured as the number of nodes in the path from the root of
        this tree to the node at the greatest depth in this tree.

        Runtime: O(n)
        >>> tree = TwoDTree((0, 0), (500, 500))
        >>> tree.height()
        1
        >>> tree.insert('a', (250, 250))
        >>> tree.height()
        1
        >>> tree.insert('b', (150, 150))
        >>> tree.insert('b', (300, 300))
        >>> tree.height()
        2
        """
        if self.is_leaf():
            return 1
        else:
            h = 1
            if self._lt:
                h = max(h, 1 + self._lt.height())
            if self._gt:
                h = max(h, 1 + self._gt.height())
            return h

    def depth(self, tree: Tree) -> Optional[int]:
        """ Return the depth of the subtree <tree> relative to <self>. Return
        None if <tree> is not a descendant of <self> and if <tree> is <self>.

        Runtime: O(log(n))
        >>> tree = TwoDTree((0, 0), (500, 500))
        >>> tree.insert('a', (250, 250))
        >>> tree.insert('b', (150, 150))
        >>> tree1 = tree.__getattribute__('_lt')
        >>> tree.depth(tree1)
        1
        """
        if isinstance(tree, TwoDTree):
            if self is tree or self.is_leaf() or tree.is_empty():
                return None
            else:
                subtree = self._point_position(tree._point)
                if subtree:
                    dep = subtree._help_depth(tree)
                    if dep is not None:
                        return dep + 1

    def _help_depth(self, tree: TwoDTree) -> Optional[int]:
        """
        Return the depth of the subtree <tree> relative to <self>. Return
        None if <tree> is not a descendant of <self>,  if <tree> is <self>
        return 0.
        === Precondition ===
        - This function is only called to the trees other than the root
        TwoDTree.
        """
        if self is tree:
            return 0
        elif self.is_leaf():
            return None
        else:
            subtree = self._point_position(tree._point)
            if subtree:
                dep = subtree._help_depth(tree)
                if dep is not None:
                    return dep + 1

    def _point_position(self, point: Tuple[int, int]) -> TwoDTree:
        """ Return the leaf <self> in the direction point <point> is located at.

        Runtime: O(1)
        """
        if self._split_type == 'x':
            if point[0] <= self._point[0]:
                return self._lt
            else:
                return self._gt
        elif self._split_type == 'y':
            if point[1] <= self._point[1]:
                return self._lt
            else:
                return self._gt

    def is_leaf(self) -> bool:
        """ Return True if <self> has no children

        Runtime: O(1)
        >>> tree = TwoDTree((0, 0), (500, 500))
        >>> tree.is_leaf()
        True
        >>> tree.insert('a', (250, 250))
        >>> tree.is_leaf()
        True
        >>> tree.insert('b', (150, 150))
        >>> tree.is_leaf()
        False
        """
        return not self._lt and not self._gt

    def is_empty(self) -> bool:
        """ Return True if <self> or any of its descendants do not store any
        information about the location of any players.

        Runtime: O(1)
        >>> tree = TwoDTree((0, 0), (500, 500))
        >>> tree.is_empty()
        True
        >>> tree.insert('a', (250, 250))
        >>> tree.is_empty()
        False
        """
        return self.is_leaf() and not self._name and not self._point

    def balance(self) -> None:
        """ Balance <self> so that there is at most a difference of 1 between
        the size of the _lt subtree and the size of the _gt subtree for all
        trees in <self>.

        === Precondition ===
        It is possible to balance this tree
        >>> tree = TwoDTree((0, 0), (500, 500))
        >>> tree.insert('a', (250, 250))
        >>> tree.insert('b', (100, 150))
        >>> tree.insert('c', (120, 200))
        >>> tree.insert('d', (150, 100))
        >>> tree.insert('e', (300, 300))
        >>> tree.balance()
        >>> tree.__getattribute__('_point')
        (150, 100)
        >>> tree.__getattribute__('_name')
        'd'
        >>> tree_l1 = tree.__getattribute__('_lt')
        >>> tree_l1.__getattribute__('_point')
        (120, 200)
        >>> tree_l2 = tree_l1.__getattribute__('_lt')
        >>> tree_l2.__getattribute__('_point')
        (100, 150)
        >>> tree_g1 = tree.__getattribute__('_gt')
        >>> tree_g1.__getattribute__('_point')
        (300, 300)
        >>> tree_g2 = tree_g1.__getattribute__('_lt')
        >>> tree_g2.__getattribute__('_point')
        (250, 250)
        >>> tree_g1.height() <= tree_l1.height() <= tree_g1.height() + 1
        True
        """
        if not self.is_leaf() and not (
                self._lt and self._gt and self._lt.is_leaf() and
                self._gt.is_leaf()):
            if (not self._lt or self._lt.is_leaf() or self._gt) and \
                    (not self._gt or not self._gt.is_leaf() or self._lt):
                lst_x, lst_y0 = self._build_list()
                lst_x.sort()
                lst_y0.sort()
                lst_y = []
                for item in lst_y0:
                    lst_y.append(((item[0][1], item[0][0]), item[1]))
                self._lt, self._gt = None, None
                self._point, self._name = None, None
                self._help_balance(lst_x, lst_y)

    def _help_balance(self, lst_x: list, lst_y: list) -> None:
        """
        Rebuild self as a balance tree from the <lst_x>, <lst_y>, which records
        all the points from original self in order.
        """
        lst0_x, lst1_x, lst0_y, lst1_y = [], [], [], []
        if self._split_type == 'x':
            if len(lst_x) == 1:
                self._point, self._name = lst_x[0]
            else:
                mid = len(lst_x) // 2
                while mid < len(lst_x) - 1 and lst_x[mid][0][0] == \
                        lst_x[mid + 1][0][0]:
                    mid += 1
                self._point, self._name = lst_x[mid]
                lst0_x = lst_x[:mid]
                if mid + 1 < len(lst_x):
                    lst1_x = lst_x[mid + 1:]
                for item in lst_y:
                    if item in lst0_x:
                        lst0_y.append(item)
                    elif item in lst1_x:
                        lst1_y.append(item)

        else:
            if len(lst_y) == 1:
                self._point, self._name = lst_y[0]
            else:
                mid = len(lst_y) // 2
                while mid < len(lst_y) - 1 and lst_y[mid][0][1] == \
                        lst_y[mid + 1][0][1]:
                    mid += 1
                self._point, self._name = lst_y[mid]
                lst0_y = lst_y[:mid]
                if mid + 1 < len(lst_x):
                    lst1_y = lst_y[mid + 1:]
                for item in lst_x:
                    if item in lst0_y:
                        lst0_x.append(item)
                    elif item in lst1_y:
                        lst1_x.append(item)
        if lst0_x:
            self._lt = TwoDTree(None, None)
            if self._split_type == 'x':
                self._lt._split_type = 'y'
            else:
                self._lt._split_type = 'x'
            self._lt._help_balance(lst0_x, lst0_y)
        if lst1_x:
            self._gt = TwoDTree(None, None)
            if self._split_type == 'x':
                self._gt._split_type = 'y'
            else:
                self._gt._split_type = 'x'
            self._gt._help_balance(lst1_x, lst1_y)

    def _build_list(self) -> Tuple[List[Tuple[tuple, str]],
                                   List[Tuple[tuple, str]]]:
        """
        Return a tuple of two lists: lst_x, which records all the points
        and name from self in order from smallest to biggest, based on x, and
        lst_y, which records all the points and name from self in order from
        smallest to biggest, based on x.
        """
        lst_x, lst_y = [], []
        if self._lt:
            lst_x.extend(self._lt._build_list()[0])
            lst_y.extend(self._lt._build_list()[1])
        lst_x.append((self._point, self._name))
        lst_y.append(((self._point[1], self._point[0]), self._name))
        if self._gt:
            lst_x.extend(self._gt._build_list()[0])
            lst_y.extend(self._gt._build_list()[1])
        return lst_x, lst_y


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={'extra-imports': ['typing'],
                                'disable': ['R0913', 'R0902', 'W0611', 'R1710',
                                            'R1702']})
