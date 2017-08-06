import pygame
import random
from helper.game_object_helper import *




class GameObject(object):
    """ Representa um objeto 2D no jogo"""

    def __init__(self, game_scene, depth=0, pos=(0,0)):
        self.game_scene = game_scene
        self.depth = depth
        self.posX, self.posY = pos


    def render(self, pos=None):
        """
        Metodo abstrato, renderiza um GameObject na tela
        :param pos: uma tupla (x,y), sendo as posicoes onde o objeto sera renderizado
        :return: None
        """
        pass

    def action(self, pressed_mouse=[], pressed_key=[], passed_time=0, **others):
        """
        Metodo abstrato, acoes a serem executadas ao chamar o metodo em um GameObject
        :param mouse: eventos, sendo os eventos do mouse
        :param key: eventos, sendo os eventos do teclado
        :param others: outros parametros
        :return:
        """
        pass

    def getKey(self):
        return self.depth


class PanelInfo(GameObject):

    def __init__(self, game_scene, depth=0, pos=(0,0)):
        super(PanelInfo,self).__init__(game_scene, depth, pos)
        self.font_color = (25, 255, 25)
        self.font = pygame.font.Font(None, 40)
        self.point = 0

    def render(self, pos=None):
        message = self.font.render("$: " + str(self.point) , 1, self.font_color)
        self.game_scene.screen.blit(message, self.pos)

    def action(self, pressed_mouse=[], pressed_key=[], passed_time=0, **others):
        pass


class Gun(GameObject):
    def __init__(self, game_scene, gun_img, aim_img, gun_sound=None, gun_reload_sound=None, no_ammo_sound=None,
                 speed=0, ammo=0, max_ammo=10, damage=5):
        super(Gun, self).__init__(game_scene)
        self.gun_img = gun_img
        self.aim_img = aim_img
        self.gun_sound = gun_sound
        self.no_ammo_sound = no_ammo_sound
        self.gun_reload_sound = gun_reload_sound
        self.aim_pos = (200, 200)
        self.speed = speed
        self.ammo = ammo
        self.max_ammo = max_ammo
        self.reload = 0
        self.shot_volume = 0.2
        self.set_shoot_volume(self.shot_volume)
        self.shoot = None
        self.depth = 99999  # Um valor alto de profundidade pra ficar sempre a frente
        self.damage = damage

    def def_aim_pos(self, pos):
        """
        Define a posicao atual da mira
        :param pos: uma tupla (x, y), sendo os valores de x e y onde será renderizada a mira
        esses valores serao alterados de acordo com o tamanho da mira para centralizar
        :return: None
        """
        if pos:
            self.aim_pos = (pos[0] - (self.aim_img.get_width() / 2), pos[1] - (self.aim_img.get_height() / 2))

    def get_aim_pos(self):
        """
        :return: Uma tupla, sendo a posição da mira centralizada
        """
        return self.aim_pos[0] + self.aim_img.get_width() / 2, self.aim_pos[1] + self.aim_img.get_height() / 2

    def set_damage(self, damage):
        """
        :param damage: Um inteiro, sendo o valor de dano da arma entre 0 e 10
        :return: None
        """
        if damage >= 10:
            self.damage = 10
        elif damage <= 0:
            self.damage = 0
        else:
            self.damage = damage

    def get_damage(self):
        return self.damage

    def set_max_ammo(self, max_ammo):
        self.max_ammo = max_ammo

    def get_max_ammo(self):
        return self.max_ammo

    def shooter(self):
        """
        Atira e zera o tempo para recarregar
        :return: None
        """
        if self.ammo > 0:
            self.shoot = self.get_aim_pos()
            self.gun_sound.play()
            self.ammo -= 1
        else:
            self.no_ammo_sound.play()
        self.reload = 0

    def recover_shoot(self):
        return self.shoot

    def recharge_ammo(self, quantity):
        """
        Recarrega a arma
        :param quant: um inteiro, sendo a quantidade de balas a serem adicionadas
        :return: um inteiro, sendo o resto de balas alem do maximo ou 0 se nao
        """
        self.ammo += quantity
        if self.ammo > self.max_ammo:
            ret = self.ammo - self.max_ammo
            self.ammo = self.max_ammo
            return ret
        else:
            return 0

    def set_shoot_volume(self, volume):
        """
        Define a altura do som de tiro
        :param volume: um float, sendo um valor entre 0 e 1 para o som maximo
        :return: None
        """
        self.shot_volume = volume
        self.no_ammo_sound.set_volume(volume)
        self.gun_sound.set_volume(volume)

    def render(self, pos=None):
        """
        Metodo herdado de GameObject responsavel por renderizar o objeto na tela
        :param pos:
        :return:
        """
        pos = pos # TODO aqui substituir por mira direta
        self.def_aim_pos(pos)
        screen = self.game_scene.get_screen()
        if screen:
            screen.blit(self.aim_img, self.aim_pos)
    def action(self, pressed_mouse=None, pressed_key=None, passed_time=0, **others):
        """
        Metodo herdado de GameObject responsavel por alterar um objeto de acordo com eventos ocorridos
        :param pressed_mouse: Evento de pressionamento de botões do mouse
        :param pressed_key: Evento de pressionamento de botões do teclado
        :param passed_time: O tempo passado de acordo com a taxa de frame
        :param others: Outros eventos
        :return:
        """
        if pressed_mouse is None:
            pressed_mouse = []
        self.reload += passed_time
        if self.reload >= self.speed:
            if pressed_mouse[2]:
                self.shooter()


