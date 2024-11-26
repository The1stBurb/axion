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

    def move_camera_to_player(self, x, y, boundaries):
        move_x = (x - self.camera.pos[0] - 300) / 10
        move_y = (y - self.camera.pos[1] - 300) / 10
        self.camera.move_camera([move_x, move_y], boundaries)



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
        self.checkpoints = []

        self.create_block_objects()

    def create_block_objects(self):
        self.block_object_list = []
        self.player_objects = []
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
            elif block == "C":
                block_hitbox = pygame.Rect(0, 0, self.block_size, self.block_size)
                checkpoint = CheckpointBlock(idx%width, idx//width, block_hitbox, self.block_size)
                self.block_object_list.append(checkpoint)
                self.checkpoints.append(checkpoint)
    
    def get_str_of_blocks(self):
        return "".join(self.level_dict["blocklist"])
    
    def get_player_object(self):
        if self.player_objects != []:
            return self.player_objects[0]
        else:
            return None


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

        self.GRAVITY = 0.25
        self.WALKSPEED = 1.5
        self.JUMPHEIGHT = 5.5
        self.TERMINALVELOCITY = 10
        self.COYOTETIME = 6
        self.FRICTION = 0.7

        self.JUMPBUTTONS = [K_w, K_UP, K_SPACE]
        self.LEFTBUTTONS = [K_a, K_LEFT]
        self.RIGHTBUTTONS = [K_d, K_RIGHT]
        
        self.released_jump = True
        self.velocity = [0,0]
        self.airtime = 0
        self.airjumps = 1

        self.checkpoint_x = x
        self.checkpoint_y = y

    def main_loop(self, buttons_pressed, level):
        self.fall()
        self.walk(buttons_pressed)
        self.jump(buttons_pressed)
        self.update_pos(level)

    def fall(self):
        self.velocity[1] += self.GRAVITY
        if self.velocity[1] >= self.TERMINALVELOCITY:
            self.velocity[1] = self.TERMINALVELOCITY
        self.airtime += 1

    def walk(self, buttons_pressed):
        key_walk = 0
        for button in self.LEFTBUTTONS:
            if buttons_pressed[button]:
                key_walk -= 1
                break
        for button in self.RIGHTBUTTONS:
            if buttons_pressed[button]:
                key_walk += 1
                break

        self.velocity[0] += key_walk * self.WALKSPEED
        self.velocity[0] *= self.FRICTION
        

    def jump(self, buttons_pressed):
        for button in self.JUMPBUTTONS:
            if buttons_pressed[button]:
                if self.airtime < self.COYOTETIME:
                    self.velocity[1] = -self.JUMPHEIGHT
                    self.released_jump = False
                elif self.airjumps > 0 and self.released_jump:
                    self.velocity[1] = -self.JUMPHEIGHT
                    self.airjumps -= 1
                    self.released_jump = False
                break
        else:
            self.released_jump = True

    def detect_wall(self, level):
        if self.get_tile_at(self.x, self.y, level) == "B" or self.get_tile_at(self.x, self.y+19, level) == "B" or self.get_tile_at(self.x+19, self.y, level) == "B" or self.get_tile_at(self.x+19, self.y+19, level) == "B":
            if self.velocity[0] > 0:
                self.x -= (self.x % 20)
            else:
                self.x += 20-(self.x % 20)
            self.velocity[0] = 0


    def detect_floor_ceiling(self, level):
        if self.get_tile_at(self.x, self.y, level) == "B" or self.get_tile_at(self.x, self.y+20, level) == "B" or self.get_tile_at(self.x+19, self.y, level) == "B" or self.get_tile_at(self.x+19, self.y+20, level) == "B":
            if self.velocity[1] > 0:
                self.y -= (self.y % 20)
                self.airtime = 0
                self.airjumps = 1
            else:
                self.y += 20-(self.y % 20)
            self.velocity[1] = 0
            

            
    def update_pos(self, level):
        self.x += self.velocity[0]
        self.detect_wall(level)
        self.y += self.velocity[1]
        self.detect_floor_ceiling(level)


    def pos_block(self, camera_pos):
        self.hitbox.left = self.x - camera_pos[0]
        self.hitbox.top = self.y - camera_pos[1]

    def reset_to_checkpoint(self):
        self.x = self.checkpoint_x
        self.y = self.checkpoint_y
        self.airtime = 0
        self.airjumps = 1
        self.velocity = [0, 0]

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

class CheckpointBlock(Block):
    def __init__(self, x, y, hitbox, blocksize):
        super().__init__(x, y, (0, 0, 0), hitbox, blocksize)
        self.claimed = False
        self.color = [0, 100, 0]

    def claim(self, player):
        self.color = [10, 255, 50]
        player.checkpoint_x = self.p_x
        player.checkpoint_y = self.p_y

    def check_touching_player(self, player):
        self.get_pixel_coords()
        if (player.x < self.p_x + 19 and player.x > self.p_x - 19) and (player.y < self.p_y + 19 and player.y > self.p_y - 19):
            if not self.claimed:
                self.claim(player)
    
    def get_pixel_coords(self):
        self.p_x = self.x * 20
        self.p_y = self.y * 20
    

class Camera():
    def __init__(self, move_buttons, speed):
        self.pos = [0, 0]
        self.move_buttons = move_buttons
        self.speed = speed


    def move_camera(self, movement, boundaries):
        self.pos[0] += movement[0]
        self.pos[1] += movement[1]
        if self.pos[0] < 0:
            self.pos[0] = 0
        if self.pos[1] < 0:
            self.pos[1] = 0
        if self.pos[0] > boundaries[0] - 600:
            self.pos[0] = boundaries[0] - 600
        if self.pos[1] > boundaries[1] - 600:
            self.pos[1] = boundaries[1] - 600