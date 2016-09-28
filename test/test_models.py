import  unittest
from model.game_object import *
from helper.pygame_helper import *


class TestGameObject(unittest.TestCase):
    
    def testCreateGameObject(self):
        go = GameObject
        self.assertEqual(go, GameObject)

class TestZumbi(unittest.TestCase):

    def testGetSpriteSequence(self):
        z = Zombie('game_scene', load_sound('../_audio/m19.ogg'))
        z.add_sprite_sequence('teste', ['w1', 'w2'])
        assert(z.get_sprite_sequence('teste'))
