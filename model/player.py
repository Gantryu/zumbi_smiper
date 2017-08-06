class Player(object):
    def __init__(self, nick, avatar = None, guns=None, money = 0):
        if not guns is None:
            self.guns = []
        self._money = money
        self.nick = nick
        self.avatar = avatar

    def deposity(self, money):
        if money > 0:
            self._money += money

    def pay(self, valor):
        if valor > 0 and self.money > valor:
            self._money -= valor
            return True
        return False


