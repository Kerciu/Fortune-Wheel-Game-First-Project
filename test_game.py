from players import Player
from fortune_wheel import (introduction,
                           fortune_wheel,
                           load_from_json,
                           update_hidden_word,
                           check_guessed_letter,
                           check_guessed_vowel,
                           hide_word,
                           remove_player_points,
                           inform_players,
                           end_inform_players,
                           play_round,
                           check_final_input_letters,
                           guess_full_password,
                           winner,
                           pre_final,
                           final_round,
                           countdown,
                           reveal_letters,
                           guess_final_password,
                           )
import sys
import pytest
import json
import io
import time


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
    assert player1.nickname() == player_nickname


def test_load_from_json_file_exists():
    with open('hasla.json') as f:
        assert f is not None


def test_load_from_json_correct_output():
    result = load_from_json()
    assert isinstance(result, list)


def test_load_from_json_data_loading():
    result = load_from_json()
    assert len(result) > 0


def test_load_from_json_correct_values():
    result = load_from_json()
    assert all(isinstance(item.word(), str)
               and isinstance(item.category(), str) for item in result)


def test_load_from_json_keys_exist():
    result = load_from_json()
    assert all(hasattr(item, 'word') and
               hasattr(item, 'category') for item in result)


def test_load_from_json_file_not_empty():
    with open('hasla.json') as f:
        data = json.load(f)
        assert len(data['kategorie_i_hasla']) > 0


def test_load_from_json_keys_exist_in_data():
    with open('hasla.json') as f:
        data = json.load(f)
        for item in data['kategorie_i_hasla']:
            assert 'kategoria' in item and 'hasło' in item


def test_load_from_json_valid_json():
    try:
        with open('hasla.json') as f:
            json.load(f)
    except ValueError:
        assert False


def test_load_from_json_category_not_empty():
    result = load_from_json()
    assert all(item.category.strip() != '' for item in result)


def test_load_from_json_word_not_empty():
    result = load_from_json()
    assert all(item.word.strip() != '' for item in result)


def test_fortune_wheel_result_in_choices():
    choices = [100, 200, 300, 'BANKRUT', 'STOP']
    result = fortune_wheel(choices)
    assert result in choices


def test_fortune_wheel_result_type():
    choices = [100, 200, 300, 'BANKRUT', 'STOP']
    result = fortune_wheel(choices)
    assert isinstance(result, (int, str))


def test_fortune_wheel_choices_not_empty():
    choices = [100, 200, 300, 'BANKRUT', 'STOP']
    result = fortune_wheel(choices)
    assert choices


def test_fortune_wheel_empty_choices():
    choices = []
    result = fortune_wheel(choices)
    assert result is None


def test_fortune_wheel_choice_frequency():
    choices = [100] * 50 + [200] * 30 + [300] * 20
    results = [fortune_wheel(choices) for _ in range(100)]
    frequencies = {100: results.count(100), 200: results.count(200),
                   300: results.count(300)}
    assert frequencies == {100: 50, 200: 30, 300: 20}


def test_fortune_wheel_unique_choices():
    choices = [100, 200, 300, 'BANKRUT', 'STOP']
    results = [fortune_wheel(choices) for _ in range(100)]
    assert len(set(results)) > 1


def test_fortune_wheel_randomness():
    choices = [100, 200, 300, 'BANKRUT', 'STOP']
    results_1 = [fortune_wheel(choices) for _ in range(100)]
    results_2 = [fortune_wheel(choices) for _ in range(100)]
    assert results_1 != results_2


def test_fortune_wheel_invalid_choices():
    choices = ['100', 200, 300, 'BANKRUT', 'STOP']
    result = fortune_wheel(choices)
    assert result is None


def test_fortune_wheel_different_choices_types():
    choices = [100, 200.0, '300', 'BANKRUT', 'STOP']
    result = fortune_wheel(choices)
    assert result in choices


def test_fortune_wheel_single_choice():
    choices = [100]
    result = fortune_wheel(choices)
    assert result == 100


def test_fortune_wheel_no_choices():
    choices = []
    result = fortune_wheel(choices)
    assert result is None


def test_fortune_wheel_output_delay():
    choices = [100, 200, 300, 'BANKRUT', 'STOP']
    start_time = time.time()
    fortune_wheel(choices)
    end_time = time.time()
    elapsed_time = end_time - start_time
    expected_times = [0.05, 0.08, 0.11, 0.14, 0.17,
                      0.20, 0.23, 0.26, 0.29, 0.32, 0.35]
    assert elapsed_time in expected_times


