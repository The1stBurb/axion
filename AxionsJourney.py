import pygame
from pygame.locals import *
import os, sys

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


class Game:
    def __init__(self):
        self.camera = Camera(None, 1)
        self.level_idx = 0



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
        self.player_objects = []

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
                new_player = PlayerBlock(self.block_size*(idx%width), self.block_size*(idx//width), block_hitbox, self.block_size)
                self.player_objects.append(new_player)
    
    def get_str_of_blocks(self):
        return "".join(self.level_dict["blocklist"])
    
    def get_player_objects(self):
        return self.player_objects


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

    def render(self, windowSurface):
        pygame.draw.rect(windowSurface, self.color, self.hitbox)



class PlayerBlock(Block):
    def __init__(self, x, y, hitbox, blocksize):
        super().__init__(x, y, (80,80,255), hitbox, blocksize)

        self.GRAVITY = 0.02
        self.WALKSPEED = 3
        self.JUMPHEIGHT = 0.33
        self.TERMINALVELOCITY = 5

        self.JUMPBUTTONS = [pygame.K_w, pygame.K_UP, pygame.K_SPACE]
        
        self.velocity = [0,0]

    def main_loop(self, buttons_pressed, level):
        self.walk(buttons_pressed)
        self.fall()
        self.jump(buttons_pressed)
        self.update_pos(level)

    def fall(self):
        self.velocity[1] += self.GRAVITY
        if self.velocity[1] >= self.TERMINALVELOCITY:
            self.velocity[1] = self.TERMINALVELOCITY

    def walk(self, buttons_pressed):
        pass

    def jump(self, buttons_pressed):
        for button in self.JUMPBUTTONS:
            if buttons_pressed[button]:
                self.velocity[1] = -self.JUMPHEIGHT

    def detect_wall(self):
        pass

    def detect_floor_ceiling(self, level):
        print(self.x, self.y)
        print(self.get_tile_at(self.x, self.y, level))

            

    def update_pos(self, level):
        self.x += self.velocity[0]
        self.detect_wall()
        self.y += self.velocity[1]
        self.detect_floor_ceiling(level)


    def pos_block(self, camera_pos):
        self.hitbox.left = self.x - camera_pos[0]
        self.hitbox.top = self.y - camera_pos[1]


    @staticmethod
    def get_tile_at(x, y, level):
        tile_x = int(x/20)
        tile_y = int(y/20)
        tile_idx = tile_x + tile_y*level.level_dict["width"]
        return level.level_dict["blocklist"][tile_idx]


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