import pygame
from pygame.locals import *
import random

pygame.init()
# game setup
GAME_RES = WIDTH, HEIGHT = 1000, 600
FPS = 120
GAME_TITLE = 'Default Game Title'

window = pygame.display.set_mode(GAME_RES, HWACCEL | HWSURFACE | DOUBLEBUF)
pygame.display.set_caption(GAME_TITLE)
clock = pygame.time.Clock()
# car img
car_img = pygame.image.load("./macchina.png")
car_img = pygame.transform.scale(car_img, (150, 100))
# player image
pl_img = pygame.image.load("./sprite.png")
pl_img = pygame.transform.scale(pl_img, (130, 80))
# background image
bgd = pygame.image.load("./strada.jpg")
bgd = pygame.transform.scale(bgd, (WIDTH, HEIGHT))
# end game setup

# Game Values
objects = {}
background_color = (150, 150, 150)  # RGB value


class Player(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH//2
        self.rect.y = HEIGHT - 100
        self.speed = 25

    def move(self, direction):
        if direction == "left":
            self.rect.x -= self.speed
        elif direction == "right":
            self.rect.x += self.speed
        elif direction == "up":
            self.rect.y -= self.speed


class Car(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x_speed = 0

    def move(self):
        self.rect.x += self.x_speed

    def reset(self):
        self.rect.x = 0 - 160

# instance car
cars = [
    Car(car_img, 0, 200),
    Car(car_img, 0, 300)
]

car_group = pygame.sprite.Group(*cars)
for c in car_group:
    # range excluded the last number
    c.x_speed = random.choice([*range(2, 6)])

# instance player
player = Player(pl_img)
player_group = pygame.sprite.GroupSingle(
    player
)
# End of Game Values

# Game loop
game_ended = False
while not game_ended:
    # Event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            game_ended = True
            break
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                game_ended = True
                break
            if event.key == K_w:
                player.move("up")
            if event.key == K_a:
                player.move("left")
            if event.key == K_d:
                player.move("right")
        # win point
        if player.rect.y <= 100:
            game_ended = True
            break
    # collision detection
    # car collide with right
    for car in cars:
        if car.rect.x > WIDTH:
            car.reset()
    # player collide with car group
    if pygame.sprite.groupcollide(player_group, car_group, True, False):
        game_ended = True
    # player collide with left
    if player.rect.x < 0:
        player.move("right")
    # player collide with right
    if player.rect.x + player.rect.width > WIDTH:
        player.move("left")
    # Display update
    pygame.Surface.fill(window, background_color)
    window.blit(bgd, (0, 0))
    for car in cars:
        car.move()
    player_group.draw(window)
    car_group.draw(window)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
exit(0)