def test_fortune_wheel_prize_picked_from_choices():
    choices = [100, 200, 300, 'BANKRUT', 'STOP']
    picked_prize = fortune_wheel(choices)
    assert picked_prize in choices


def test_fortune_wheel_shuffle_choices():
    choices = [100, 200, 300, 'BANKRUT', 'STOP']
    original_choices = choices.copy()
    fortune_wheel(choices)
    assert choices != original_choices


def test_fortune_wheel_all_choices_displayed():
    choices = [100, 200, 300, 'BANKRUT', 'STOP']
    captured_output = io.StringIO()
    sys.stdout = captured_output
    fortune_wheel(choices)
    sys.stdout = sys.__stdout__
    output = captured_output.getvalue()
    for choice in choices:
        assert str(choice) in output


def test_fortune_wheel_terminal_cleared():
    choices = [100, 200, 300, 'BANKRUT', 'STOP']
    captured_output = io.StringIO()
    sys.stdout = captured_output
    fortune_wheel(choices)
    sys.stdout = sys.__stdout__
    output = captured_output.getvalue()
    assert output.startswith('\033c')


def test_fortune_wheel_delay_increment():
    choices = [100, 200, 300, 'BANKRUT', 'STOP']
    delay_values = []
    captured_output = io.StringIO()
    sys.stdout = captured_output
    fortune_wheel(choices)
    sys.stdout = sys.__stdout__
    output = captured_output.getvalue()
    lines = output.split('\n')
    for i in range(len(lines) - 1):
        delay_values.append(float(lines[i+1][-4:]))
    for i in range(len(delay_values) - 1):
        assert delay_values[i+1] - delay_values[i] >= 0.01


def test_update_hidden_word():
    assert update_hidden_word('example', '------', 'e') == '------'
    assert update_hidden_word('hello', '-----', 'l') == '--ll-'
    assert update_hidden_word('python', '------', 'o') == '------'
    assert update_hidden_word('python', '------', 'z') == '------'
    assert update_hidden_word('programming', '----------', 'i') == '----------'
    assert update_hidden_word('', '', 'a') == ''
    assert update_hidden_word('test', '----', 't') == 't--t'
    assert update_hidden_word('hello', '', 'e') == ''
    assert update_hidden_word('banana', '------', 'a') == '------'
    assert update_hidden_word('algorithm', '---------', 'g') == '--g------'
    assert update_hidden_word('poland', '------', 'i') == '------'
    assert update_hidden_word('apple', '-----', 'p') == '-pp--'
    assert update_hidden_word('python', '------', 'n') == '-----n'
    assert update_hidden_word('idea', '----', 'd') == '-d--'


def test_check_guessed_letter_letter_found():
    word = 'example'
    hidden_word = '------'
    guessed_letter = 'e'
    points = 10

    updated_hidden_word, earned_points = check_guessed_letter(word,
                                                              hidden_word,
                                                              guessed_letter,
                                                              points)

    assert updated_hidden_word == 'e---e--'
    assert earned_points == 10


def test_check_guessed_letter_letter_not_found():
    word = 'example'
    hidden_word = '------'
    guessed_letter = 'z'
    points = 5

    updated_hidden_word, earned_points = check_guessed_letter(word,
                                                              hidden_word,
                                                              guessed_letter,
                                                              points)

    assert updated_hidden_word == '------'
    assert earned_points == 0


def test_check_guessed_letter_duplicate_letters():
    word = 'banana'
    hidden_word = '------'
    guessed_letter = 'a'
    points = 15

    updated_hidden_word, earned_points = check_guessed_letter(word,
                                                              hidden_word,
                                                              guessed_letter,
                                                              points)

    assert updated_hidden_word == '-a-a-a'
    assert earned_points == 15


def test_check_guessed_vowel_vowel_found():
    word = 'example'
    hidden_word = '------'
    guessed_vowel = 'a'

    vowel_found, updated_hidden_word = check_guessed_vowel(word,
                                                           hidden_word,
                                                           guessed_vowel)

    assert vowel_found is True
    assert updated_hidden_word == '--a---'


def test_check_guessed_vowel_vowel_not_found():
    word = 'example'
    hidden_word = '------'
    guessed_vowel = 'i'

    vowel_found, updated_hidden_word = check_guessed_vowel(word,
                                                           hidden_word,
                                                           guessed_vowel)

    assert vowel_found is False
    assert updated_hidden_word == '------'


