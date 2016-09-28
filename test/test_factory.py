import unittest
from main.factory import *

class TestZombieFactory(unittest.TestCase):
    zf = ZombieFactory()
    def testGZombieWallk(self):
        print(self.zf.g_zombie_walk())

    def testGZombieDie(self):
        print(self.zf.g_zombie_die())
