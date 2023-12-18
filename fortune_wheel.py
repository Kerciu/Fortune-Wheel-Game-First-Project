import random
import time
import os
import json
import keyboard
from players import Player, WordAndCategory


def clear_terminal():
    # Czyszczenie terminala
    os.system('cls' if os.name == 'nt' else 'clear')


def print_fences():
    print('--------------')


def fortune_wheel(choices):
    # Wylosowana losowa wartość z koła fortuny i wymieszana lista
    picked_up_prize = random.choice(choices)
    copied_choices = choices.copy()
    random.shuffle(copied_choices)

    # Wyświetlanie elementów koła fortuny z rosnącym opóźnieniem
    delay = 0.05
    for i, element in enumerate(3 * copied_choices):
        clear_terminal()
        if i == len(copied_choices) - 1:
            print(picked_up_prize)
        else:
            print(element)
        time.sleep(delay)
        # Zwiększanie opóźnienie wraz z kolejnym wyświetlanym elementem
        delay += 0.02

    # Opóźnienie przed wyświetleniem wyniku i wyczyszczenie terminala
    time.sleep(1)
    clear_terminal()
    return f'Wylosowana karta to: {picked_up_prize}'


def introduction():
    time.sleep(1)
    print("Witamy w Kole Fortuny! Przedstawcie się dzisiejsi uczestnicy!")
    time.sleep(3)
    print_fences()
    player_one = input("Graczu pierwszy, podaj swoje imię: ")
    print_fences()
    player_two = input("Graczu drugi, teraz twoja kolej: ")
    print_fences()
    player_three = input('Teraz kolej na gracza numer trzy: ')
    clear_terminal()
    introduction = f"Witam was: {player_one}, {player_two} i {player_three}\n"
    print(introduction + "Zaczynamy grę!")

    player1 = Player(player_one)
    player2 = Player(player_two)
    player3 = Player(player_three)

    players = [player1, player2, player3]
    return players


def hidden_password(password):
    hidden_word = ''
    for char in password:
        if char.isalpha():
            hidden_word += '-'
        else:
            hidden_word += char
    print(f"Ukryte hasło:\n{hidden_word}")

    consonants = set('bcdfghjklmnpqrstvwxyz')

    while '-' in hidden_word:
        guess = input("Podaj spółgłoskę: ").lower()

        if len(guess) != 1 or guess not in consonants:
            print("Podana wartość nie jest spółgłoską")
            continue

        found = False
        for i, letters in enumerate(password):
            if guess in letters:
                hidden_word = hidden_word[:i] + letters + hidden_word[i+1:]
                found = True

        if found:
            print(f"Zgadłeś! Litera {guess} znajduje się w haśle!")
        else:
            print(f"Niestety litera {guess} nie znajduje się w haśle!")

        print(f"Ukryte hasło:\n{hidden_word}")

    print("Gratulacje! Odgadłeś całe hasło!")
    return hidden_word


def load_from_json():
    word_and_category_list = []
    with open('hasla.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        for objects in data['kategorie_i_hasla']:
            category = objects['kategoria']
            word = objects['hasło']
            word_and_category = WordAndCategory(word, category)
            word_and_category_list.append(word_and_category)
    return word_and_category_list


def center_text(text):
    for char in text:
        char_len = len(char)
        return ' ' * char_len


def guess_full_password(players, word):
    clear_terminal()
    print("Wprowadź hasło lub naciśnij enter by kontynuować: ")
    full_guess = input().lower()
    active_player_index = 0
    while full_guess != word.lower():
        print("Niestety, nie zgadłeś! Kolej na następnego gracza")
        active_player_index = (active_player_index + 1) % len(players)
        player = players[active_player_index]
        print(f"Kolej na gracza: {player.name()}")
        print("Wprowadź hasło lub naciśnij enter aby kontynuować: ")
        full_guess = input().lower()
    name = players[active_player_index].name()
    print(f"Gratulacje! Hasło odgadnięte przez gracza {name}!")


def play_round(list_of_words_and_categ, players):
    random_instance = random.choice(list_of_words_and_categ)
    word = random_instance.word()
    category = random_instance.category()

    round_over = False
    active_player = 0

    hidden_word = ''
    for char in word:
        if char.isalpha():
            hidden_word += '-'
        else:
            hidden_word += char

    while not round_over:
        print(f"Kategoria: {category}\nUkryte hasło:\n{hidden_word}")

        player = players[active_player]
        print(f"Kolej na gracza {player.name()}")
        print("Kręcenie kołem fortuny...")
        time.sleep(0.2)

        prizes = [550, 350, 400, 1500, 'BANKRUT', 300, '500?',
                  'NIESPODZIANKA', 150, 200, 100, 400, 250, 450, 2500, 'STOP']
        surprise = ['Sprzęt AGD', 'Czajnik elektryczny', 'Toster',
                    'Skórzana galanteria', 'Wok', 'Zegarek Szwajcarski',
                    'Sprzet audio', 'Pobyt w spa']

        fortune_wheel(prizes)
        choice = random.choice(prizes)
        if choice == 'BANKRUT':
            player.points() == 0
            player = players[active_player + 1]
        elif choice == 'NIESPODZIANKA':
            random_surprise = random.choice(surprise)
            prizes.remove('NIESPODZIANKA')
            player.prizes().append(random_surprise)
            continue
        elif choice == 'STOP':
            player = players[active_player + 1]
            continue
        elif choice == '500?':
            while True:
                decision = input("Odkrywasz pole czy obstawiasz za 500 zl?\n"
                                    "1. Odkrywam\n"
                                    "2. Obstawiam\n"
                                    "Decyzja: ")
                if decision == 1:
                    random_choice = random.choice(['BANKRUT', 3000])
                    if random_choice == 'BANKRUT':
                        player.points() == 0
                        print("Niestety, wylosowałeś bankruta!")
                        break
                    elif random_choice == 3000:
                        player.add_points(3000)
                        print("Gratulacje, udało ci się zdobyć 3000 zł !")
                        break
                    else:
                        print("Nieprawidłowa wartość")
                        continue
        key = guess_full_password(players, word)
        keyboard.on_press_key('9', lambda event: key)
        # Reszta kodu logiki gry
        keyboard.unhook_all()


def inform_players(players):
    print("======Aktualny stan graczy======")
    for player in players:
        print(player.info())
    print("================================")
