import pygame
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Brick breaker")

font = pygame.font.Font('freesansbold.ttf', 32)

#creating all the bricks, true means 'not destroyed', the latter part indicates position
brick_list = []
for i in range(16):
    brick_list.append([True, (i*50, 50)])
for i in range(15):
    brick_list.append([True, (25 + i*50, 75)])
for i in range(16):
    brick_list.append([True, (i*50, 100)])
for i in range(15):
    brick_list.append([True, (25 + i*50, 125)])

brickImg = pygame.image.load("brick.png")

platformImg = pygame.image.load("ball_holder_platform.png")
platformImg2 = pygame.transform.scale(platformImg, (100, 80))
platformX = 350
platformY = 550
platformX_change = 0

ballImg = pygame.image.load("ball.png")
ballImg2 = pygame.transform.scale(ballImg, (25, 25))
ballX = 388
ballY = 525
ballX_change = .5
ballY_change = -.5

game_state = 'pause'

score = 0
num_of_bricks = 62
point_font = pygame.font.Font('freesansbold.ttf', 16)

def show_score():
    score_render = point_font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_render, (10, 10))

def show_platform(x, y):
    screen.blit(platformImg2, (x, y))

def show_ball(x, y):
    screen.blit(ballImg2, (x, y))

def show_game_over():
    over_text = font.render("GAME OVER!", True, (255, 255, 255))
    screen.blit(over_text, (300, 250))

def show_pause_play_msg():
    msg = font.render("Press 'Space' to pause or play", True, (255, 255, 255))
    screen.blit(msg, (180, 250))

def show_game_complete():
    msg = font.render("Game complete!", True, (255, 255, 255))
    screen.blit(msg, (300, 250))

def show_all_bricks():      #'not destroyed' bricks
    for brick in brick_list:
        if brick[0] == True:
            screen.blit(brickImg, brick[1])



running = True
while running:

    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                platformX_change = -1
            if event.key == pygame.K_RIGHT:
                platformX_change = 1
            if event.key == pygame.K_SPACE:
                if game_state == 'play':
                    game_state = 'pause'
                elif game_state == 'pause':
                    game_state = 'play'

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                platformX_change = 0

    if game_state == 'play':
        platformX += platformX_change

        if platformX < 0:
            platformX = 0
        elif platformX > 700:
            platformX = 700


        ballX += ballX_change
        ballY += ballY_change

        #reflect in the left, right and top wall
        if ballX <= 0 or ballX >= 787.5:
            ballX_change *= -1
        if ballY <= 0:
            ballY_change *= -1

        #reflect and break the bricks
        for brick in brick_list:
             if brick[0] == True:           #brick exists
                 if ballY_change < 0:       #going upward, collision on the bottom of the brick
                    if brick[1][1] + 25 == ballY and brick[1][0] <= ballX+12.5 <= brick[1][0]+50:
                        brick[0] = False
                        ballY_change *= -1
                        score += 1
                        explosion_sound = mixer.Sound('explosion.wav')
                        explosion_sound.play()
                 elif ballY_change > 0:     #going downward, collision on the top of the brick
                    if ballY+25 == brick[1][1] and brick[1][0] <= ballX+12.5 <= brick[1][0]+50:
                        brick[0] = False
                        ballY_change *= -1
                        score += 1
                        explosion_sound = mixer.Sound('explosion.wav')
                        explosion_sound.play()

                 #collision on side of the brick, both left and right
                 if (brick[1][0] == ballX+12.5 or brick[1][0]+50 == ballX) and (brick[1][1] <= ballY+12.5 <= brick[1][1]+25):
                    brick[0] = False
                    ballX_change *= -1
                    score += 1
                    explosion_sound = mixer.Sound('explosion.wav')
                    explosion_sound.play()

        #game complete condition
        if score == num_of_bricks:
            game_state = 'complete'

        #reflect on platform
        if ballY == 525 and platformX <= (ballX+12.5) <= (platformX + 100):
            ballY_change *= -1
            bullet_sound = mixer.Sound('laser.wav')
            bullet_sound.play()

        #game over condition
        if ballY > 575:
            game_state = 'game_over'

    elif game_state == 'pause':
        show_pause_play_msg()

    elif game_state == 'complete':
        show_game_complete()

    elif game_state == 'game_over':
        show_game_over()

    show_score()
    show_platform(platformX, platformY)
    show_ball(ballX, ballY)
    show_all_bricks()

    pygame.display.update()
