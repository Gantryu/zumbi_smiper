from helper.pygame_helper import *
from main.img_const import *


class ZombieFactory():
    def __init__(self, dimension = None):
        self.dimension = dimension


    def g_zombie_walk(self):
        walk = []
        for i in range(5,13):
            if i < 10: i_file = '000' + str(i)
            else: i_file = '00' + str(i)
            walk.append(load_img(path_img(i_file+'.png'), self.dimension))
        return walk

    def g_zombie_die(self):
        die = []
        for i in range(23,29):
            i_file = '00' + str(i)
            die.append(load_img(path_img(i_file+'.png'), self.dimension))
        return die

    def g_zombie_headshot(self):
        headshot = []
        for i in range (29,37):
            i_file = '00' + str(i)
            headshot.append(load_img(path_img(i_file+'.png'), self.dimension))
        return headshot