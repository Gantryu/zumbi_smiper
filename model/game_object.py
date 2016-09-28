import pygame
from helper.game_object_helper import *

class Bag(object):
  def __init__(self, objects = []):
      self.objects = objects


  def add_object(self, object):
      self.objects.append(object)


  def remove_object(self, object):
      self.objects.remove(object)




class GameObject(object):
    """ Representa um objeto qualquer do jogo """

    def __init__(self, game_scene, depth = 0, pos = ()):
        self.game_scene = game_scene
        self.depth = depth
        self.posX, self.posY = 0, 0
        if (len(pos) == 2):
            self.posX = pos[0]
            self.posY = pos[1]


    def render(self,  pos = None):
        '''
        Metodo abstrato, renderiza um GameObject na tela
        :param pos: uma tupla (x,y), sendo as posicoes onde o objeto sera renderizado
        :return: None
        '''
        pass

    def action(self, pressed_mouse = [], pressed_key = [], passed_time = 0, **others):
        '''
        Metodo abstrato, acoes a serem executadas ao chamar o metodo em um GameObject
        :param mouse: eventos, sendo os eventos do mouse
        :param key: eventos, sendo os eventos do teclado
        :param others: outros parametros
        :return:
        '''
        pass

    def getKey(self):
        return self.depth


class Gun(GameObject):


    def __init__(self, game_scene, gun_img, aim_img, gun_sound = None, gun_reload_sound = None, no_ammo_sound = None,
                 speed = 0, ammo = 0, max_ammo = 10, damage = 5):
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
        self.depth = 99999 # Um valor alto de profundidade pra ficar sempre a frente
        self.damage=damage

    def def_aim_pos(self, pos):
        '''
        Define a posicao atual da mira
        :param pos: uma tupla (x, y), sendo os valores de x e y onde será renderizada a mira
        esses valores serao alterados de acordo com o tamanho da mira para centralizar
        :return: None
        '''
        if pos: self.aim_pos = (pos[0] - (self.aim_img.get_width() / 2), pos[1] - (self.aim_img.get_height() / 2))

    def get_aim_pos(self):
        return (self.aim_pos[0] + self.aim_img.get_width() / 2, self.aim_pos[1] + self.aim_img.get_height() / 2)

    def set_damage(self, damage):
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
        '''
        Atira e zera o tempo para recarregar
        :return: None
        '''
        if self.ammo > 0:
            self.shoot = self.get_aim_pos()
            self.gun_sound.play()
            self.ammo -= 1
        else:
            self.no_ammo_sound.play()
        self.reload = 0

    def recover_shoot(self):
        return self.shoot




    def recharge_ammo(self, quant):
        '''
        Recarrega a arma
        :param quant: um inteiro, sendo a quantidade de balas a serem adicionadas
        :return: um inteiro, sendo o resto de balas alem do maximo ou 0 se nao
        '''
        self.ammo += quant
        if self.ammo > self.max_ammo:
            ret = self.ammo - self.max_ammo
            self.ammo = self.max_ammo
            return ret
        else: return 0


    def set_shoot_volume(self, volume):
        '''
        Define a altura do som de tiro
        :param volume: um float, sendo um valor entre 0 e 1 para o som maximo
        :return: None
        '''
        self.shot_volume = volume
        self.no_ammo_sound.set_volume(volume)
        self.gun_sound.set_volume(volume)


    def render(self, pos = None):
        pos =  self.game_scene.get_pygame().mouse.get_pos()
        self.def_aim_pos(pos)
        screen = self.game_scene.get_screen()
        if screen:
            screen.blit(self.aim_img, self.aim_pos)


    def action(self, pressed_mouse = [], pressed_key = [], passed_time = 0, **others):
        self.reload += passed_time
        if self.reload >= self.speed:
            if pressed_mouse[2]: self.shooter()



class Zombie(GameObject):
    def __init__(self, game_scene, zombie_sound, default_sprite = None, sprite_sequences=None, pos=(), life = 100,
                 speed = 200):
        super(Zombie, self).__init__(game_scene, pos = pos)
        if sprite_sequences is None:
            sprite_sequences = {}
        self.sprite_sequences = sprite_sequences
        self.default_sprite = default_sprite
        self.zombie_sound = zombie_sound
        self.set_zombie_volume(0.1)
        self.life = life
        self.speed = speed
        self.mov = 0
        self.current_key = None
        self.headshot = False

        self.resistence = {'head':0, 'body':0, 'members':0}

        self.current_sprite_sequence = []
        self.index_current_sprite = 0
        self.current_sprite = default_sprite

    def cause_damage(self, damage, member):
        if self.life > 0:
            self.life -= ((10 - self.resistence[member]) * damage)
            return True
        self.die(member)
        return False

    def die(self, member, die_sprites='die'):
        self.speed = 100
        self.life = 0
        if member == 'head':
            die_sprites = 'headshot'
            self.speed = 50
        self.def_current_sprite_sequence(die_sprites) # pode gerar um KeyError

    def update(self, passed_time):
        self.mov += passed_time
        if self.mov >= self.speed:  # Todo otimizar
            if self.current_key == 'walk':
                if self.index_current_sprite < len(self.current_sprite_sequence) - 1:
                    self.index_current_sprite += 1
                else:
                    self.index_current_sprite = 0
                self.posX -= self.current_sprite.get_rect().size[0] / 10
            elif self.current_key == 'headshot' or self.current_key == 'die':
                if self.index_current_sprite < len(self.current_sprite_sequence) - 1:
                    self.index_current_sprite += 1
                else:
                    self.index_current_sprite = len(self.current_sprite_sequence) - 1
            self.current_sprite = self.current_sprite_sequence[self.index_current_sprite]
            self.mov = 0


    def set_resistence(self, head=0, body=0, members=0):
        self.resistence['head'] = head
        self.resistence['body'] = body
        self.resistence['members'] = members

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


    def get_member_in_point(self, point):
        sizeX = self.current_sprite.get_rect().size[0]
        sizeY = self.current_sprite.get_rect().size[1]
        sizesY = percent_body_zombieY(sizeY, 17, 27, 40)
        pointY_in_sprite = self.get_pos_gun_subsurface(point)[1]

        if(pointY_in_sprite < sizesY[0]): return 'head'
        elif(pointY_in_sprite > sizesY[0] and pointY_in_sprite < sizesY[2]): return 'body' # TODO verificar tiro braco
        else: return 'members'



    def get_pos_gun_subsurface(self, point):
        return int(point[0] - self.posX), int(point[1] - self.posY)

    def render(self, pos = None):
        self.game_scene.get_screen().blit(self.current_sprite, (self.posX, self.posY))


    def action(self, pressed_mouse = [], pressed_key = [], passed_time = 0, **others):
        self.update(passed_time)
        self.depth = self.posY
        for gun in self.game_scene.get_guns():
            # TODO analizar pixel
           p = gun.recover_shoot()
           if p and (self.current_key != 'headshot'):
               if self.current_sprite.get_rect(x=self.posX, y=self.posY).collidepoint(p):
                    if self.current_sprite.get_at(self.get_pos_gun_subsurface(p)) != pygame.Color(0,0,0,0):
                        self.cause_damage(gun.get_damage(), self.get_member_in_point(p))