class Zombie(GameObject):
    def __init__(self, game_scene, zombie_sound=None, default_sprite=None, sprite_sequences=None, pos=(), life=100,
                 speed=200):
        """
        :param game_scene:
        :param zombie_sound:
        :param default_sprite:
        :param sprite_sequences:
        :param pos:
        :param life:
        :param speed:
        """
        super(Zombie, self).__init__(game_scene, pos=pos)
        if sprite_sequences is None:
            sprite_sequences = {}
        self.sprite_sequences = sprite_sequences
        self.default_sprite = default_sprite
        self.zombie_sound = zombie_sound
        self.life = life
        self.speed = speed
        self.mov = 0
        self.current_key = None
        self.headshot = False
        self.resistance = {'head': 0, 'body': 0, 'members': 0}
        self.current_sprite_sequence = []
        self.index_current_sprite = 0
        self.current_sprite = default_sprite
        self._reward = 0 # Recompensa apos morte do zumbi
        self.dir = 1 # Direçao que o zumbi anda
        self.hide_time = 20000 # Tempo para o zumbi ser retirado da tela apos morto
        self.died = False  # True caso o zumbi morra
        self.finished = False # True caso o zumbi esteja morto a algum tempo, ou sai do campo de visão
        self.scape = False # True caso o zumbi sai do campo de visão


    def cause_damage(self, damage, member):
        if self.life > 0:
            self.life -= ((10 - self.resistance[member]) * damage)
            if self.life <= 0:
                self.die(member)
            return True
        self.die(member)
        return False


    def get_reward(self):
        """
        Recupera a recompensa atribuida ao zumbi morto, e zera a variavel _reward
        :return: Um inteiro, sendo a quantidade de pontos ganhos
        """
        ret = self._reward
        self._reward = 0
        return ret

    def die(self, member, die_sprites='die'):
        self.speed = 100
        self.life = 0
        self._reward = 5 # Todo mudar recompensa
        if member == 'head':
            die_sprites = 'headshot'
            self.speed = 70
            self._reward = 10  # Todo mudar recompensa
        self.def_current_sprite_sequence(die_sprites)  # Todo pode gerar um KeyError

    def walk(self, dir=0):
        if self.index_current_sprite < len(self.current_sprite_sequence) - 1:
            self.index_current_sprite += 1
        else:
            self.index_current_sprite = 0
        self.posX -= (dir * (self.current_sprite.get_rect().size[0] / 10))


    def update(self, passed_time):
        self.mov += passed_time
        if self.died:
            if self.mov > self.hide_time:
                self.finished = True
            return

        if self.mov >= self.speed:
            # Zombie escapa
            if self.posX < -200 and self.dir == 1 or self.posX > self.game_scene.w + 200 and self.dir == -1:
                self.scape = True
                self.finished = True
                self.sound()
            if self.current_key == 'walk':
                self.walk(self.dir)
            elif self.current_key == 'headshot' or self.current_key == 'die':
                if self.index_current_sprite < len(self.current_sprite_sequence) - 1:
                    self.index_current_sprite += 1
                else:
                    self.index_current_sprite = len(self.current_sprite_sequence) - 1
                    self.died = True
            self.current_sprite = self.current_sprite_sequence[self.index_current_sprite]
            self.mov -= self.speed

    def set_resistance(self, head=0, body=0, members=0):
        self.resistance['head'] = head
        self.resistance['body'] = body
        self.resistance['members'] = members

    def set_zombie_volume(self, volume):
        self.zombie_sound.set_volume(volume)


    def add_sprite_sequence(self, sprite_key, sprite_sequence):
        self.sprite_sequences[sprite_key] = sprite_sequence

    def get_sprite_sequence(self, sprite_sequence_name):
        return self.sprite_sequences[sprite_sequence_name]

    def get_currrent_sprite_sequence(self):
        return self.current_sprite_sequence

    def def_current_sprite_sequence(self, key):
        self.index_current_sprite = -1
        self.current_sprite_sequence = self.get_sprite_sequence(key)
        self.current_key = key

    def sound(self):
        self.zombie_sound.play()

    def get_member_in_point(self, point):
        sizeX = self.current_sprite.get_rect().size[0]
        sizeY = self.current_sprite.get_rect().size[1]
        sizesY = percent_body_zombieY(sizeY, 17, 27, 40)
        pointY_in_sprite = self.get_pos_gun_subsurface(point)[1]

        if pointY_in_sprite < sizesY[0]:
            return 'head'
        elif sizesY[0] < pointY_in_sprite < sizesY[2]:
            return 'body'  # TODO verificar tiro no braco
        else:
            return 'members'

    def get_pos_gun_subsurface(self, point):
        return int(point[0] - self.posX), int(point[1] - self.posY)

    def render(self, pos=None):
        self.game_scene.get_screen().blit(self.current_sprite, (self.posX, self.posY))


    def action(self, pressed_mouse=None, pressed_key=None, passed_time=0, **others):
        if pressed_key is None:
            pressed_key = []
        if pressed_mouse is None:
            pressed_mouse = []
        self.update(passed_time)
        self.depth = self.posY
        for gun in self.game_scene.get_guns():
            # TODO analizar pixel
            p = gun.recover_shoot()
            if p and (self.current_key != 'headshot' and self.current_key != 'die'):
                if self.current_sprite.get_rect(x=self.posX, y=self.posY).collidepoint(p):
                    if self.current_sprite.get_at(self.get_pos_gun_subsurface(p)) != pygame.Color(0, 0, 0, 0):
                        self.cause_damage(gun.get_damage(), self.get_member_in_point(p))
