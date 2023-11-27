from players import Player
import fortune_wheel
import pytest

def test_player_object_creation(monkeypatch):
    input_values = iter(["Janusz", "Grazyna", "Zygmunt"])
    monkeypatch.setattr('builtins.input', lambda _: next(input_values))
    player1, player2, player3 = fortune_wheel.introduction()
    assert player1 is not None
    assert player2 is not None
    assert player3 is not None
    assert isinstance(player1, Player)
    assert isinstance(player2, Player)
    assert isinstance(player3, Player)


def test_player_name_creation(monkeypatch):
    player_name = 'Janusz'
    monkeypatch.setattr('builtins.input', lambda _: player_name)
    player1, _, _ = fortune_wheel.introduction()
    assert player1.nickname() == player_name


def test_player_nickname():
    player = Player('Gerwazy', 200)
    assert player.nickname() == 'Gerwazy'


def test_player_points():
    player = Player('Gerwazy', 200)
    assert player.points() == 200


def test_player_info_one_point():
    player = Player('Gerwazy', 1)
    assert player.info() == 'Gerwazy has 1 point.'


def test_player_info_not_one_point():
    player = Player('Gerwazy', 200)
    assert player.info() == 'Gerwazy has 200 points.'

