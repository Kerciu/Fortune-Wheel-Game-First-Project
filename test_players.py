from players import Player


def test_player_nicknickname():
    player = Player('Gerwazy', 200)
    assert player.nicknickname() == 'Gerwazy'


def test_player_points():
    player = Player('Gerwazy', 200)
    assert player.points() == 200


def test_player_info_one_point():
    player = Player('Gerwazy', 1)
    assert player.info() == 'Gerwazy has 1 point.'


def test_player_info_not_one_point():
    player = Player('Gerwazy', 200)
    assert player.info() == 'Gerwazy has 200 points.'
