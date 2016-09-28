__author__ = 'gustavosmc'

import qrcode
import io
import base64
from io import BytesIO
from PIL import Image




def generate_qrcode(text, size = 4, border = 2):
    """
    Gera uma imagem qr code
    :param size: um inteiro, sendo o tamanho da imagem, padrao = 4
    :param border: um inteiro, sendo a borda da imagem, padrao = 2
    :param text: uma string, sendo o texto a ser impresso em qrcode na imagem
    :return: Pil.Image, uma imagem contendo o texto passado no parametro em formato qrcode
    """
    img = qrcode.make(text, box_size=size, border = border)
    output = io.BytesIO()
    img.save(output, "GIF")
    output.seek(0)
    output_s = output.read()
    b64 = base64.b64encode(output_s).decode()
    image = Image.open(BytesIO(base64.b64decode(b64)))
    output.close()
    return image