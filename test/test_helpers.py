import unittest
from helper.connection_helper import *
from helper.qrcode_helper import *
from PIL import Image
from io import BytesIO

class TestPrimeiroTeste(unittest.TestCase):
    def test(self):
        self.assertEqual(2, 2, "Primeiro Teste")


class TestConnectionHelper(unittest.TestCase):

    def testValidateCommand(self):
        msg = ' Teste validaçao comando falhou para '
        self.assertEqual(validate_comand("1234"), False, msg + "1234")
        self.assertEqual(validate_comand("st(1)"), True, msg + "st(1)")
        self.assertEqual(validate_comand("mv(100,100)"), True, msg + "mv(100,100)")

    def testGenerateStringConnection(self):
        msg = ' Teste criação de string falhou com '
        teste = "(localhost,7000,senha)"
        self.assertEqual(generate_str_connection('localhost', 7000, "senha"), teste, msg + teste)


class TestQrCodeHelper(unittest.TestCase):

    def testGenerateQrCode(self):
        img = generate_qrcode("teste")
        self.assertIsNotNone(img)
        #img.show() # descomentar para abrir a imagem
