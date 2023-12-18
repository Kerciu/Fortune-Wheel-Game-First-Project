class WrongWordError(Exception):
    pass


class WrongCategoryError(Exception):
    pass


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
    def __init__(self, nickname, points=0, perm_points=0, prizes=None):
        self._nickname = nickname
        self._points = points
        self._perm_points = perm_points
        self._prizes = [] if not prizes else prizes

    def nickname(self):
        return self._nickname

    def points(self):
        return self._points

    def perm_points(self):
        return self._perm_points

    def prizes(self):
        return self._prizes

    def set_nickname(self, new_nickname):
        self._nickname = new_nickname

    def add_perm_points(self, new):
        self._perm_points += new

    def add_points(self, new_points):
        self._points += new_points

    def remove_points(self, new_points):
        self._points -= new_points

    def add_prizes(self, new_prizes):
        self._prizes.append(new_prizes)

    def info(self):
        nickname = self._nickname
        exception_points = 'point' if self._points == 1 else 'points'
        return f"{nickname.capitalize()} has {self._points} {exception_points}."

    def __str__(self):
        return self.info()


class WordAndCategory:
    """
    Class WordAndCategory: Contains attributes:
    :param word: Shown password to guess
    :type word: str

    :param category: Shown category to guess
    :type category: str
    """
    def __init__(self, word, category):
        if not isinstance(word, str):
            e = "Slowo do odgadniecia musi byc w formacie string!"
            raise WrongWordError(e)
        self._word = word
        if not isinstance(category, str):
            e = "Kategoria musi być w formacie string!"
            raise WrongCategoryError(e)
        self._category = category

    def word(self):
        return self._word

    def category(self):
        return self._category
