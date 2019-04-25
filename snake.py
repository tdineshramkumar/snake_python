from enum import Enum, auto
import random


class Direction(Enum):
    """ Enumeration to represent directions """
    LEFT = auto()
    UP = auto()
    RIGHT = auto()
    DOWN = auto()

    @staticmethod
    def all_directions():
        """ This utility function returns a list of all possible directions """
        return [Direction.LEFT, Direction.UP, Direction.RIGHT, Direction.DOWN]

    @staticmethod
    def opposite_direction(direction):
        """ Returns the opposite of requested direction """
        return Direction.RIGHT if direction == Direction.LEFT \
            else Direction.LEFT if direction == Direction.RIGHT \
            else Direction.UP if direction == Direction.DOWN else Direction.DOWN


class PointGenerator:
    """ This generator class returns a Point class with set bounds """
    @staticmethod
    def new(width, height):
        class Point:
            """ Stores x, y coordinates and wraps inside set bound """
            def __init__(self, x, y):
                self.X = x % width
                self.Y = y % height

            def __eq__(self, other):
                if not other:
                    return False
                return self.X == other.X and self.Y == other.Y
        return Point


class SnakeUtils:
    @staticmethod
    def get_next_point(__Point, head, direction):
        """ __Point is the point class obtained from generator,
        head is point after which to look at the given direction """
        if direction == Direction.LEFT:
            return __Point(head.X - 1, head.Y)
        elif direction == Direction.UP:
            return __Point(head.X, head.Y - 1)
        elif direction == Direction.RIGHT:
            return __Point(head.X + 1, head.Y)
        else:
            return __Point(head.X, head.Y + 1)


class Snake:
    """ This class holds the representation of snake and
    contains functions to manipulate the snake.
     Snake is just a list of points, with first index representing the tail
     and last index the head. The next position of the snake is updated based on direction
     If next position is food, then snake is grown. Else length is maintained.
     Collision occurs and game ends if updated head lies in the body of the snake.
     Also direction of the snake can't be reversed
     """
    def __init__(self, width, height):
        """ Create a snake enclosed with given bounds,
            snake wraps around the bounds
         """
        """ Point class with specified bounds """
        self.Point = PointGenerator.new(width, height)
        """ Initial snake has just a point """
        self.snake = [self.Point(0, height // 2)]
        """ Set the initial direction of motion """
        self.direction = Direction.RIGHT

        """ Handler to call when snake updates """
        self.on_snake_grow_handler = None
        self.on_snake_remove_handler = None

    def register_snake_handlers(self, snake_grow_handler, snake_remove_handler):
        self.on_snake_grow_handler = snake_grow_handler
        self.on_snake_remove_handler = snake_remove_handler

    def __call_snake_remove_handler__(self, point):
        if self.on_snake_remove_handler:
            """ Call with snake and the point """
            self.on_snake_remove_handler(self, point)

    def __call_snake_grow_handler__(self, point):
        if self.on_snake_grow_handler:
            """ Call with snake and the point """
            self.on_snake_grow_handler(self, point)

    def remove_last_point(self):
        """ Utility function to remove the last segment, useful in motion """
        point = self.snake.pop(0)
        self.__call_snake_remove_handler__(point)
        return point

    def get_new_position(self):
        """ Get the next position based on the head and the direction """
        head = self.snake[-1]
        if self.direction == Direction.LEFT:
            return self.Point(head.X - 1, head.Y)
        elif self.direction == Direction.UP:
            return self.Point(head.X, head.Y - 1)
        elif self.direction == Direction.RIGHT:
            return self.Point(head.X + 1, head.Y)
        else:
            return self.Point(head.X, head.Y + 1)

    def check_in_snake(self, point):
        """ Used to check for collisions """
        return point in self.snake

    def __contains__(self, point):
        """ Support 'in' operation, to check if point is within snake
         for collision detection """
        return self.check_in_snake(point)

    def grow_snake(self, point):
        """ Grow the snake up updating the head with given point """
        assert point not in self.snake
        self.snake.append(point)
        self.__call_snake_grow_handler__(point)

    def __len__(self):
        return len(self.snake)

    def update_direction(self, direction):
        """ Direction can't be updated without constraint, it can't go backwards """
        if (self.direction == Direction.LEFT and direction == Direction.RIGHT) or (
                self.direction == Direction.UP and direction == Direction.DOWN) or (
                self.direction == Direction.RIGHT and direction == Direction.LEFT) or (
                self.direction == Direction.DOWN and direction == Direction.UP):
            """ Cannot update direction to opposite direction """
            return False
        """ If update is possible """
        self.direction = direction
        return True


