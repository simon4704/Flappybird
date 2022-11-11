# -*- coding: utf-8 -*-
"""
Created on Fri May  7 17:46:04 2021

@author: simon
"""

import pygame
import os
import math
import numpy as np

pygame.font.init()

os.chdir(os.getcwd())


WIDTH, HEIGHT = 900, 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy bird")


BLACK = (0,0,0)
WHITE = (255,255,255)

FPS = 60

BIRD_IMPORT = pygame.image.load('bird_done.PNG')
BIRD_SCALED = pygame.transform.scale(BIRD_IMPORT, (17*3,12*3))

PIPE_WIDTH, PIPE_HEIGHT = 23*3, 186*3

PIPE_BOTTOM_IMPORT = pygame.image.load('pipe_bottom.PNG')
PIPE_BOTTOM_SCALED = pygame.transform.scale(PIPE_BOTTOM_IMPORT, (PIPE_WIDTH, PIPE_HEIGHT))

PIPE_TOP_IMPORT = pygame.image.load('pipe_top.PNG')
PIPE_TOP_SCALED = pygame.transform.scale(PIPE_TOP_IMPORT, (PIPE_WIDTH, PIPE_HEIGHT))

GROUND_IMPORT = pygame.image.load('ground.PNG')
GROUND_SCALED = pygame.transform.scale(GROUND_IMPORT, (360*3, 6*3))

HOR_VEL = 5 # horizontal velocity


VERT_ACC = 5/10 # vertical acceleration



#%%

def draw_window(birdo, birdi, pillars, ground):
    WINDOW.fill(WHITE)
    
    # pygame.draw.rect(WINDOW, BLACK, birdo)
    WINDOW.blit(birdi, (birdo.x-(17*3)//2*0, birdo.y-5))
    
    for pillar in pillars:
        # pygame.draw.rect(WINDOW, BLACK, pillar)
        pass
    for i in range(3):
        WINDOW.blit(PIPE_BOTTOM_SCALED, (pillars[i].x, pillars[i].y))
        WINDOW.blit(PIPE_TOP_SCALED, (pillars[i].x, pillars[i].y-PIPE_HEIGHT-200))
        pass
    
    WINDOW.blit(GROUND_SCALED, (ground.x, ground.y))

    
    pygame.display.update()



#%%

def handle_bird_vel(keys_pressed, birdo, bird_vel, birdi, just_jumped):
    if keys_pressed[pygame.K_UP] and just_jumped == False and birdo.y < 50:
        bird_vel = -1
        just_jumped = True
        
    if keys_pressed[pygame.K_UP] and just_jumped == False and birdo.y > 50:
        bird_vel = -8
        just_jumped = True
        
    elif keys_pressed[pygame.K_UP] and just_jumped == True:
        bird_vel += VERT_ACC
        just_jumped = True
        
    else:
        bird_vel += VERT_ACC
        just_jumped = False
        
    return bird_vel


#%%

def handle_bird_pos(birdo, bird_vel):
    birdo.y += bird_vel


#%%

def handle_bird_angle(bird_vel, birdi):
    angle = math.atan(bird_vel/7)*(-1)
    birdi = pygame.transform.rotate(birdi, angle*180/math.pi)
    return birdi


#%%

def generate_pillars():
    pillar_pos = np.round(np.random.uniform(250, 450, 3))
    pillar_11 = pygame.Rect(900, pillar_pos[0], PIPE_WIDTH, 500-pillar_pos[0])
    pillar_12 = pygame.Rect(900, 0, PIPE_WIDTH, pillar_pos[0]-200)
    
    pillar_21 = pygame.Rect(900+(WIDTH+PIPE_WIDTH)//3, pillar_pos[1], PIPE_WIDTH, 500-pillar_pos[1])
    pillar_22 = pygame.Rect(900+(WIDTH+PIPE_WIDTH)//3, 0, PIPE_WIDTH, pillar_pos[1]-200)
    
    pillar_31 = pygame.Rect(900+(WIDTH+PIPE_WIDTH)//3*2, pillar_pos[2],PIPE_WIDTH, 500-pillar_pos[2])
    pillar_32 = pygame.Rect(900+(WIDTH+PIPE_WIDTH)//3*2, 0, PIPE_WIDTH, pillar_pos[2]-200)
    pillars = (pillar_11, pillar_21, pillar_31, pillar_12, pillar_22, pillar_32)
    
    return pillars


#%%

def move_pillar(pillars):
    index = 0
    for pillar in pillars:
        if pillar.x < -PIPE_WIDTH:
            pillar.x = 900
            if index == 0:
                pillar.y = np.round(np.random.uniform(250,450,1))[0]
                pillar.height = HEIGHT - pillar.y
                last_y = pillar.y
                index += 1
            else:
                pillar.height = last_y - 200
        else:
            pillar.x -= HOR_VEL


#%%

def move_ground(ground):
    if ground.x > -85:
        ground.x -= HOR_VEL
        # print("greater")
    else:
        ground.x = 0
        # print("less")


#%%

def check_collision(birdo, birdi, pillars, game_started):
    collision = False
    birdi = birdi
    game_started = True
    for pillar in pillars:
        if birdo.colliderect(pillar):
            collision = True
            break
    
    if birdo.y >= HEIGHT-12*2:
        collision = True
    
    if collision == True:
        pillars = generate_pillars()
        birdo.y = 300
        birdi = BIRD_SCALED
        game_started = False
    
    return birdi, game_started, pillars


#%%

def main():
    run = True
    clock = pygame.time.Clock()
    
    
    birdo = pygame.Rect(100, 300, 17*3-5, 12*3) # birdo means bird object
    bird_vel = float(0)
    birdi = BIRD_SCALED # birdi means bird image
    just_jumped = False

    pillars = generate_pillars()
    
    ground = pygame.Rect(0, HEIGHT-6*3, 1, 1)
    
    draw_window(birdo, birdi, pillars, ground)
    
    game_started = False
    
    
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        if game_started == False:
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_UP]:
                game_started = True
        
        
        if game_started == True:
            birdi = BIRD_SCALED # birdi means bird image
            
            keys_pressed = pygame.key.get_pressed()
            
            bird_vel = handle_bird_vel(keys_pressed, birdo, bird_vel, birdi, just_jumped)
            handle_bird_pos(birdo, bird_vel)
            birdi = handle_bird_angle(bird_vel, birdi)
            
            move_pillar(pillars)
            move_ground(ground)
            
            birdi, game_started, pillars = check_collision(birdo, birdi, pillars, game_started)
            
            
            draw_window(birdo, birdi, pillars, ground)







    pygame.quit()



if __name__ == "__main__":
    main()
    

