#Code written by Patrick Ledoit in its entirity - 15-10-20
#Wall evading game
#Follow instructions once the code has been executed
#Change line 353, to = 48 to hear one more song and make it more difficult ;)
#Line 71 You can change the path to 'assets/main_char2' or char3,4,5 for a different character
#Can you beat the game?



# The MIT License (MIT)
# Copyright © 2020 <Patrick Ledoit>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import pygame, sys, random, time

#Vars
#Display
width = 500
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
game_active = True
tick_rate = 60
game_won = False
faded = False
animationed = False
limit = True
music = False

#Sq mov calc
x = width//2
y = width//2
x_change = 0
y_change = 0
speed = 2

#Wall
coordslist = list(range(10,500,20))
gapslist = list(range(20,45,5))
xwall_list = []
ywall_list = []
lvl = 1
altlvl = 1
wall_counter = 0
wall_kill = False
wall_delay = 0

#score
high_score = 0
#Vars end

pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 16, buffer = 512)

pygame.init()

#Pygame vars
screen = pygame.display.set_mode((width,width))
clock = pygame.time.Clock()
pygame.display.set_caption('WallZ')
#Pygame vars end

#Texts:


#Assets
sq_surface = pygame.image.load('assets/main_char.png').convert_alpha()#You can change the path to 'assets/main_char2' for a different character or char3,4,5
sq_surface = pygame.transform.scale2x(sq_surface)
sq_rect = sq_surface.get_rect(center = (width//2, width//2))

xwall_surface = pygame.image.load('assets/xwall.png').convert_alpha()
xwall_surface = pygame.transform.scale2x(xwall_surface)

ywall_surface = pygame.image.load('assets/ywall.png').convert_alpha()
ywall_surface = pygame.transform.scale2x(ywall_surface)

game_font = pygame.font.Font('assets/MonsterFriendFore.otf',15)
game_font_big = pygame.font.Font('assets/MonsterFriendFore.otf',35)

rain_surface = pygame.image.load('assets/rain.jpg').convert_alpha()
rain_surface = pygame.transform.smoothscale(rain_surface, (width,width))

death_sound = pygame.mixer.Sound('sound/snd_heartshot.wav')
lvlup_sound = pygame.mixer.Sound('sound/snd_textnoise.wav')
score_sound = pygame.mixer.Sound('sound/snd_credit_s.wav')
fade_sound = pygame.mixer.Sound('sound/mus_intronoise.ogg')
win_sound = pygame.mixer.Sound('sound/snd_ballchime.ogg')

#Assets end

#Get coords
def get_coords():
    if altlvl == 1:
        coordx = random.choice(coordslist)
        coordy = random.choice(coordslist)
    elif altlvl == 2:
        coordx = random.choice(coordslist[len(coordslist)//3:])
        coordy = random.choice(coordslist[len(coordslist)//3:])

    gapx = random.choice(gapslist)
    gapy = random.choice(gapslist)

    return coordx, coordy, gapx, gapy

#Create lWall
def create_lwall(random_wall_pos,gap):
    bot_wall = xwall_surface.get_rect(midtop = (-10,random_wall_pos+gap))
    top_wall = xwall_surface.get_rect(midbottom = (-10,random_wall_pos-gap))
    return bot_wall, top_wall

def move_lwall(walls):
    for wall in walls:
        wall.centerx+=speed//2
    return walls

#Create Twall
def create_twall(random_wall_pos,gap):
    left_wall = ywall_surface.get_rect(midright = (random_wall_pos-gap,-10))
    right_wall = ywall_surface.get_rect(midleft = (random_wall_pos+gap,-10))
    return left_wall, right_wall

def move_twall(walls):
    for wall in walls:
        wall.centery+=speed//2
    return walls

def draw_xwalls(walls):
    counter = 0
    for wall in walls:
        screen.blit(xwall_surface,wall)

def draw_ywalls(walls):
    for wall in walls:
        screen.blit(ywall_surface,wall)

#Collisions
def check_collisions(walls):
    for wall in walls:
        if sq_rect.colliderect(wall):
            death_sound.play()
            return False
    return True

#score display
def score_display(game_state):
    if game_state == 'main_game':
        score_surface,score_rect = text(str(wall_counter),False,(90,90,90),(width//2,50))
        screen.blit(score_surface,score_rect)

    if game_state == 'game_over':
        score_surface,score_rect = text(f'Score: {wall_counter}',False,(90,90,90),(width//2,50))
        screen.blit(score_surface,score_rect)

        highscore_surface = game_font.render(f'High Score: {high_score}',True,(0,0,0))
        highscore_rect = highscore_surface.get_rect(center = (width//2,420))
        screen.blit(highscore_surface,highscore_rect)

        help_surface = game_font.render(f'[Press SPACE to restart]',True,(0,0,0))
        help_rect = help_surface.get_rect(center = (width//2,450))
        screen.blit(help_surface,help_rect)

        over_surface = game_font_big.render(f'GAME OVER',True, white)
        over_rect = over_surface.get_rect(center = (width//2,width//2))
        screen.blit(over_surface,over_rect)

        over2_surface = game_font_big.render(f'[',True, red)
        over2_rect = over_surface.get_rect(center = (width//2+width//4+5, width//2+40))
        screen.blit(over2_surface,over2_rect)
        over2_surface = game_font_big.render(f'[',True, black)
        over2_rect = over_surface.get_rect(center = (width//2+width//4+5, width//2+40))
        screen.blit(over2_surface,over2_rect)
        over2_surface = game_font_big.render(f',',True, red)
        over2_rect = over_surface.get_rect(center = (width//2+width//4+20, width//2+20))
        screen.blit(over2_surface,over2_rect)
        over2_surface = game_font.render(f',',True, red)
        over2_surface = pygame.transform.flip(over2_surface,True,False)
        over2_rect = over_surface.get_rect(center = (width//2+width//4+12, width//2+55))
        screen.blit(over2_surface,over2_rect)


def update_score(wall_counter,high_score):
    if wall_counter>high_score:
        high_score = wall_counter

    return high_score
#score display

def text(string,big,color,loc):

    if big:
        surface = game_font_big.render(string,True,color)
        rect = surface.get_rect(center = loc)
        return surface,rect
    else:
        surface = game_font.render(string,True,color)
        rect = surface.get_rect(center = loc)
        return surface,rect

def fade(width, height,sq_surface):
    fade = pygame.Surface((width, height))
    fade.fill((0,0,0))
    sq_rect =  sq_surface.get_rect(center = (width//2,width//2))
    for alpha in range(0, 255):
        fade.set_alpha(alpha)
        sq_surface.set_alpha(alpha)
        screen.blit(fade, (0,0))
        screen.blit(sq_surface,sq_rect)
        pygame.display.update()
        pygame.time.delay(10)

    return fade

#Start menu:
welcome_surface = game_font.render('YOU ARE TRAPPED IN THE ',True,white)
welcome_rect = welcome_surface.get_rect(center = (width//2-30,50))

welcome_surface3 = game_font.render('WALLZ',True,red)
welcome_rect3 = welcome_surface3.get_rect(center = (width//2+160,50))

welcome_surface2 = game_font.render('can you escape?',True,white)
welcome_rect2 = welcome_surface2.get_rect(center = (width//2,100))


arrow_surface = game_font.render('Use Arrows Keys',True,white)
arrow_rect = arrow_surface.get_rect(center = (width//2,width//2-15))
screen.blit(arrow_surface,arrow_rect)

arrow2_surface = game_font.render('To Move',True,white)
arrow2_rect = arrow2_surface.get_rect(center = (width/2,width//2+15))
screen.blit(arrow2_surface,arrow2_rect)

space_surface = game_font.render('Press SPACE To Start',True,white)
space_rect = space_surface.get_rect(center = (width/2,width-width//4))
screen.blit(space_surface,space_rect)

space2_surface = game_font.render('[IF YOU DARE]',True,black)
space2_rect = space2_surface.get_rect(center = (width/2,width-width//4+25))
screen.blit(space2_surface,space2_rect)

start = True
pygame.mixer.music.load('sound/DeterminationUT.mp3')
pygame.mixer.music.play()
MUSIC_END2 = pygame.USEREVENT+2
pygame.mixer.music.set_endevent(MUSIC_END2)
while start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        #movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                start = False

        if event.type == MUSIC_END2:
            pygame.mixer.music.load('sound/DeterminationUT.mp3')
            pygame.mixer.music.play()

    screen.blit(rain_surface,(0,0))

    screen.blit(welcome_surface,welcome_rect)
    screen.blit(welcome_surface2,welcome_rect2)
    screen.blit(welcome_surface3,welcome_rect3)

    screen.blit(arrow_surface,arrow_rect)
    screen.blit(arrow2_surface,arrow2_rect)

    screen.blit(space_surface,space_rect)
    screen.blit(space2_surface,space2_rect)

    pygame.display.update()
    clock.tick(tick_rate)

#Start game
SPAWNWALL = pygame.USEREVENT
pygame.time.set_timer(SPAWNWALL,3000) #in ms
MUSIC_END = pygame.USEREVENT+1

while True:

    #Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        #movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_change = -speed
                #print('left')
            elif event.key == pygame.K_RIGHT:
                x_change = speed
                #print('right')
            elif event.key == pygame.K_UP:
                y_change = -speed
                #print('up')
            elif event.key == pygame.K_DOWN:
                y_change = speed
                #print('down')
            elif event.key == pygame.K_SPACE and not game_active:
                pygame.mixer.music.stop()
                fade_sound.play()
                time.sleep(1)
                if random.choice([0,1]) == 0:
                    pygame.mixer.music.load('sound/MEGALOVANIA UT.mp3')
                    pygame.mixer.music.play()
                else:
                    pygame.mixer.music.load('sound/Battle Against A True Hero UT.mp3')
                    pygame.mixer.music.play()
                pygame.mixer.music.set_endevent(MUSIC_END)

                game_active = True
                xwall_list.clear()
                ywall_list.clear()
                x_change = 0
                y_change = 0
                speed = 2
                lvl = 1
                altlvl = 1
                wall_counter = 0
                wall_kill = False
                wall_delay = 0

                sq_rect.center = (width//2,width//2)
                #print('space')


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                x_change = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                y_change = 0

        if event.type == MUSIC_END and game_active and not faded:
            pygame.mixer.music.play()
        #Movement end

        #Wall
        if event.type == SPAWNWALL and game_active and not game_won:

            wall_counter += 1

            if wall_delay == 0:

                coordx, coordy, gapx, gapy = get_coords()
                #print(coordx, coordy, gapx, gapy)
                if wall_counter == 30:#Change this to 48 to hear one more song and make it more difficult ;)
                    fade_sound.play()
                    game_won = True

                elif wall_counter % 12 == 0:
                    lvlup_sound.play()
                    lvl += 1
                    wall_delaylvl = 1
                    wall_kill = False
                    altlvl = min(lvl,2)
                    if lvl > 2:
                        tick_rate += 30
                    #print('Level UP')
                elif wall_counter % 2 ==0:
                    score_sound.play()

                if altlvl == 1:
                    xwall_list.extend(create_lwall(coordy,gapy))

                if altlvl == 2:
                    if wall_delaylvl == 0:
                        xwall_list.extend(create_lwall(coordy,gapy))
                        ywall_list.extend(create_twall(coordx,gapx))
                    else:
                        if wall_counter % 12 !=0:
                            wall_delaylvl -= 1
                            wall_counter -= 1
                    #print(wall_delay,wall_counter,wall_kill,altlvl,lvl)

                if not wall_kill and (wall_counter % 12 == 4):
                    wall_kill = True

                if wall_kill:
                    if altlvl == 1:
                        xwall_list.pop(0)
                        xwall_list.pop(0)
                    if altlvl == 2:
                        xwall_list.pop(0)
                        xwall_list.pop(0)
                        ywall_list.pop(0)
                        ywall_list.pop(0)
            else:
                wall_counter -=1

            wall_delay += 1
            if wall_delay == altlvl:
                wall_delay = 0
        #wall end
    #events end

    #sq move calcs end
    if x_change > 0:#right
        if sq_rect.centerx < width-10:#has to be left
            sq_rect.centerx += x_change#ok
    else:#left
        if sq_rect.centerx > 10 and limit:#has to be right
            sq_rect.centerx += x_change#ok
        elif not limit:
            sq_rect.centerx += x_change

    if y_change > 0:#down
        if sq_rect.centery < width-10:#has to be up
            sq_rect.centery += y_change#ok
    else:#up
        if sq_rect.centery > 10:#has to be down
            sq_rect.centery += y_change#ok
    #sq move calcs end

    #screen.fill(white)
    screen.blit(rain_surface,(0,0))

    if game_active and not game_won:
        #display
        screen.blit(sq_surface,sq_rect)

        #collision
        game_active = check_collisions(xwall_list) and check_collisions(ywall_list)

        if altlvl == 1:
            xwall_list = move_lwall(xwall_list)
            draw_xwalls(xwall_list)

        if altlvl == 2:
            xwall_list = move_lwall(xwall_list)
            draw_xwalls(xwall_list)
            ywall_list = move_twall(ywall_list)
            draw_ywalls(ywall_list)

        score_display('main_game')

    elif not game_active and not game_won:
        pygame.mixer.music.stop()
        high_score = update_score(wall_counter,high_score)
        score_display('game_over')

    elif game_won and not faded and not animationed:
        pygame.mixer.music.stop()
        tick_rate = 60
        fade_surface = fade(width,width,sq_surface)
        faded = True
        sq_rect.centery = width//2
        sq_rect.centerx = width//2


    elif game_won and faded and not animationed:
        screen.blit(fade_surface,(0,0))
        screen.blit(sq_surface,sq_rect)
        limit = False
        win_surface, win_rect = text('freedom ?', False,(90,90,90),(width//2,width//2+100))
        screen.blit(win_surface,win_rect)

        if sq_rect.centerx <= -10:
            animationed = True
            win_sound.play()

    elif game_won and faded and animationed:
        screen.blit(fade_surface,(0,0))
        win_surface, win_rect = text('YOU WIN', True,red,(width//2,width//2))
        screen.blit(win_surface,win_rect)

    pygame.display.update()
    clock.tick(tick_rate)
    #display end

    if not music:
        pygame.mixer.music.stop()
        fade_sound.play()
        time.sleep(1)

        pygame.mixer.music.load('sound/MEGALOVANIA UT.mp3')
        pygame.mixer.music.play()
        pygame.mixer.music.set_endevent(MUSIC_END)
        music = True
