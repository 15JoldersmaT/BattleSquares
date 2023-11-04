import pygame
import random
import math

pygame.init()
display = pygame.display.set_mode((600,600))
pygame.display.set_caption('Battle Square!')
clock = pygame.time.Clock()

runners = []
GRID_SIZE = 30  # Each grid cell will be 30x30 pixels
grid = [[[] for _ in range(20)] for _ in range(20)]  # 20x20 grid based on 600x600 display and 30x30 grid size

class Unit:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direct = random.choice(['Up', 'Down', 'Left', 'Right'])
        self.color = (random.randint(1,255), random.randint(1,255), random.randint(1,255))
        self.frames_moved_in_current_direction = 0

        
    def distance(self, other):
        return (self.x - other.x)**2 + (self.y - other.y)**2  # Use squared distance for efficiency

    def move(self):
        if self.frames_moved_in_current_direction > 10:
            self.direct = random.choice(['Up', 'Down', 'Left', 'Right'])
            self.frames_moved_in_current_direction = 0
        self.frames_moved_in_current_direction += 1

        if self.direct == 'Down' and self.y < 590:
            self.y += 1
        elif self.direct == 'Up' and self.y > 0:
            self.y -= 1
        elif self.direct == 'Right' and self.x < 590:
            self.x += 1
        elif self.direct == 'Left' and self.x > 0:
            self.x -= 1

    def main(self, display):
        pygame.draw.rect(display, self.color, (self.x, self.y, 10, 10))

for i in range(1750):
    x = random.randrange(600)
    y = random.randrange(600)
    r = Unit(x,y)
    runners.append(r)
    grid[y // GRID_SIZE][x // GRID_SIZE].append(r)

while True:
    display.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    threshold_distance_squared = 10**2

    for i, runner1 in enumerate(runners):
        x, y = runner1.x // GRID_SIZE, runner1.y // GRID_SIZE
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < 20 and 0 <= ny < 20:
                    for runner2 in grid[ny][nx]:
                        if runner1 != runner2 and runner1.distance(runner2) < threshold_distance_squared:
                            if random.choice([True, False]):
                                runner1.color = runner2.color
                            else:
                                runner2.color = runner1.color

    for runner in runners:
        old_x, old_y = runner.x // GRID_SIZE, runner.y // GRID_SIZE
        runner.main(display)
        runner.move()
        new_x, new_y = runner.x // GRID_SIZE, runner.y // GRID_SIZE

        # Update grid if unit moved to a different cell
        if old_x != new_x or old_y != new_y:
            grid[old_y][old_x].remove(runner)
            grid[new_y][new_x].append(runner)

    clock.tick(100)
    pygame.display.update()
