import pygame
from main.scene import *
from main.img_const import *
from main.factory import *
import random

BG_02 = '../_img/bg_02.png'
BG_01 = '../_img/bg_01.jpg'
BG_SOUND = '../_audio/bg_audio01.ogg'


pygame.init()
pygame.mixer.init()
pygame.mixer.init()
pygame.mouse.set_visible(False)
gs = GameScene(BG_02, BG_SOUND, pygame)
# zombie_sprite = load_img(ZOMBIES_SPRITES)
# zombies_green = zombie_sprite.subsurface((4, 68), (56, 65))


gs.load_bg_img()
gs.load_bg_sound()
gun = Gun(gs, load_img('../_img/aim1.png'), load_img('../_img/aim2.png'), load_sound('../_audio/m19.ogg'),
          no_ammo_sound=load_sound('../_audio/empty_gun.ogg'), speed=100)

gun.set_shoot_volume(0.5)
gun.set_damage(10)
gun.set_max_ammo(1000)
gun.recharge_ammo(1000)

z = ZombieFactory((158, 158))
zumbi_walk = z.g_zombie_walk()
zumbi_die = z.g_zombie_die()
zumbi_headshot = z.g_zombie_headshot()

zumbi = Zombie(gs, load_sound('../_audio/sound_zombie01.ogg'), load_img(path_img('0001.png'), (158, 158)),
               pos=(2000, 550))
zumbi.set_resistance(0, 3, 8)
zumbi.add_sprite_sequence('walk', zumbi_walk)
zumbi.add_sprite_sequence('die', zumbi_die)
zumbi.add_sprite_sequence('headshot', zumbi_headshot)
zumbi.def_current_sprite_sequence('walk')

zumbi1 = Zombie(gs, load_sound('../_audio/sound_zombie01.ogg'), load_img(path_img('0001.png'), (158, 158)),
                pos=(2000, 600), speed=150)
zumbi1.set_resistance(0, 5, 8)
zumbi1.add_sprite_sequence('walk', zumbi_walk)
zumbi1.add_sprite_sequence('die', zumbi_die)
zumbi1.add_sprite_sequence('headshot', zumbi_headshot)
zumbi1.def_current_sprite_sequence('walk')

zumbi2 = Zombie(gs, load_sound('../_audio/sound_zombie01.ogg'), load_img(path_img('0001.png'), (158, 158)),
                pos=(2000, 530))
zumbi2.set_resistance(0, 0, 0)
zumbi2.add_sprite_sequence('walk', zumbi_walk)
zumbi2.add_sprite_sequence('die', zumbi_die)
zumbi2.add_sprite_sequence('headshot', zumbi_headshot)
zumbi2.def_current_sprite_sequence('walk')


def testProfundidade():

    gs.add_scene_object(gun)
    gs.add_scene_object(zumbi)
    gs.add_scene_object(zumbi2)


def testDanoSprite():

    gs.add_scene_object(gun)
    gs.add_scene_object(zumbi)
    gs.add_scene_object(zumbi1)
    gs.add_scene_object(zumbi2)

def testMudancaSprite():
    from copy import copy
    gs.add_scene_object(gun)
    for i in range(20):
        zumbi1.posX = zumbi1.posX + i * 30
        zumbi.posX = zumbi1.posX + i * 20
        zumbi2.posX = zumbi1.posX + i * 10
        zumbi1.posY = random.randrange(480,640 )
        zumbi.posY = random.randrange(480, 640)
        zumbi2.posY = random.randrange(480, 640)

        gs.add_scene_object(copy(zumbi1))
        gs.add_scene_object(copy(zumbi))
        gs.add_scene_object(copy(zumbi2))


#testProfundidade()
#testDanoSprite()
testMudancaSprite()
gs.start()