def test_check_guessed_vowel_not_a_vowel():
    word = 'example'
    hidden_word = '------'
    guessed_vowel = 'x'

    vowel_found, updated_hidden_word = check_guessed_vowel(word,
                                                           hidden_word,
                                                           guessed_vowel)

    assert vowel_found is False
    assert updated_hidden_word == '------'


def test_check_guessed_vowel_accented_vowel():
    word = 'próba'
    hidden_word = '-----'
    guessed_vowel = 'ó'

    vowel_found, updated_hidden_word = check_guessed_vowel(word,
                                                           hidden_word,
                                                           guessed_vowel)

    assert vowel_found is True
    assert updated_hidden_word == '--ó--'


def test_hide_word_all_hidden():
    word = 'example'
    guessed_letters = []

    hidden = hide_word(word, guessed_letters)
    assert hidden == '-------'


def test_hide_word_some_guessed():
    word = 'example'
    guessed_letters = ['e', 'x']

    hidden = hide_word(word, guessed_letters)
    assert hidden == 'ex----e'


def test_hide_word_all_guessed():
    word = 'example'
    guessed_letters = ['e', 'x', 'a', 'm', 'p', 'l']

    hidden = hide_word(word, guessed_letters)
    assert hidden == 'example'


def test_hide_word_empty_word():
    word = ''
    guessed_letters = ['a', 'b', 'c']

    hidden = hide_word(word, guessed_letters)
    assert hidden == ''


def test_hide_word_special_characters():
    word = 'special!@#'
    guessed_letters = ['e', 's', 'p', 'c', 'i', 'a', 'l']

    hidden = hide_word(word, guessed_letters)
    assert hidden == 'special!@#'


def test_remove_player_points_all_positive():
    players = [
        Player("Alice", points=10),
        Player("Bob", points=5),
        Player("Charlie", points=0)
    ]

    remove_player_points(players)

    for player in players:
        assert player.points() == 0


def test_remove_player_points_some_positive():
    players = [
        Player("David", points=0),
        Player("Eva", points=20),
        Player("Frank", points=0)
    ]

    remove_player_points(players)

    assert players[0].points() == 0
    assert players[1].points() == 0
    assert players[2].points() == 0


def test_remove_player_points_all_zero():
    players = [
        Player("Grace", points=0),
        Player("Henry", points=0),
        Player("Isabella", points=0)
    ]

    remove_player_points(players)

    assert players[0].points() == 0
    assert players[1].points() == 0
    assert players[2].points() == 0


def test_inform_players_output():
    players = [
        Player("Alice", points=10),
        Player("Bob", points=5),
        Player("Charlie", points=0)
    ]

    expected_output = (
        "======Aktualny stan graczy======\n"
        "Alice ma 10 punktów.\n"
        "Bob ma 5 punktów.\n"
        "Charlie ma 0 punktów.\n"
        "================================"
    )

    captured_output = io.StringIO()
    sys.stdout = captured_output
    inform_players(players)
    sys.stdout = sys.__stdout__
    assert captured_output.getvalue().strip() == expected_output.strip()


def test_end_inform_players():
    players = [
        Player("Alice", perm_points=10),
        Player("Bob", perm_points=5),
        Player("Charlie", perm_points=1)
    ]

    expected_output = (
        "====== Stan graczy na koniec rundy ======\n"
        "Alice ma 10 punktów.\n"
        "Bob ma 5 punktów.\n"
        "Charlie ma 1 punkt.\n"
        "========================================="
    )

    captured_output = io.StringIO()
    sys.stdout = captured_output
    end_inform_players(players)
    sys.stdout = sys.__stdout__
    assert captured_output.getvalue().strip() == expected_output.strip()


def test_player_info_with_prizes():
    player = Player("Alice", points=10)
    player.add_prizes("Sprzęt AGD")
    player.add_prizes("Pobyt w spa")

    prize_list = ["Sprzęt AGD", "Pobyt w spa"]

    prizes = f'\t\nWygrane nagrody: {prize_list}'
    name = player.nickname()

    expected_info = f"{name} ma {player.points()} punktów." + prizes

    assert expected_info == player.info()


def test_winner_basic_scenario():
    players = [
        Player("Player1", perm_points=100),
        Player("Player2", perm_points=150),
        Player("Player3", perm_points=80)
    ]
    assert winner(players).nickname() == "Player2"


def test_winner_tie_scenario():
    players = [
        Player("Player1", perm_points=200),
        Player("Player2", perm_points=180),
        Player("Player3", perm_points=200)
    ]
    assert winner(players).nickname() in ["Player1", "Player3"]


