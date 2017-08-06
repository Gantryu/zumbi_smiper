from connection.connection import *
import unittest
import socket


class TestServer(unittest.TestCase):

    def testStartServer(self):
        server = Server()
        server.start_server()
        self.assertEqual(server.running, True, " Servidor funcionando")
        server.close_server()

    # def testWaitNewClient(self):
    #     server = Server()
    #     server.start_server()
    #     server.wait_new_connection()
    #     tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     dest = ("localhost", 7000)
    #     tcp.connect(dest)
    #     tcp.send('SC(EXITIN)'.encode("UTF8"))
    #     server.close_server()
    #
    # def testBufferMsg(self):
    #     # TODO as vezes da erro
    #     server = Server()
    #     server.start_server()
    #     server.wait_new_connection()
    #     tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     dest = ("localhost", 7000)
    #     tcp.connect(dest)
    #     tcp.send(" tt(A)".encode("utf-8"))
    #     tcp.send(" tt(B)".encode("utf-8"))
    #     tcp.send(" tt(C)".encode("utf-8"))
    #     tcp.send(" tt(D)".encode("utf-8"))
    #     print("clientes : ", server.clients[0].get_recv_msg())
    #     server.clients[0].recover_first_recv_message()
    #     test = server.clients[0].get_recv_msg()[:] # [:] faz uma copia de uma lista
    #     print("clientes : ", server.clients[0].get_recv_msg())
    #     tcp.send('SC(EXITIN)'.encode("utf-8"))
    #     server.close_server()
    #     #self.assertEqual(test, ['tt(B)', 'tt(C)', 'tt(D)'])

