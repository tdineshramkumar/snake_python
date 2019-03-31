from snake import *
import random


class Game:
    SNAKE_BODY = 1
    SNAKE_HEAD = 2
    BOULDER = 3
    FOOD = 4
    NOTHING = 5

    def __init__(self, width, height):
        self.width, self.height = width, height
        self.snake = Snake(width, height)
        self.Point = PointGenerator.new(width, height)
        """ Update boulders before starting the game """
        self.boulders = []
        self.on_update_food_handler = None
        self.__update_food__()
        self.score = 0
        self.game_over = False
        self.victory = False

    def register_update_food_handler(self, handler):
        self.on_update_food_handler = handler
        self.call_update_food_handler()

    def call_update_food_handler(self):
        if self.on_update_food_handler:
            """ call by passing the entire game and the food position """
            self.on_update_food_handler(self, self.food)

    def is_game_over(self):
        """ Check if game is over due to collision or completion """
        return self.game_over

    def is_victory(self):
        """ Check if the reason for game completion is winning """
        return self.victory

    def __get_potential_points__(self):
        """ get points not on snake and boulders """
        points = []
        for i in range(self.width):
            for j in range(self.height):
                """ Check if a point is not in boulders or snake """
                point = self.Point(i, j)
                if point in self.snake or point in self.boulders:
                    continue
                else:
                    """ Then a potential point """
                    points.append(point)
        return points

    def __get_random_point__(self):
        """ Get a random point not on snake or boulder """
        points = self.__get_potential_points__()
        if not points:
            """ If no points possible, ie all occupied """
            return None
        else:
            """ Choose any one of them at random and return """
            return random.choice(points)

    def __update_food__(self):
        """ Set up the food item at a new position not on snake or boulder """
        """ This function must be called only after updating 
        the snake to prevent placing food inside snake"""
        self.food = self.__get_random_point__()
        self.call_update_food_handler()

    def get_current_snake_direction(self):
        return self.snake.direction

    def next_iteration(self, direction=None):
        """ Run a the next step, change direction if any,
        get the new position, check if in boulders or at snake, then signal end of game
        if on food, then grow the snake, else simply pop the tail and update head. """
        """ WARNING: check if game over before calling this function """
        if direction:
            """ If some direction update """
            self.snake.update_direction(direction)
        """ Get the new resultant position of the snake head """
        position = self.snake.get_new_position()
        if position in self.boulders:
            """ End of game on collision with some boulder """
            self.game_over = True
            return False
        elif position == self.food:
            """ If food then, increment score """
            self.score += 1
            """ Grow the snake, last tail remains """
            self.snake.grow_snake(position)
            """ Place the food at a new location """
            self.__update_food__()
            if not self.food:
                """ No more positions for food, Victory """
                self.game_over = True
                self.victory = True
                return False
        else:
            """ Remove the last tail segment """
            self.snake.remove_last_point()
            """ Then check if any resultant collisions with itself """
            if self.snake.check_in_snake(position):
                """ Collision with itself """
                self.game_over = True
                return False
            """ If no collision then grow the snake """
            self.snake.grow_snake(position)
        """ Return true if next iteration is possible, yet another way to check if game is in progress
            or completed """
        return True

    def on_position(self, x, y):
        """ Utility function to check whats on a given position """
        if self.Point(x, y) in self.boulders:
            """ If point is a boulder"""
            return self.BOULDER
        elif self.Point(x, y) in self.snake:
            """ If point is on snake return if body or head, distinction may be useful in drawing """
            if self.Point(x, y) == self.snake.snake[-1]:
                return self.SNAKE_HEAD
            return self.SNAKE_BODY
        elif self.Point(x, y) == self.food:
            """ If a food item """
            return self.FOOD
        else:
            """ If nothing, blank space """
            return self.NOTHING


class Bots:
    @staticmethod
    def bot_1(game, mutation=0.01):
        """ This bot makes decisions based on neighbours, it tries to avoid collision, if possible.
            if no potential collision, then moves towards food, it does not see if boulder lies between it
            and food unless it reaches the boulder (boulder becomes its neighbour)
          """
        food = game.food
        head = game.snake.snake[-1]
        """ Calculate a list of directions which result in immediate collision, these must be avoided """
        neg_directions = []
        if game.Point(head.X + 1, head.Y) in game.snake or game.Point(head.X + 1, head.Y) in game.boulders:
            neg_directions.append(Direction.RIGHT)
        if game.Point(head.X - 1, head.Y) in game.snake or game.Point(head.X - 1, head.Y) in game.boulders:
            neg_directions.append(Direction.LEFT)
        if game.Point(head.X, head.Y + 1) in game.snake or game.Point(head.X, head.Y + 1) in game.boulders:
            neg_directions.append(Direction.DOWN)
        if game.Point(head.X, head.Y - 1) in game.snake or game.Point(head.X, head.Y - 1) in game.boulders:
            neg_directions.append(Direction.UP)

        if len(neg_directions) == 4:
            """Can't do anything, if surrounded """
            return Direction.LEFT
        elif len(neg_directions) == 3:
            """ If only one remaining direction, the go with it """
            if Direction.LEFT not in neg_directions:
                return Direction.LEFT
            elif Direction.RIGHT not in neg_directions:
                return Direction.RIGHT
            if Direction.UP not in neg_directions:
                return Direction.UP
            if Direction.DOWN not in neg_directions:
                return Direction.DOWN
        elif len(neg_directions) == 2:
            directions = Direction.all_directions()
            directions.remove(neg_directions[0])
            directions.remove(neg_directions[1])
            """  Choose randomly from the remaining directions """
            return random.choice(directions)
        else:
            """ If no collision at site, go towards the food """
            """ Add a small mutation is decision making, to prevent loops """
            if random.random() <= mutation:
                """ Go random, because of mutation """
                # print("Mutation!!")
                directions = Direction.all_directions()
                directions.remove(Direction.opposite_direction(game.get_current_snake_direction()))
                return random.choice(directions)

            """ When food is some direction of the snake, go that way """
            if head.X == food.X and head.Y > food.Y:
                return Direction.UP
            elif head.X == food.X and head.Y < food.Y:
                return Direction.DOWN
            elif head.Y == food.Y and head.X > food.X:
                return Direction.LEFT
            elif head.Y == food.Y and head.X < food.X:
                return Direction.RIGHT
            """ This bot does not aggressive go towards the food """
