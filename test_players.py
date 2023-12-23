import pytest
from players import (Player,
                    WordAndCategory,
                    WrongCategoryError,
                    WrongWordError)


@pytest.fixture
def player():
    return Player("John")


def test_player_initialization(player):
    assert player.nickname() == "John"
    assert player.points() == 0
    assert player.perm_points() == 0
    assert player.prizes() == []


def test_set_nickname(player):
    player.set_nickname("Jane")
    assert player.nickname() == "Jane"


def test_add_points(player):
    player.add_points(100)
    assert player.points() == 100


def test_remove_points(player):
    player.add_points(50)
    player.remove_points(30)
    assert player.points() == 20


def test_remove_points_greater_than_current(player):
    player.remove_points(100)
    assert player.points() == 0


def test_add_prizes(player):
    player.add_prizes("Prize 1")
    player.add_prizes("Prize 2")
    assert player.prizes() == ["Prize 1", "Prize 2"]


def test_info_plural_points(player):
    player.add_points(5)
    assert player.info() == "John has 5 points."


def test_info_singular_points(player):
    player.add_points(1)
    assert player.info() == "John has 1 point."


def test_add_perm_points(player):
    player.add_perm_points(50)
    assert player.perm_points() == 50


@pytest.fixture
def word_and_category():
    return WordAndCategory("Apple", "Fruit")


def test_word_and_category_initialization():
    word_cat = WordAndCategory("Banana", "Fruit")
    assert word_cat.word() == "Banana"
    assert word_cat.category() == "Fruit"


def test_word_and_category_invalid_word_type():
    with pytest.raises(WrongWordError):
        WordAndCategory(123, "Fruit")


def test_word_and_category_invalid_category_type():
    with pytest.raises(WrongCategoryError):
        WordAndCategory("Apple", 123)


def test_word_and_category_word():
    word_cat = WordAndCategory("Banana", "Fruit")
    assert word_cat.word() == "Banana"


def test_word_and_category_category():
    word_cat = WordAndCategory("Banana", "Fruit")
    assert word_cat.category() == "Fruit"


def test_word_and_category_word_and_category_are_strings():
    word_cat = WordAndCategory("Banana", "Fruit")
    assert isinstance(word_cat.word(), str)
    assert isinstance(word_cat.category(), str)


def test_word_and_category_change_word():
    word_cat = WordAndCategory("Banana", "Fruit")
    word_cat._word = "Apple"
    assert word_cat.word() == "Apple"


def test_word_and_category_change_category():
    word_cat = WordAndCategory("Banana", "Fruit")
    word_cat._category = "Food"
    assert word_cat.category() == "Food"
