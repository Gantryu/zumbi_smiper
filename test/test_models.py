import  unittest
from model.game_object import *
from helper.pygame_helper import *


class TestGameObject(unittest.TestCase):
    
    def testCreateGameObject(self):
        go = GameObject
        self.assertEqual(go, GameObject)

class TestZumbi(unittest.TestCase):

    def testGetSpriteSequence(self):
        z = Zombie(None)
        z.add_sprite_sequence('teste', ['w1', 'w2'])
        assert(z.get_sprite_sequence('teste'))


    def testRewardZumbi(self):
        z = Zombie(None)
        z._reward = 10
        ret = z.get_reward()
        self.assertEqual(ret, 10)
        self.assertEqual(z._reward, 0)


