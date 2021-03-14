import pygame
import random

pygame.init()
display_width = 800
display_height = 600
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Space War")
clock = pygame.time.Clock()

background = pygame.image.load("background.png")
enemy = pygame.image.load("enemy.png")
player = pygame.image.load("player.png")
bullet = pygame.image.load("bullet.png")

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
light_red = (255,0,0)
yellow = (200,200,0)
light_yellow = (255,255,0)
green = (0,255,0)
light_green = (0,255,0)
orange = (155,200,0)

smallfont = pygame.font.Font("freesansbold.ttf",20)
medfont = pygame.font.Font("freesansbold.ttf",30)
largefont = pygame.font.Font("freesansbold.ttf",50)

def text_objects(text, color, size):
    if (size == "small"):
        textSurface = smallfont.render(text, True, color)
    elif (size == "medium"):
        textSurface = medfont.render(text, True, color)
    elif (size == "large"):
        textSurface = largefont.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_to_screen(msg, color, y_displace=0, size="small"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = int(display_width/2),int(display_height/2)+y_displace
    gameDisplay.blit(textSurf, textRect)

def show_score(score):
    text = smallfont.render("Score: "+str(score), True, black)
    gameDisplay.blit(text, [int(display_width/2),0])

def won(score,exp_x,exp_y):
    won = True
    explosion(exp_x,exp_y)
    message_to_screen("You Won", red, -50, "large")
    message_to_screen("Score "+str(score), green, 0, "medium")
    message_to_screen("Press r to restart the game", black, 25, "small")
    pygame.display.update()
    while won:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                quit()
            if (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_r):
                    game_loop()
        
        clock.tick(5)

def explosion(x, y, size=75):
    # ptgame.mixer.Sound.play(explosion_sound)
    explode = True
    while explode:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        startPoint = x,y
        colorChoices = [red, light_red, yellow, light_yellow]
        magnitude = 1
        while (magnitude < size):
            exploding_bit_x = x+random.randrange(-1*magnitude,magnitude)
            exploding_bit_y = y+random.randrange(-1*magnitude,magnitude)
            pygame.draw.circle(gameDisplay, colorChoices[random.randrange(0,4)], (exploding_bit_x,exploding_bit_y), random.randrange(1,5))
            magnitude += 1
            pygame.display.update()
            clock.tick(100)
        explode = False

def game_over(score,player_x,player_y):
    over = True
    explosion(player_x,player_y)
    message_to_screen("Game Over", red, -50, "large")
    message_to_screen("Score "+str(score), green, 0, "medium")
    message_to_screen("Press r to restart the game", black, 25, "small")
    pygame.display.update()
    while over:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                quit()
            if (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_r):
                    game_loop()
        
        clock.tick(5)

def bullet_hit(bullet_pos,enemy_x,enemy_y):
    damage = 0
    if (enemy_x<=bullet_pos[0]<=enemy_x+enemy.get_width() and
        enemy_y<=bullet_pos[1]<=enemy_y+enemy.get_height()):
        del bullet_pos
        damage = 1
    return damage

def collision(player_x,player_y,enemy_beam,score):
    if (player_x<=enemy_beam[0]<=player_x+player.get_width() and player_y<=enemy_beam[1]<=player_y+player.get_height()):
        game_over(score,player_x+int(player.get_width()/2),player_y+int(player.get_height()/2))

def game_loop():
    health = 100
    
    enemy_x = int((display_width-enemy.get_width())/2)
    enemy_y = int(display_height/10)
    enemy_x_change = 3
    beam_x = int(display_width/2)
    beam_y = enemy_y+enemy.get_height()
    enemy_beam = []

    player_x = int((display_width-player.get_width())/2)
    player_y = int(display_height/10)*8
    player_x_change = 0
    player_y_change = 0
    
    #bullet_state = "ready"
    bullet_pos = []
    bullet_y_change = -8
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_x_change = -5
                if event.key == pygame.K_RIGHT:
                    player_x_change = 5
                if event.key == pygame.K_UP:
                    player_y_change = -10
                if event.key == pygame.K_DOWN:
                    player_y_change = 10
                if event.key == pygame.K_SPACE:
                    bullet_pos.append([player_x+int((player.get_width()-bullet.get_width())/2),player_y])
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player_x_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player_y_change = 0

        gameDisplay.fill(white)
        gameDisplay.blit(background,(0,0))
        enemy_x += enemy_x_change
        player_x += player_x_change
        player_y += player_y_change
        gameDisplay.blit(enemy,(enemy_x,enemy_y))
        gameDisplay.blit(player,(player_x,player_y))
        
        if (enemy_x+enemy.get_width() >= display_width):
            enemy_x_change = -3
        elif (enemy_x <= 0):
            enemy_x_change = 3
        if (player_x+player.get_width() > display_width):
            player_x = display_width-player.get_width()
        elif (player_x < 0):
            player_x = 0
        if (player_y+player.get_height() > display_height):
            player_y = display_height-player.get_height()
        elif (player_y < 300):
            player_y = 300

        if (enemy_x == int((display_width-enemy.get_width())/2)):
            enemy_beam.append([beam_x,beam_y,-6,0])
            enemy_beam.append([beam_x,beam_y,-5,1])
            enemy_beam.append([beam_x,beam_y,-4,2])
            enemy_beam.append([beam_x,beam_y,-3,3])
            enemy_beam.append([beam_x,beam_y,-2,4])
            enemy_beam.append([beam_x,beam_y,-1,5])
            enemy_beam.append([beam_x,beam_y,0,6])
            enemy_beam.append([beam_x,beam_y,1,5])
            enemy_beam.append([beam_x,beam_y,2,4])
            enemy_beam.append([beam_x,beam_y,3,3])
            enemy_beam.append([beam_x,beam_y,4,2])
            enemy_beam.append([beam_x,beam_y,5,1])
            enemy_beam.append([beam_x,beam_y,6,0])
            

        for i in range(len(enemy_beam)):
            pygame.draw.circle(gameDisplay,yellow,(enemy_beam[i][0],enemy_beam[i][1]),5)
            enemy_beam[i][0] += enemy_beam[i][2]
            enemy_beam[i][1] += enemy_beam[i][3]
            collision(player_x,player_y,enemy_beam[i],100-health)
            #if (enemy_beam[i][0]<0 or enemy_beam[i][0]>display_width or enemy_beam[i][1]>display_height):
            #    del enemy_beam[i]

        for i in range(len(bullet_pos)):
            gameDisplay.blit(bullet,(bullet_pos[i][0],bullet_pos[i][1]))
            bullet_pos[i][1] += bullet_y_change
            damage = bullet_hit(bullet_pos[i],enemy_x,enemy_y)
            health -= damage
            #if (bullet_pos[i][1] < 0):
            #    del bullet_pos[i]

        show_score(100-health)
        if (health <= 0):
            won(100-health,enemy_x+int(enemy.get_width()/2),enemy_y+int(enemy.get_height()/2))

        pygame.display.update()
        clock.tick(60)

game_loop()
pygame.quit()
quit()
