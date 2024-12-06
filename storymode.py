import pygame
from pygame.locals import *
import os, sys
from AxionsJourney import *
import random

mainClock = pygame.time.Clock()
pygame.init()

WINDOWWIDTH = 600
WINDOWHEIGHT = 600
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption("Axion's Journey")


def run_level(level, GAME, BLACKOUT, CHECKPOINT, DEATH, FINISH, hit, song):

    pygame.mixer.music.load(song)

    pygame.mixer.music.play(-1)

    player = level.get_player_object()
    fadeout_frames = -1
    fadein_frames = 180

    while True:
        # FIRST
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if event.key == K_r:
                    player.reset_to_checkpoint()

                if event.key == K_e:
                    if level.is_writing:
                        level.is_writing = False
                        for block in level.text_blocks:
                            block.is_writing = False
                    else:
                        for block in level.text_blocks:
                            if block.check_touching_player(player) and not block.is_writing:
                                block.is_writing = True
                                level.is_writing = True
                                break
                            

            elif event.type == CHECKPOINT:
                for block in level.block_object_list:
                    if isinstance(block, CheckpointBlock):
                        block.declaim()

            elif event.type == DEATH:
                level.death_particles(player)
                GAME.camera.screenshake_intensity = 18
                hit.play()

            elif event.type == FINISH:
                player = None
                fadeout_frames = 300
                pygame.mixer.music.fadeout(6000)

        
        if fadeout_frames > -1:
            fadeout_frames -= 1
            BLACKOUT.fade_out(fadeout_frames, 300)
            if fadeout_frames == 0:
                break
        elif fadein_frames > 0:
            fadein_frames -= 1
            BLACKOUT.fade_in(fadein_frames, 180)
    
        
        keys = pygame.key.get_pressed()

        if player != None and fadein_frames == 0:
            if player.dead == 0:
                if not level.is_writing:
                    player.main_loop(keys, level, DEATH, FINISH)
            else:
                player.dead -= 1
                if player.dead == 0:
                    player.reset_to_checkpoint()


        for block in level.block_object_list:
            if isinstance(block, CheckpointBlock):
                if player != None:
                    block.check_touching_player(player, CHECKPOINT)
            elif isinstance(block, AirJumpBlock):
                if player != None:
                    block.check_touching_player(player)
                block.particles(GAME.camera.pos, level)
            elif isinstance(block, ExitBlock):
                block.change_color()
                block.particles(GAME.camera.pos, level)
            elif isinstance(block, DangerBlock):
                block.particles(level, GAME.camera.pos)
            elif isinstance(block, WindBlock):
                if player != None:
                    if block.check_touching_player(player):
                        block.push_player(player)
                block.particles(level, GAME.camera.pos)

        for block in level.fog_blocks:
            block.spread(level, 30)


        level_width = level.level_dict["width"] * 20
        level_height = level.level_dict["height"] * 20
        if player != None:
            GAME.move_camera_to_player(player.x+20, player.y+20, [level_width, level_height])
        GAME.camera.screenshake()

        if player != None:
            player.pos_block(GAME.camera.pos)

        for block in level.block_object_list:
            block.pos_block(GAME.camera.pos)
        for block in level.fog_blocks:
            block.pos_block(GAME.camera.pos)
        for block in level.text_blocks:
            block.pos_block(GAME.camera.pos)

        for particle in level.particles:
            particle.update()
            particle.pos_particle(GAME.camera.pos)
            if "wind" in particle.type:
                particle.kill_wind_particle(level)

        level.clear_dead_particles()
        # Draw rectangles
        windowSurface.fill((255,255,255))

        for block in level.block_object_list:
            block.render(windowSurface, GAME.camera.pos)
        for block in level.text_blocks:
            block.render(windowSurface, GAME.camera.pos)
            if player != None:
                if block.check_touching_player(player):
                    block.draw_prompt(GAME.camera.pos, windowSurface)

        if player != None:
            if player.dead == 0:
                player.render(windowSurface, GAME.camera.pos)

        for block in level.fog_blocks:
            block.render(windowSurface, GAME.camera.pos)

        for particle in level.particles:
            particle.render(windowSurface)

        for block in level.text_blocks:
            if block.is_writing:
                block.drawing_text += 1
                block.message.draw_text(block.drawing_text, windowSurface)
            else:
                block.drawing_text = 0

        BLACKOUT.draw(windowSurface)

        # LAST
        pygame.display.update()
        mainClock.tick(60)

    


def main():

    LEVELMANAGER = LevelManager()
    GAME = Game()
    BLACKOUT = Blackout()

    levels = LEVELMANAGER.load_all()
    if levels == []:
        levels.append(LEVELMANAGER.create_empty_level(30,30))
    
    player = None

    CHECKPOINT = pygame.USEREVENT + 1
    DEATH = pygame.USEREVENT + 2
    FINISH = pygame.USEREVENT + 3


    pygame.mixer.init()
    hit = pygame.mixer.Sound("sfx/hit.wav")

    # LOAD IN
    pygame.mixer.music.load("music/Adventure - Disasterpiece.mp3")
    pygame.mixer.music.play(-1)

    pygame_logo = pygame.image.load("img/Pygame_logo.png")
    pygame_logo = pygame.transform.scale(pygame_logo, (500, 140))

    WHITE = (255, 255, 255)

    for x in range(80):
        windowSurface.fill(WHITE)
        pygame.display.update()
        mainClock.tick(60)
    
    for x in range(20):
        windowSurface.fill(WHITE)
        pygame_logo.set_alpha(x/20*255)
        windowSurface.blit(pygame_logo, (50, 230))
        pygame.display.update()
        mainClock.tick(60)
    
    for x in range(60):
        windowSurface.fill(WHITE)
        windowSurface.blit(pygame_logo, (50, 230))
        pygame.display.update()
        mainClock.tick(60)
    
    for x in range(30, 0, -1):
        windowSurface.fill(WHITE)
        pygame_logo.set_alpha(x/30*255)
        windowSurface.blit(pygame_logo, (50, 230))
        pygame.display.update()
        mainClock.tick(60)
    

    for x in range(80):
        windowSurface.fill(WHITE)
        pygame.display.update()
        mainClock.tick(60)



    run_level(levels[0], GAME, BLACKOUT, CHECKPOINT, DEATH, FINISH, hit, "music/Luna Ascension EX - flashygoodness.mp3")
    run_level(levels[1], GAME, BLACKOUT, CHECKPOINT, DEATH, FINISH, hit, "music/Cheat Codes - Nitro Fun.mp3")

    print("Process completed.")

main()
