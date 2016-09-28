import pygame
import os

def load_img(img, dimension = None):
    '''
    Carrega uma imagem para a memoria, usando pygame
    :param img: uma string, sendo o caminho da imagem
    :return: um objeto pygame.Image
    '''
    # todo tratar excessões
    img = pygame.image.load(os.path.join(img))
    if dimension:
        img = pygame.transform.scale(img, dimension)
    return img


def load_sound(sound):
    '''
    Carrega um som para a memoria, usando pygame
    :param sound: uma string, sendo o caminho do audio
    :return: um objeto pygame.mixer.Sound
    '''
    sound = pygame.mixer.Sound(os.path.join(sound))
    return sound