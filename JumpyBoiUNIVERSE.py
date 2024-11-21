import pygame
from pygame.locals import *
import os, sys

mainClock = pygame.time.Clock()
pygame.init()

WINDOWWIDTH = 600
WINDOWHEIGHT = 600
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption("Jumpy Boi UNIVERSE")

# Make a UML diagram of all the classes
# Classes like:
'''
Block, which has children like PlayerBlock and LavaBlock
Camera, associated with PlayerBlock 
LevelEditor, which is associated with camera
Level, which has blocks in it
Particle
SoundManager
'''
class LevelManager:
    def __init__(self):
        self.camera = Camera(None, None)

    def create_empty_level(self, id, dimensions):
        level_list = []
        level_list += ["B"] * dimensions[0] # top of box
        level_list += ((["B"] + [" "] * (dimensions[0]-2) + ["B"]) * (dimensions[1]-2)) # walls and middle of box
        level_list += ["B"] * dimensions[0] # bottom of box
        



        return Level(id, {
            "width": dimensions[0],
            "height": dimensions[1],
            "blocklist": level_list
        }, 20)
    
    def save_all(self, list_of_levels):
        print("Saving...")
        i=0
        for level in list_of_levels:
            l_dict = level.level_dict
            l_width = l_dict["width"]
            l_height = l_dict["height"]
            l_list = "".join(l_dict["blocklist"])
            
            level_file = open("levels/level-"+str(i)+".jbu", "w")
            level_file.write(str(l_width) + "," + str(l_height) + "," + l_list)
            level_file.close()
            i += 1
        print("Levels saved!")

    def load_all(self):

        levels = []

        level_dir = "levels"
        id=0
        for file in os.listdir(level_dir):
            lvl_file = open("levels/"+file, "r")
            lvl_txt = lvl_file.read()
            width = ""
            for char in lvl_txt:
                if char == ",":
                    break
                width += char
            lvl_txt = lvl_txt[len(width)+1:]
                
            width = int(width)
            height = ""
            for char in lvl_txt:
                if char == ",":
                    break
                height += char
            lvl_txt = lvl_txt[len(height)+1:]
            height = int(height)
            lvl_list = list(lvl_txt)

            levels.append(Level(
                id,
                {
                    "width": width,
                    "height": height,
                    "blocklist": lvl_list
                },
                20
                ))
            
            id+=1


        return levels

    def add_level(self, level_idx):

        while True:
            try:
                width = int(input("What should the width of the new level be?: ").strip())
                break
            except ValueError:
                print("That's not a valid integer.")
        
        while True:
            try:
                height = int(input("What should the height of the new level be?: ").strip())
                break
            except ValueError:
                print("That's not a valid integer.")
        
        return self.create_empty_level(level_idx, [width, height])




class Level:
    def __init__(self, id, level_dict, block_size):
        self.id = id
        self.level_dict = level_dict
        self.block_object_list = []
        self.block_size = block_size

        self.create_block_objects()

    def create_block_objects(self):
        self.block_object_list = []
        width = self.level_dict["width"]
        for idx, block in enumerate(self.level_dict["blocklist"]):
            if block == "B":
                block_hitbox = pygame.Rect(0, 0, self.block_size, self.block_size)
                self.block_object_list.append(RegBlock(idx%width, idx//width, block_hitbox, self.block_size))
            elif block == "N":
                block_hitbox = pygame.Rect(0, 0, self.block_size, self.block_size)
                self.block_object_list.append(BounceBlock(idx%width, idx//width, block_hitbox, self.block_size))
            elif block == "P":
                block_hitbox = pygame.Rect(0, 0, self.block_size, self.block_size)
                self.block_object_list.append(PlayerBlock(idx%width, idx//width, block_hitbox, self.block_size))
    
    def get_str_of_blocks(self):
        return "".join(self.level_dict["blocklist"])


class LevelEditor:
    def __init__(self):
        self.camera = Camera({"up": K_w, "down": K_s, "left": K_a, "right": K_d}, 5)
        self.tile_num = 0
        self.level_idx = 0
        self.brush = "B"

    def add_block(self, level):
        level.level_dict["blocklist"][self.tile_num] = self.brush
        level.create_block_objects()
    
    def change_brush(self, new_brush):
        self.brush = new_brush


class Block:
    def __init__(self, x, y, color, hitbox, blocksize):
        self.x = x
        self.y = y
        self.color = color
        self.hitbox = hitbox
        self.blocksize = blocksize

    def pos_block(self, camera_pos):
        self.hitbox.left = self.x*self.blocksize - camera_pos[0]
        self.hitbox.top = self.y*self.blocksize - camera_pos[1]

    def render(self):
        pygame.draw.rect(windowSurface, self.color, self.hitbox)



class PlayerBlock(Block):
    def __init__(self, x, y, hitbox, blocksize):
        super().__init__(x, y, (80,80,255), hitbox, blocksize)

        self.GRAVITY = -0.1
        self.WALKSPEED = 3
        self.JUMPHEIGHT = 5
        self.TERMINALVELOCITY = 5
        
        self.velocity = [0,0]

    def main_loop(self, buttons_pressed):
        self.walk(buttons_pressed)
        self.fall()
        self.jump(buttons_pressed)

    def fall(self):
        self.velocity[1] += self.GRAVITY
        if self.velocity[1] >= self.TERMINALVELOCITY:
            self.velocity[1] = self.TERMINALVELOCITY

    def walk(self, buttons_pressed):
        pass

    def jump(self, buttons_pressed):
        pass

    def detect_wall(self):
        pass

    def detect_floor_ceiling(self):
        pass

    def update_pos(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]


class RegBlock(Block):
    def __init__(self, x, y, hitbox, blocksize):
        super().__init__(x, y, (0,0,0), hitbox, blocksize)

class LaserBlock(Block):
    pass

class BounceBlock(Block):
    def __init__(self, x, y, hitbox, blocksize):
        super().__init__(x, y, (0,255,0), hitbox, blocksize)

class WaterBlock(Block):
    pass

class ExitBlock(Block):
    pass

class Camera():
    def __init__(self, move_buttons, speed):
        self.pos = [0, 0]
        self.move_buttons = move_buttons
        self.speed = speed


    def move_camera(self, movement):
        self.pos[0] += movement[0]
        self.pos[1] += movement[1]

def main():
    editing = True

    LEVELMANAGER = LevelManager()

    levels = LEVELMANAGER.load_all()
    if levels == []:
        levels.append(LEVELMANAGER.create_empty_level(30,30))
    

    LEVELEDITOR = LevelEditor()
    blocksize = 20

    cursor_box = pygame.Rect(0, 0, 20, 20)

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
            
            # then other stuff

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
                    


            # Set positions of rectangles
            for block in levels[LEVELEDITOR.level_idx].block_object_list:
                block.pos_block(LEVELEDITOR.camera.pos)

            # Draw rectangles
            windowSurface.fill((255,255,255))

            for block in levels[LEVELEDITOR.level_idx].block_object_list:
                block.render()

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
            players = LEVELMANAGER.get_players()
            

            for player in players:
                pass


            for block in levels[LEVELEDITOR.level_idx].block_object_list:
                block.pos_block(LEVELEDITOR.camera.pos)

            # Draw rectangles
            windowSurface.fill((255,255,255))

            for block in levels[LEVELEDITOR.level_idx].block_object_list:
                block.render()


            # LAST
            pygame.display.update()
            mainClock.tick(60)
        

main()
