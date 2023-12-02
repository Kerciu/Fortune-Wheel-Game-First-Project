class Player:
    """
    Class Players: Contains attributes:
    :param nickname: Player's nickname
    :type nickname: str

    :param points: Player's points, deafults to 0
    :type points: int

    :param prizes: Player's prizes, deafults to None
    :type prizes: str
    """
    def __init__(self, nickname, points=0, prizes=None):
        self._nickname = nickname
        self._points = points
        self._prizes = prizes

    def nickname(self):
        return self._nickname
    
    def points(self):
        return self._points
    
    def set_nickname(self, new_nickname):
        return self._nickname == new_nickname
    
    def set_points(self, new_points):
        return self._points == new_points
    
    def prizes(self):
        return self._prizes
    
    def set_prizes(self, new_prizes):
        return self._prizes == new_prizes

    def info(self):
        name = self._nickname
        exception_points = 'point' if self._points == 1 else 'points'
        return f"{name.capitalize()} has {self._points} {exception_points}."
    
    def __str__(self):
        return self.info()
    
class Game:
    def __init__(self, player, points):
        self.player = player
        self.enemies = points
        self._result = None

    # def play(self, rounds):
    #     print('Starting the game')
    #     for round in range(1, rounds + 1):
    #         print(f'Round: {round}')
    #         target, damage, status = self.player.attack(self.enemies)
    #         if target:
    #             if status:
    #                 print(f'{target.name()} took {damage} points of damage.')
    #                 if not target.is_alive():
    #                     print(f'{target.name()} died.')
    #                     self.enemies.remove(target)
    #                 else:
    #                     print(f'{target.name()} escaped')
    #     self._result = bool(self.enemies)
    #     return self._result