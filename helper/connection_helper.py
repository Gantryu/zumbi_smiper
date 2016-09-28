import pygame
import re

# Expressao regular para validacao do comando recebido do cliente
rex = re.compile(' {0,1}\w{2}\((-|\w|,)+\)')

def validate_comand(command):
    '''
    Valida se o comando recebido pela rede é válido
    :param command: Uma string, sendo o comando a ser validado
    :return: Verdadeiro ou falso
    '''
    if(rex.match(command) != None):
        return True
    return False

def generate_str_connection(host, port,  pass_key = "password"):
    '''
    Gera uma string que será usada pelo cliente para se conectar ao servidor
    :param host: Uma string, sendo o endereço da maquina (o ip)
    :param port: Um inteiro, sendo a porta na qual o cliente ira conectar
    :param pass_key: Uma string, sendo uma senha para autenticar a conexão
    :return: Uma string, na qual o cliente usará para se conectar
    '''
    # Todo validar a palavra passe
    return '('+host+','+str(port)+','+pass_key+')'


def split_comands(str_comands):
    '''
    Transforma uma string em um vetor de comandos
    :param str_comands: Uma string, sendo os comandos todos em uma unica string
    :return: Um vetor, na qual terá varias string cortadas por " " [espaço]
    '''
    return str_comands.split(" ");
