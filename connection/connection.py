__author__ = 'gustavosmc'
'''
Este modulo contém classes responsáveis pela conexão entre servidor
e clientes
'''
import socket
from threading import *
from helper.connection_helper import *


class Server(object):
    """ Classe servidora, acesso remoto, gerenciar clientes"""


    def __init__(self, host='', port=5000):
        """
        :param host: uma string, sendo o ip da interface na qual sera criado o servidor
        :param port: um inteiro, sendo a porta na qual sera criado o servidor
        :param clients: uma lista, com clientes ja definidos para conectarem
        """
        self.rec_messages = []
        self.serv_socket = None
        self.host = host
        self.port = port
        self.running = False
        self.serv_thread = None

    # noinspection PyBroadException
    def start_server(self, port=5000):
        self.port = port
        """
        :param port: inteiro porta, sendo a porta na qual ira iniciar a escuta do servidor padrao = 5000
        :return: True se conectou ou False se não conseguiu conectar
        """
        try:
            self.addr = (self.host, self.port)  # VARIAVEL CONTENDO OS VALORES DO IP E PORTA
            self.serv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Usando um protocolo udp
            self.serv_socket.bind(self.addr)  # Define para qual IP e porta o servidor deve aguardar
        except :
            print("falha ao iniciar servidor")
            return False
        if self.serv_socket != None:
            self.running = True
            self.serv_thread = ServerThread(self)
            self.serv_thread.start()




    def recover_last_message(self):
        return self.rec_messages.pop(-1)


    def close_server(self):
        """
        Envia mensagem dizendo que vai encerrar a todos os clientes e finaliza conexão com todos
        estes no servidor e os remove da lista de clientes conectados
        :return:
        """

        self.serv_socket.close()
        self.running = False

    def closed(self):
        """
        Verifica se o servidor está online
        :return: verdadeiro ou falso
        """
        # Solicita status de funcionamento ao objeto interno serv_socket
        return self.serv_socket._closed


    def size_messages(self):
        """
        Verifica e retorna a quantidade de mensagens recebidas de clientes
        :return:
        """
        return len(self.rec_messages)


class ServerThread(Thread):

    def __init__(self, server):
        Thread.__init__(self)
        self.server = server

    def run(self):
        while self.server.running:
            msg, client = self.server.serv_socket.recvfrom(512)
            msg = msg.decode('utf-8')
            if msg.lower() == 'close'.lower():
                self.server.close_server()
            self.server.rec_messages.append(msg)


# TODO implementar cliente
class Client(object):
    None





class MacInfo(object):
    def get_host_name(self):
        """
        Metodo para pegar o nome do host
        :return: uma string, sendo o nome do host
        """
        return socket.gethostname()

    def get_interface_ip(self, lan):
        """
        Metodo para pegar o ip da rede
        :param lan: uma string, sendo o nome da interface de rede
        :return: o ip da interface caso exista na lista ou None
        """
        import netifaces as ni
        try:
            intf = self.get_interfaces()
            ip = ni.ifaddresses(intf[intf.index(lan)])[2][0]["addr"]
            print(ip)
            return ip
        except Exception:
            return None


    def get_interfaces(self):
        """
        Metodo para pegar todas as interfaces de rede
        :return: uma lista, com todas as interfaces de rede acessiveis
        """
        import netifaces as ni
        return ni.interfaces()[2:]



