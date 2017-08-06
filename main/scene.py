import pygame
from pygame.locals import *
from sys import exit
from helper.qrcode_helper import *
from helper.pygame_helper import *
from model.game_object import *
from PIL import Image

GAME_NAME = 'Zombie Smiper'


class GameScene(object):
    def __init__(self, bg_img, bg_audio, pygame, frames=70):
        self.bg_img = bg_img
        self.bg_audio = bg_audio
        self.background = None
        self.pygame = pygame
        self.screen = None
        self.scene_objects = []
        self.guns = []
        self.zombies = []
        self.players = []
        self.frames = frames
        self.running = False

        self.info_panel = PanelInfo(self)
        self.w = 0
        self.h = 0

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
            self.scene_objects.append(game_object)
            if isinstance(game_object, Gun):
                self.guns.append(game_object)
            elif isinstance(game_object, Zombie):
                self.zombies.append(game_object)

    def update_objects(self, pressed_mouse=[], passed_time=0, **others):
        sobjects = sorted(self.scene_objects, key=GameObject.getKey)  # ordena objetos para profundidade eixo Y
        for go in sobjects:
            if isinstance(go, Gun):
                go.shoot = None
                go.render(others['aim']) # TODO aqui suporte renderizar +1 mira
            go.action(pressed_mouse=pressed_mouse, passed_time=passed_time, **others)
            go.render()

    def pause_play(self):
        self.running = not self.running

    def start(self):
        info_screen = pygame.display.Info()
        self.w, self.h = info_screen.current_w, info_screen.current_h
        self.screen = pygame.display.set_mode((self.w, self.h), FULLSCREEN | DOUBLEBUF, 32)
        pygame.display.set_caption(GAME_NAME)
        self.background = load_img(self.bg_img)
        self.background = pygame.transform.scale(self.background, (self.w, self.h))
        clock = pygame.time.Clock()

        self.info_panel.pos = (10, 10)
        self.add_scene_object(self.info_panel)
        self.aim = [int(self.w / 2), int(self.h / 2)]

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
                    if event.key == K_p:  # Pause e Play
                        self.pause_play()

                    if event.key == K_s:  # Shoot
                        # TODO adicionar aqui o evento do controle
                        evt = pygame.event.Event(MOUSEBUTTONDOWN, button=2)
                        pressed_mouse = (evt, evt, evt)

                    if event.key == K_UP:
                        self.aim[1] -= passed_time
                    elif event.key == K_DOWN:
                        self.aim[1] += passed_time
                    elif event.key == K_LEFT:
                        self.aim[0] -= passed_time
                    elif event.key == K_RIGHT:
                        self.aim[0] += passed_time


            # motor principal
            if self.running:
                self.update_objects(pressed_mouse, passed_time, aim=self.aim)  # Renderiza todos os objetos
                for z in self.zombies:
                    self.info_panel.point += z.get_reward()
                    if z.finished:
                        self.zombies.remove(z)
                        self.scene_objects.remove(z)
                    if z.scape:
                       self.info_panel.point -= 30
            else:
                self.update_objects(pressed_mouse, 0, aim=self.aim)  # Renderiza todos os objetos com tempo 0


            pygame.display.flip()


def main():
    pass


if __name__ == '__main__':
    main()
