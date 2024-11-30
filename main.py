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

def main():
    editing = True

    LEVELMANAGER = LevelManager()
    GAME = Game()

    levels = LEVELMANAGER.load_all()
    if levels == []:
        levels.append(LEVELMANAGER.create_empty_level(30,30))
    

    LEVELEDITOR = LevelEditor()
    blocksize = 20

    cursor_box = pygame.Rect(0, 0, 20, 20)
    
    player = None

    CHECKPOINT = pygame.USEREVENT + 1
    DEATH = pygame.USEREVENT + 2
    FINISH = pygame.USEREVENT + 3

    drawing_text = 0


    while True:
        # FIRST
        if editing:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == K_t:
                        LEVELMANAGER.save_all(levels)
                    elif event.key == K_g:
                        levels.append(LEVELMANAGER.add_level(len(levels)))
                        LEVELEDITOR.level_idx = len(levels)-1
                    elif event.key == K_r:
                        levels[LEVELEDITOR.level_idx] = LEVELMANAGER.add_level(LEVELEDITOR.level_idx)
                    elif event.key == K_j:
                        LEVELEDITOR.level_idx -= 1
                        if LEVELEDITOR.level_idx < 0:
                            LEVELEDITOR.level_idx = len(levels)-1
                    elif event.key == K_k:
                        LEVELEDITOR.level_idx += 1
                        if LEVELEDITOR.level_idx >= len(levels):
                            LEVELEDITOR.level_idx = 0
                    # change brush
                    elif event.key == K_b:
                        LEVELEDITOR.change_brush("B")
                    elif event.key == K_e:
                        LEVELEDITOR.change_brush(" ")
                    elif event.key == K_p:
                        LEVELEDITOR.change_brush("P")
                    elif event.key == K_c:
                        LEVELEDITOR.change_brush("C")
                    elif event.key == K_v:
                        LEVELEDITOR.change_brush("J")
                    elif event.key == K_x:
                        LEVELEDITOR.change_brush("X")
                    elif event.key == K_z:
                        LEVELEDITOR.change_brush("Z")
                    elif event.key == K_f:
                        LEVELEDITOR.change_brush("F")
                    elif event.key == K_n:
                        LEVELEDITOR.change_brush("N")


                    elif event.key == K_q:
                        editing = False
            


            if player == None:
                player = levels[LEVELEDITOR.level_idx].get_player_object()

            # Get keys pressed and mouse position
            keys = pygame.key.get_pressed()
            raw_mouse_pos = pygame.mouse.get_pos()
            
            # Get camera movements

            level_width = levels[LEVELEDITOR.level_idx].level_dict["width"] * 20
            level_height = levels[LEVELEDITOR.level_idx].level_dict["height"] * 20
            if keys[LEVELEDITOR.camera.move_buttons["up"]]:
                LEVELEDITOR.camera.move_camera([0, -LEVELEDITOR.camera.speed], [level_width, level_height])
            if keys[LEVELEDITOR.camera.move_buttons["down"]]:
                LEVELEDITOR.camera.move_camera([0, LEVELEDITOR.camera.speed], [level_width, level_height])
            if keys[LEVELEDITOR.camera.move_buttons["left"]]:
                LEVELEDITOR.camera.move_camera([-LEVELEDITOR.camera.speed, 0], [level_width, level_height])
            if keys[LEVELEDITOR.camera.move_buttons["right"]]:
                LEVELEDITOR.camera.move_camera([LEVELEDITOR.camera.speed, 0], [level_width, level_height])

            mouse_pos = [raw_mouse_pos[0]+LEVELEDITOR.camera.pos[0], raw_mouse_pos[1]+LEVELEDITOR.camera.pos[1]]

            LEVELEDITOR.tile_num = mouse_pos[0] // blocksize + (mouse_pos[1] // blocksize) * levels[LEVELEDITOR.level_idx].level_dict["width"]

            cursor_box.left = LEVELEDITOR.tile_num % levels[LEVELEDITOR.level_idx].level_dict["width"] * blocksize
            cursor_box.top = LEVELEDITOR.tile_num // levels[LEVELEDITOR.level_idx].level_dict["width"] * blocksize
            cursor_box.left -= LEVELEDITOR.camera.pos[0]
            cursor_box.top -= LEVELEDITOR.camera.pos[1]

            if pygame.mouse.get_pressed()[0]:
                if levels[LEVELEDITOR.level_idx].level_dict["blocklist"][LEVELEDITOR.tile_num] != LEVELEDITOR.brush:
                    if LEVELEDITOR.brush != "N" and levels[LEVELEDITOR.level_idx].level_dict["blocklist"][LEVELEDITOR.tile_num] == "N":
                        LEVELEDITOR.add_block(levels[LEVELEDITOR.level_idx])
                        levels[LEVELEDITOR.level_idx].messages.pop(LEVELEDITOR.tile_num)
                    else:
                        LEVELEDITOR.add_block(levels[LEVELEDITOR.level_idx])
                        player = levels[LEVELEDITOR.level_idx].get_player_object()
                    
            try:
                player.pos_block(LEVELEDITOR.camera.pos)
            except:
                pass

            # Set positions of rectangles
            for block in levels[LEVELEDITOR.level_idx].block_object_list:
                block.pos_block(LEVELEDITOR.camera.pos)
            for block in levels[GAME.level_idx].fog_blocks:
                block.pos_block(LEVELEDITOR.camera.pos)
            for block in levels[GAME.level_idx].text_blocks:
                block.pos_block(LEVELEDITOR.camera.pos)

            # Draw rectangles
            windowSurface.fill((255,255,255))

            for block in levels[LEVELEDITOR.level_idx].block_object_list:
                block.render(windowSurface)
            for block in levels[LEVELEDITOR.level_idx].fog_blocks:
                block.render(windowSurface)
            for block in levels[LEVELEDITOR.level_idx].text_blocks:
                block.render(windowSurface) 

            try:
                player.render(windowSurface)
            except:
                pass

            # Cursor
            if LEVELEDITOR.brush == "B":
                cursor_color = (0,0,0)
            elif LEVELEDITOR.brush == " ":
                cursor_color = (255,255,255)
            elif LEVELEDITOR.brush == "P":
                cursor_color = (80,80,255)
            elif LEVELEDITOR.brush == "C":
                cursor_color = (0,100,0)
            elif LEVELEDITOR.brush == "J":
                cursor_color = (255,175,0)
            elif LEVELEDITOR.brush == "X":
                cursor_color = (255,20,71)
            elif LEVELEDITOR.brush == "Z":
                cursor_color = (255,200,100)
            elif LEVELEDITOR.brush == "F":
                cursor_color = (50,0,22)
            elif LEVELEDITOR.brush == "N":
                cursor_color = (200, 200, 150)

            pygame.draw.rect(windowSurface, cursor_color, cursor_box)


            # LAST
            pygame.display.update()
            mainClock.tick(60)




        else: # Not in editing mode?




            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == K_q:
                        editing = True
                    if event.key == K_r:
                        player.reset_to_checkpoint()

                elif event.type == CHECKPOINT:
                    for block in levels[GAME.level_idx].block_object_list:
                        if isinstance(block, CheckpointBlock):
                            block.declaim()

                elif event.type == DEATH:
                    levels[GAME.level_idx].death_particles(player)

                elif event.type == FINISH:
                    GAME.level_idx += 1
                    player = None
                    continue


            if player == None:
                player = levels[GAME.level_idx].get_player_object()
            
            keys = pygame.key.get_pressed()

            if player.dead == 0:
                player.main_loop(keys, levels[GAME.level_idx], DEATH, FINISH)
            else:
                player.dead -= 1
                if player.dead == 0:
                    player.reset_to_checkpoint()


            for block in levels[GAME.level_idx].block_object_list:
                if isinstance(block, CheckpointBlock):
                    block.check_touching_player(player, CHECKPOINT)
                elif isinstance(block, AirJumpBlock):
                    block.check_touching_player(player)
                elif isinstance(block, ExitBlock):
                    block.change_color()
                elif isinstance(block, DangerBlock):
                    block.particles(levels[GAME.level_idx])

            for block in levels[GAME.level_idx].text_blocks:
                if block.check_touching_player(player):
                    block.drawing_text += 1
                    block.message.draw_text(block.drawing_text)
                else:
                    block.drawing_text = 0
                
            for block in levels[GAME.level_idx].fog_blocks:
                block.spread(levels[GAME.level_idx], 30)


            level_width = levels[GAME.level_idx].level_dict["width"] * 20
            level_height = levels[GAME.level_idx].level_dict["height"] * 20
            GAME.move_camera_to_player(player.x+20, player.y+20, [level_width, level_height])

            player.pos_block(GAME.camera.pos)

            for block in levels[GAME.level_idx].block_object_list:
                block.pos_block(GAME.camera.pos)
            for block in levels[GAME.level_idx].fog_blocks:
                block.pos_block(GAME.camera.pos)
            for block in levels[GAME.level_idx].text_blocks:
                block.pos_block(GAME.camera.pos)

            for particle in levels[GAME.level_idx].particles:
                particle.update()
                particle.pos_particle(GAME.camera.pos)
                levels[GAME.level_idx].clear_dead_particles()

            # Draw rectangles
            windowSurface.fill((255,255,255))

            for block in levels[GAME.level_idx].block_object_list:
                block.render(windowSurface)
            for block in levels[GAME.level_idx].text_blocks:
                block.render(windowSurface)
            if player.dead == 0:
                player.render(windowSurface)

            for block in levels[GAME.level_idx].fog_blocks:
                block.render(windowSurface)


            for particle in levels[GAME.level_idx].particles:
                particle.render(windowSurface)


            # LAST
            pygame.display.update()
            mainClock.tick(60)
        

main()
