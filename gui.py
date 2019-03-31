import pygame
from game import Game, Bots
from snake import Snake, Direction
pygame.init()

WHITE, BLACK, RED, GREEN = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 255, 0)


class GameGUI:
    width, height = 30, 30
    box_size = 10
    WIDTH, HEIGHT = width * box_size, height * box_size
    FPS = 60
    BOT_MODE = True

    def __init__(self):
        self.screen = pygame.display.set_mode((GameGUI.WIDTH, GameGUI.HEIGHT))
        self.screen.fill(WHITE)
        self.game_over = False
        self.game_quit = False
        self.rectangle_list = []
        self.game = Game(GameGUI.width, GameGUI.height)
        self.game.register_update_food_handler(self.on_food_handler)
        self.game.snake.register_snake_handlers(self.on_snake_grow_handler, self.on_snake_remove_handler)
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()

    def on_food_handler(self, game, food):
        # print("Inside food handler ")
        width, height = GameGUI.box_size, GameGUI.box_size
        left, top = food.X * GameGUI.box_size, food.Y * GameGUI.box_size
        rect = pygame.Rect(left, top, width, height)
        pygame.draw.rect(self.screen, WHITE, rect)
        pygame.draw.ellipse(self.screen, GREEN, rect)
        self.rectangle_list.append(rect)

    def on_snake_grow_handler(self, snake, head):
        # print("Inside grow handler")
        box_size = GameGUI.box_size
        width, height = GameGUI.box_size, GameGUI.box_size
        left, top = head.X * GameGUI.box_size, head.Y * GameGUI.box_size
        rect = pygame.Rect(left, top, width, height)
        if len(snake) > 1:
            prev_head = snake.snake[-2]
            left, top = prev_head.X * GameGUI.box_size, prev_head.Y * GameGUI.box_size
            prev_rect = pygame.Rect(left, top, width, height)
            pygame.draw.rect(self.screen, WHITE, prev_rect)
            pygame.draw.rect(self.screen, BLACK, prev_rect.inflate(-box_size//5, -box_size//5))
            self.rectangle_list.append(prev_rect)
        pygame.draw.rect(self.screen, BLACK, rect)
        self.rectangle_list.append(rect)

    def on_snake_remove_handler(self, snake, tail):
        # print("Inside remove handler ")
        width, height = GameGUI.box_size, GameGUI.box_size
        left, top = tail.X * GameGUI.box_size, tail.Y * GameGUI.box_size
        rect = pygame.Rect(left, top, width, height)
        pygame.draw.rect(self.screen, WHITE, rect)
        self.rectangle_list.append(rect)

    def quit_game(self):
        self.game_quit = True
        pygame.quit()
        quit()

    def game_loop(self):
        while not self.game_quit:
            direction = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()

                directions = []
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        directions.append(Direction.LEFT)
                    elif event.key == pygame.K_UP:
                        directions.append(Direction.UP)
                    elif event.key == pygame.K_RIGHT:
                        directions.append(Direction.RIGHT)
                    elif event.key == pygame.K_DOWN:
                        directions.append(Direction.DOWN)
                direction = directions[0] if len(directions) == 1 else None
            pygame.display.update(self.rectangle_list)
            self.rectangle_list = []
            self.clock.tick(GameGUI.FPS)
            # print('GAME OVER:', self.game_over)
            if not self.game_over:
                if GameGUI.BOT_MODE:
                    direction = Bots.bot_1(self.game)
                self.game_over = not self.game.next_iteration(direction)
                if self.game_over:
                    print("GAME OVER")


if __name__ == '__main__':
    game_gui = GameGUI()
    game_gui.game_loop()
