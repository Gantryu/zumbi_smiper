import pygame
from pygame.locals import *
from sys import exit
from helper.qrcode_helper import *
from helper.pygame_helper import *
from model.game_object import *
from PIL import Image


GAME_NAME = 'Zombie Smiper'


class GameScene(object):

    def __init__(self, bg_img, bg_audio, pygame, frames = 30):
        self.bg_img = bg_img
        self.bg_audio = bg_audio
        self.background = None
        self.pygame = pygame
        self.screen = None
        self.scene_objects = []
        self.guns = []
        self.zombies = []
        self.frames = 30
        self.running = False

    def load_bg_sound(self, bg_audio=None):
        if bg_audio: self.bg_audio = bg_audio
        bg_sound = load_sound(self.bg_audio)
        bg_sound.play(-1)

    def load_bg_img(self, bg_img=None):
        if bg_img: self.bg_img = bg_img


    def get_screen(self):
        return self.screen

    def get_pygame(self):
        return self.pygame

    def get_background(self):
        return self.background

    def get_zombies(self):
        return self.zombies

    def get_guns(self):
        return self.guns


    def add_scene_object(self, game_object):
        if isinstance(game_object, GameObject):
            self.scene_objects.append(game_object) # todo verificar se é um GameObject
            if isinstance(game_object, Gun):
                self.guns.append(game_object)
            elif isinstance(game_object, Zombie):
                self.zombies.append(game_object)


    def update_objects(self, pressed_mouse = [], passed_time = 0, **others):
        # TODO pode precisar de otimizacao essa parte da profundidade a imagem no eixo Y
        sobjects = sorted(self.scene_objects, key=GameObject.getKey)
        for go in sobjects:
            if (isinstance(go, Gun)):
                go.shoot=None
            go.action(pressed_mouse=pressed_mouse, passed_time=passed_time, **others)
        for go in sobjects:
            go.render()



    def pause_play(self):
        self.running = not self.running


    def start(self):
        info_screen = pygame.display.Info()
        w, h = info_screen.current_w, info_screen.current_h
        self.screen = pygame.display.set_mode((w, h), FULLSCREEN | DOUBLEBUF, 32)
        pygame.display.set_caption(GAME_NAME)
        self.background = load_img(self.bg_img)
        self.background = pygame.transform.scale(self.background, (w, h))
        clock = pygame.time.Clock()

        self.running = False
        while True:
            pressed_mouse = pygame.mouse.get_pressed()

            passed_time = clock.tick(self.frames)
            self.screen.blit(self.background, (0, 0))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        exit()
                    elif event.key == K_p: # Pause e Play
                        self.pause_play()
                    elif event.key == K_s: # Shoot
                        # TODO adicionar aqui o evento do controle
                        evt = pygame.event.Event(MOUSEBUTTONDOWN, button = 2)
                        pressed_mouse = (evt, evt, evt)
            if self.running :
                self.update_objects(pressed_mouse, passed_time) # Renderiza todos os objetos
            else:
                self.update_objects(pressed_mouse, 0) # Renderiza todos os objetos
            pygame.display.flip()


def main():
 pass


if __name__ == '__main__':
    main()
