import pygame
from pygame.locals import *
import os, sys
from AxionsJourney import *

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
    
    players = []

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
                    elif event.key == K_n:
                        LEVELEDITOR.change_brush("N")
                    elif event.key == K_e:
                        LEVELEDITOR.change_brush(" ")
                    elif event.key == K_p:
                        LEVELEDITOR.change_brush("P")

                    elif event.key == K_q:
                        editing = False
            


            if players == []:
                players = levels[LEVELEDITOR.level_idx].get_player_objects()

            # Get keys pressed and mouse position
            keys = pygame.key.get_pressed()
            raw_mouse_pos = pygame.mouse.get_pos()
            
            # Get camera movements
            if keys[LEVELEDITOR.camera.move_buttons["up"]]:
                LEVELEDITOR.camera.move_camera([0, -LEVELEDITOR.camera.speed])
            if keys[LEVELEDITOR.camera.move_buttons["down"]]:
                LEVELEDITOR.camera.move_camera([0, LEVELEDITOR.camera.speed])
            if keys[LEVELEDITOR.camera.move_buttons["left"]]:
                LEVELEDITOR.camera.move_camera([-LEVELEDITOR.camera.speed, 0])
            if keys[LEVELEDITOR.camera.move_buttons["right"]]:
                LEVELEDITOR.camera.move_camera([LEVELEDITOR.camera.speed, 0])

            mouse_pos = [raw_mouse_pos[0]+LEVELEDITOR.camera.pos[0], raw_mouse_pos[1]+LEVELEDITOR.camera.pos[1]]

            LEVELEDITOR.tile_num = mouse_pos[0] // blocksize + (mouse_pos[1] // blocksize) * levels[LEVELEDITOR.level_idx].level_dict["width"]

            cursor_box.left = LEVELEDITOR.tile_num % levels[LEVELEDITOR.level_idx].level_dict["width"] * blocksize
            cursor_box.top = LEVELEDITOR.tile_num // levels[LEVELEDITOR.level_idx].level_dict["width"] * blocksize
            cursor_box.left -= LEVELEDITOR.camera.pos[0]
            cursor_box.top -= LEVELEDITOR.camera.pos[1]

            if pygame.mouse.get_pressed()[0]:
                if levels[LEVELEDITOR.level_idx].level_dict["blocklist"][LEVELEDITOR.tile_num] != LEVELEDITOR.brush:
                    LEVELEDITOR.add_block(levels[LEVELEDITOR.level_idx])
                    players = levels[LEVELEDITOR.level_idx].get_player_objects()
                    

            for player in players:
                player.pos_block(LEVELEDITOR.camera.pos)

            # Set positions of rectangles
            for block in levels[LEVELEDITOR.level_idx].block_object_list:
                block.pos_block(LEVELEDITOR.camera.pos)

            # Draw rectangles
            windowSurface.fill((255,255,255))

            for block in levels[LEVELEDITOR.level_idx].block_object_list:
                block.render(windowSurface)

            for player in players:
                player.render(windowSurface)

            if LEVELEDITOR.brush == "B":
                cursor_color = (0,0,0)
            elif LEVELEDITOR.brush == "N":
                cursor_color = (0,255,0)
            elif LEVELEDITOR.brush == " ":
                cursor_color = (255,255,255)
            elif LEVELEDITOR.brush == "P":
                cursor_color = (80,80,255)
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

            if players == []:
                players = levels[GAME.level_idx].get_player_objects()
            
            keys = pygame.key.get_pressed()

            for player in players:
                player.main_loop(keys, levels[GAME.level_idx])

            for player in players:
                player.pos_block(GAME.camera.pos)

            for block in levels[GAME.level_idx].block_object_list:
                block.pos_block(GAME.camera.pos)

            # Draw rectangles
            windowSurface.fill((255,255,255))

            for block in levels[LEVELEDITOR.level_idx].block_object_list:
                block.render(windowSurface)

            for player in players:
                player.render(windowSurface)


            # LAST
            pygame.display.update()
            mainClock.tick(60)
        

main()
