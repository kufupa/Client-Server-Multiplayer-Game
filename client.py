import pygame
import os
from network import Network # import Network class from network.py


pygame.init() # initiliase all pygame modules
pygame.font.init()  # for displaying text
pygame.mixer.init()  # for playing sounds

# Font constants
HEALTH_FONT = pygame.font.SysFont("comicsans", 40)
WINNER_FONT = pygame.font.SysFont("comicsans", 100)

# Sound constants
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Grenade+1.mp3"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Gun+Silencer.mp3"))

# Window constants
WIDTH, HEIGHT = 960, 540
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First ever pygame attempt!")
FPS = 60

# Colour constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Bullet constants
BULLET_VEL = 8
MAX_BULLETS = 5

# Constant for border Rect
BORDER = pygame.Rect(WIDTH // 2 - 10, 0, 20, HEIGHT)
# position, then size - https://pygame.readthedocs.io/en/latest/rect/rect.html

# Ship constants
VEL = 5
SHIP_WIDTH, SHIP_HEIGHT = 60, 50

# Custom pygame events
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# Load and transform images
YELLOW_SHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_yellow.png"))
YELLOW_SHIP = pygame.transform.rotate(
    pygame.transform.scale(YELLOW_SHIP_IMAGE, (SHIP_WIDTH, SHIP_HEIGHT)), 90
)

RED_SHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_red.png"))
RED_SHIP = pygame.transform.rotate(
    pygame.transform.scale(RED_SHIP_IMAGE, (SHIP_WIDTH, SHIP_HEIGHT)), 270
)

SPACE = pygame.transform.scale(
    pygame.image.load(os.path.join("Assets", "space.png")), (WIDTH, HEIGHT)
)

class Player():
    def __init__(self, which):
        
        self.which = which # yellow = 1, red = 0
        # (775, 300) for red, (100, 300) for yellow
        if self.which == 1: # im yellow
            self.rect = pygame.Rect(100, 300, SHIP_WIDTH, SHIP_HEIGHT) # yellow player
        else: # im red
            self.rect = pygame.Rect(775, 300, SHIP_WIDTH, SHIP_HEIGHT) # red player


        if self.which == 1: # if im yellow
            self.ship = YELLOW_SHIP
        else:
            self.ship = RED_SHIP
        self.health = 5
        self.firing = 0
        self.bullets = []
        

    def handle_movement(self, keys_pressed):
        if self.which == 0:
        # arrow keys for red ship (one on the right)
            if (
                keys_pressed[pygame.K_LEFT] and self.rect.x - VEL > BORDER.x + BORDER.width
            ):  # left, decreasing x axis
                self.rect.x -= VEL
            if (
                keys_pressed[pygame.K_RIGHT] and self.rect.x + VEL + self.rect.width < WIDTH
            ):  # right, increasing x axis
                self.rect.x += VEL
            if keys_pressed[pygame.K_UP] and self.rect.y - VEL > 0:  # up, decreasing y axis
                self.rect.y -= VEL
            if (
                keys_pressed[pygame.K_DOWN] and self.rect.y + VEL + self.rect.height < HEIGHT
            ):  # down, increasing y axis
                self.rect.y += VEL
            

        else:
                # wasd is for the yellow spaceship (one on the left)
            if (
                keys_pressed[pygame.K_a] and self.rect.x - VEL > 0
            ):  # "a" key, left, decreasing x axis
                self.rect.x -= VEL
            if (
                keys_pressed[pygame.K_d] and self.rect.x + VEL + self.rect.width < BORDER.x
            ):  # "d" key, right, increasing x axis
                self.rect.x += VEL
            if (
                keys_pressed[pygame.K_w] and self.rect.y - VEL > 0
            ):  # "w" key, up, decreasing y axis
                self.rect.y -= VEL
            if (
                keys_pressed[pygame.K_s] and self.rect.y + VEL + self.rect.height < HEIGHT
            ):  # "s" key, down, increasing y axis
                self.rect.y += VEL
        
    def bullet_update(self, info):
        if info == 1:
            if self.firing == 0:
                self.firing = 1
                if self.which == 1: # if its yellow
                    if len(self.bullets) < MAX_BULLETS:
                        bullet = pygame.Rect(
                            self.rect.x + self.rect.width,
                            self.rect.y + self.rect.height // 2 - 2,
                            10,
                            5,
                        )
                        self.bullets.append(bullet)
                        BULLET_FIRE_SOUND.play()
                else:
                    if len(self.bullets) < MAX_BULLETS:
                        bullet = pygame.Rect(self.rect.x, self.rect.y + self.rect.height // 2 - 2, 10, 5)
                        self.bullets.append(bullet)
                        BULLET_FIRE_SOUND.play()

        else:
            self.firing = 0

        




def draw_window(p1, p2):
    WIN.blit(SPACE, (0, 0))

    if p1.which == 1:
        red_health_text = HEALTH_FONT.render("Health: " + str(p2.health), 1, WHITE)
        yellow_health_text = HEALTH_FONT.render("Health: " + str(p1.health), 1, WHITE)
    else:
        red_health_text = HEALTH_FONT.render("Health: " + str(p1.health), 1, WHITE)
        yellow_health_text = HEALTH_FONT.render("Health: " + str(p2.health), 1, WHITE)

    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))


    WIN.blit(p2.ship, (p2.rect.x, p2.rect.y))
    WIN.blit(p1.ship, (p1.rect.x, p1.rect.y))
    pygame.draw.rect(WIN, BLACK, BORDER)

    if p1.which == 0:
        for bullet in p1.bullets:
            pygame.draw.rect(WIN, RED, bullet)
        for bullet in p2.bullets:
            pygame.draw.rect(WIN, YELLOW, bullet)
    else:
        for bullet in p2.bullets:
            pygame.draw.rect(WIN, RED, bullet)
        for bullet in p1.bullets:
            pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def draw_winner(winner_text):
    draw_text = WINNER_FONT.render(winner_text, 1, WHITE)
    WIN.blit(
        draw_text,
        (
            (WIDTH / 2 - draw_text.get_width() // 2), # in the middle of the screen
            (HEIGHT / 2 - draw_text.get_height() // 2),
        ),
    )
    pygame.display.update()
    pygame.time.delay(3000)

def handle_bullets(p1, p2):
    # Checks for collisions
    for bullet in p1.bullets:
        bullet.x += BULLET_VEL
        if p2.rect.colliderect(bullet):
            # pygame.event.post(pygame.event.Event(RED_HIT))
            p1.bullets.remove(bullet)
            p2.health -= 1
        elif bullet.x > WIDTH:
            p1.bullets.remove(bullet)

    for bullet in p2.bullets:
        bullet.x -= BULLET_VEL
        if p1.rect.colliderect(bullet):
            # pygame.event.post(pygame.event.Event(YELLOW_HIT))
            p2.bullets.remove(bullet)
            p1.health -= 1
        elif bullet.x < 0:
            p2.bullets.remove(bullet)

# Function for networking aspect

def read_pos(str):
    spl = str.split(", ")
    return int(spl[0]), int(spl[1]), int(spl[2]), int(spl[3])

def make_pos(tuple):
    return str(tuple[0]) + ", " + str(tuple[1]) + ", " + str(tuple[2]) + ", " + str(tuple[3])


def game():

    n = Network()
    
    me_which = int(n.getPos()) # initilially i dont have to read pos as it jus tells whether im red or yellow, yellow = 1, red = 0
    he_which = (me_which + 1) % 2 # make sure its diff to the other

    p1 = Player(me_which)
    p2 = Player(he_which)

    clock = pygame.time.Clock()
    run = True
    while run:

        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if p1.which == 1: # if its yellow
                    if event.key == pygame.K_LCTRL and len(p1.bullets) < MAX_BULLETS:
                        bullet = pygame.Rect(
                            p1.rect.x + p1.rect.width,
                            p1.rect.y + p1.rect.height // 2 - 2,
                            10,
                            5,
                        )
                        p1.bullets.append(bullet)
                        BULLET_FIRE_SOUND.play()
                        p1.firing = 1
                else:
                    if event.key == pygame.K_RCTRL and len(p1.bullets) < MAX_BULLETS:
                        bullet = pygame.Rect(p1.rect.x, p1.rect.y + p1.rect.height // 2 - 2, 10, 5)
                        p1.bullets.append(bullet)
                        BULLET_FIRE_SOUND.play()
                        p1.firing = 1

            if event.type == pygame.KEYUP:
                if p1.which == 1: # if its yellow
                    if event.key == pygame.K_LCTRL:
                        p1.firing = 0
                else:
                    if event.key == pygame.K_RCTRL:
                        p1.firing = 0


        # END OF EVENTS FOR LOOP

        if p1.health <= 0:
                winner_text = "Your opponent Wins!"
                draw_winner(winner_text)
                run = False
                pygame.quit()

        elif p2.health <= 0:
            winner_text = "You Win!"
            draw_winner(winner_text)
            run = False
            pygame.quit()

        keys_pressed = pygame.key.get_pressed()

        # networking code
        p2Pos = read_pos(n.send(make_pos((p1.rect.x, p1.rect.y, p1.firing, p1.health)))) # send and recieve positions
        p2.rect.x = p2Pos[0]
        p2.rect.y = p2Pos[1]
        p2.bullet_update(p2Pos[2])
        p2.health = p2Pos[3]


        p1.handle_movement(keys_pressed)

        if p1.which == 1:
            handle_bullets(p1, p2)
        else:
            handle_bullets(p2, p1)

        draw_window(p1, p2)

    pygame.quit()


if __name__ == "__main__": # use __main__ no matter file name
    game()
