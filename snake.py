import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Screen dimensions
WIDTH = 640
HEIGHT = 480

# Block size
BLOCK_SIZE = 20

# FPS
FPS = 5

# Font
FONT = pygame.font.SysFont(None, 35)

class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * BLOCK_SIZE)) % WIDTH), (cur[1] + (y * BLOCK_SIZE)) % HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, BLACK, r, 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE,
                         random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE)

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, BLACK, r, 1)

def draw_text(surface, text, color, x, y):
    textobj = FONT.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def main():
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Snake Game')

    snake = Snake()
    food = Food()

    score = 0

    while True:
        snake.handle_keys()
        snake.move()

        if snake.get_head_position() == food.position:
            snake.length += 1
            score += 1
            food.randomize_position()

        screen.fill(BLACK)
        snake.draw(screen)
        food.draw(screen)
        draw_text(screen, f"Score: {score}", WHITE, 10, 10)

        pygame.display.update()
        clock.tick(FPS)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

if __name__ == "__main__":
    main()