def test_winner_empty_players():
    try:
        players = []
        winner(players)
    except ValueError as e:
        assert str(e) == "max() arg is an empty sequence"


def test_winner_negative_points():
    players = [
        Player("Player1", perm_points=-50),
        Player("Player2", perm_points=100),
        Player("Player3", perm_points=150)
    ]
    assert winner(players).nickname() == "Player3"


def test_pre_final_winner_in_players(monkeypatch):
    class MockPlayer:
        def __init__(self, nickname, points):
            self.nickname_val = nickname
            self.points_val = points

        def nickname(self):
            return self.nickname_val

        def points(self):
            return self.points_val

        def perm_points(self):
            return self.points_val

    winner_player = MockPlayer("Alice", points=100)
    players = [winner_player, MockPlayer("Bob", points=80),
               MockPlayer("Charlie", points=70)]

    monkeypatch.setattr('builtins.input', lambda _: '1')

    captured_output = io.StringIO()
    sys.stdout = captured_output

    pre_final(players)

    sys.stdout = sys.__stdout__

    expected_output = ["Bob", "Charlie"]
    for name in expected_output:
        assert name in captured_output.getvalue()


@pytest.mark.parametrize("hidden_word, actual_word", [
    ("-------", "ukraine"),
    ("-----", "apple"),
])
def test_reveal_letters(hidden_word, actual_word):
    revealed = reveal_letters(hidden_word, actual_word)
    assert len(revealed) == len(hidden_word)
    assert set(revealed) <= set('-' + actual_word)


def test_countdown(capfd):
    countdown()

    captured = capfd.readouterr()
    output_lines = captured.out.strip().split('\r')
    expected_output = [
        "Pozostało: 10 sekund",
        "Pozostało: 9 sekund",
        "Pozostało: 8 sekund",
        "Pozostało: 7 sekund",
        "Pozostało: 6 sekund",
        "Pozostało: 5 sekund",
        "Pozostało: 4 sekundy",
        "Pozostało: 3 sekundy",
        "Pozostało: 2 sekundy",
        "Pozostało: 1 sekunda",
        "Pozostało: 0 sekund"
    ]
    assert len(output_lines) == len(expected_output)

    for idx, line in enumerate(expected_output):
        assert line in output_lines[idx]


def test_guess_final_password_correct_guess(capfd, monkeypatch):
    player = "Player1"
    word = "example"
    update_word = "-------"

    input_values = ["example"]
    monkeypatch.setattr('builtins.input', lambda _: input_values.pop(0))

    guess_final_password(player, word, update_word)

    captured = capfd.readouterr()
    assert "Gratulacje" in captured.out


@pytest.mark.parametrize("hidden_word, actual_word", [
    ("-------", "ukraine"),
    ("-----", "apple"),
])
def test_reveal_letters(hidden_word, actual_word):
    revealed = reveal_letters(hidden_word, actual_word)
    assert len(revealed) == len(hidden_word)
    assert set(revealed) <= set('-' + actual_word)


def test_countdown(capfd):
    countdown()

    captured = capfd.readouterr()
    output_lines = captured.out.strip().split('\r')
    expected_output = [
        "Pozostało: 10 sekund",
        "Pozostało: 9 sekund",
        "Pozostało: 8 sekund",
        "Pozostało: 7 sekund",
        "Pozostało: 6 sekund",
        "Pozostało: 5 sekund",
        "Pozostało: 4 sekundy",
        "Pozostało: 3 sekundy",
        "Pozostało: 2 sekundy",
        "Pozostało: 1 sekunda",
        "Pozostało: 0 sekund"
    ]
    assert len(output_lines) == len(expected_output)

    for idx, line in enumerate(expected_output):
        assert line in output_lines[idx]


def test_guess_final_password_correct_guess(capfd, monkeypatch):
    player = "Player1"
    word = "example"
    update_word = "-------"

    input_values = ["example"]
    monkeypatch.setattr('builtins.input', lambda _: input_values.pop(0))

    guess_final_password(player, word, update_word)

    captured = capfd.readouterr()
    assert "Gratulacje" in captured.out


def test_guess_final_password_wrong_guess(capfd, monkeypatch):
    player = "Player1"
    word = "example"
    update_word = "-------"

    input_values = ["wrong_guess"]
    monkeypatch.setattr('builtins.input', lambda _: input_values.pop(0))

    guess_final_password(player, word, update_word)

    captured = capfd.readouterr()
    assert "Niestety" in captured.out
