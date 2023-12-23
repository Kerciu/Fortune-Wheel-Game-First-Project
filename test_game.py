from players import Player
from fortune_wheel import introduction, fortune_wheel
import pytest


def test_player_object_creation(monkeypatch):
    input_values = iter(["Janusz", "Grazyna", "Zygmunt"])
    monkeypatch.setattr('builtins.input', lambda _: next(input_values))
    player1, player2, player3 = introduction()
    assert player1 is not None
    assert player2 is not None
    assert player3 is not None
    assert isinstance(player1, Player)
    assert isinstance(player2, Player)
    assert isinstance(player3, Player)


def test_player_nickname_creation(monkeypatch):
    player_nickname = 'Janusz'
    monkeypatch.setattr('builtins.input', lambda _: player_nickname)
    player1, _, _ = introduction()
    assert player1.nicknickname() == player_nickname
