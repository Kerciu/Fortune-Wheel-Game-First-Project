import random
import time
import os
import json
import sys
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
    delay = 0.03
    for i, element in enumerate(2 * copied_choices):
        clear_terminal()
        if i == len(copied_choices) - 1:
            print(picked_up_prize)
        else:
            print(element)
        time.sleep(delay)
        # Zwiększanie opóźnienie wraz z kolejnym wyświetlanym elementem
        delay += 0.01

    # Opóźnienie przed wyświetleniem wyniku i wyczyszczenie terminala
    time.sleep(1)
    clear_terminal()
    return picked_up_prize


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

    correct_guess = False
    for player in players:
        if full_guess == word.lower():
            correct_guess = True
            print(f"Gratulacje, {player.nickname()}! Odgadłeś/aś hasło: {word}!")
            return True
    if not correct_guess:
        print("Niestety, to nieprawidłowe hasło. Kolej na następnego gracza.")
        time.sleep(2)  # Dodatkowe opóźnienie dla czytelności komunikatu
        clear_terminal()
    return False


def check_guessed_letter(word, hidden_word, guessed_letter, points):
    if guessed_letter in word:
        print(f"Zgadłeś! Litera {guessed_letter} znajduje się w haśle")
        for i, letter in enumerate(word):
            if letter == guessed_letter:
                hidden_word = hidden_word[:i] + guessed_letter + hidden_word[i + 1:]
        print(f"Zdobyłeś {points} punktów!")
        return hidden_word, points
    else:
        print("Ups! Nie udało się! Kolejka przechodzi na kolejnego gracza")
        return hidden_word, 0


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
        info = f"Kategoria: {category}\nUkryte hasło:\n{hidden_word}"
        print(info)
        time.sleep(2)
        player = players[active_player]
        print(f"Kolej na gracza {player.nickname()}")
        time.sleep(2)
        print("Kręcenie kołem fortuny...")
        time.sleep(2)

        prizes = [550, 350, 400, 1500, 'BANKRUT', 300, '500?',
                  'NIESPODZIANKA', 150, 200, 100, 400, 250, 450, 2500, 'STOP']
        surprise = ['Sprzęt AGD', 'Czajnik elektryczny', 'Toster',
                    'Skórzana galanteria', 'Wok', 'Zegarek Szwajcarski',
                    'Sprzet audio', 'Pobyt w spa']

        choice = fortune_wheel(prizes)
        print(f'Wylosowano: {choice}')
        time.sleep(1)
        if isinstance(choice, int):
            print(f"Otrzymane punkty: {choice}")
            player.add_points(choice)
        elif choice == 'BANKRUT':
            print("Niestety, jesteś BANKRUTEM")
            player.remove_points(player.points())
            player = players[(active_player + 1) % len(players)]
            continue
        elif choice == 'NIESPODZIANKA':
            random_surprise = random.choice(surprise)
            prizes.remove('NIESPODZIANKA')
            player.prizes().append(random_surprise)
        elif choice == 'STOP':
            player = active_player = (active_player + 1) % len(players)
            continue
        elif choice == '500?':
            while True:
                decision = input("Odkrywasz pole czy obstawiasz za 500 zl?\n"
                            "1. Odkrywam\n"
                            "2. Obstawiam\n"
                            "Decyzja: ")
                if decision == '1':
                    random_choice = random.choice(['BANKRUT', 3000])
                    if random_choice == 'BANKRUT':
                        print("Niestety, jesteś BANKRUTEM\n")
                        print("Kolejka przechodzi na następnego gracza...")
                        player.remove_points(player.points())
                        player = players[(active_player + 1) % len(players)]
                        break
                    else:
                        player.add_points(3000)
                        print("Gratulacje, udało ci się zdobyć 3000 zł !")
                        break
                elif decision == '2':
                    player.add_points(500)
                    print("Dodano 500 zl do twojego konta")
                    break
                else:
                    print("Nieprawidłowa wartość")
                    continue
        # Reszta kodu logiki gry

        consonants = set('bcdfghjklmnpqrstvwxyz')
        while '-' in hidden_word:
            print(info)
            guess = input(f"Kolej gracza {player.nickname()}, podaj spółgłoskę: ").lower()
            if len(guess) != 1 or guess not in consonants:
                print("Podana wartość nie jest spółgłoską")
                continue

            hidden_word, points = check_guessed_letter(word, hidden_word, guess, choice)
            if points > 0:
                player.add_points(points)
                break
            else:
                player = player[(active_player + 1) % len(players)]
                break

        while True:
            choice_input = input(f"Co chcesz teraz zrobić, graczu {player.nickname()}?\n"
                    "1. Zakręć ponownie kołem\n"
                    "2. Kup samogłoskę\n"
                    "3. Spróbuj odgadnąć hasło\n"
                    "Wybierz opcję: ")
            if choice_input == '1':
                print("Koło się kręci ponownie...")
                time.sleep(2)
                break
            elif choice_input == '2':
                while True:
                    price_for_vowel = 200
                    if player.points() < price_for_vowel:
                        print("Niewystarczająca ilość punktów do zakupu samogłoski.")
                        break
                    else:
                        vowels = set('aeiou')
                        print(f"Masz {player.points()} punktów. Cena samogłoski to {price_for_vowel} punktów.")
                        print("Wybierz samogłoskę do kupienia: ")
                        vowel = input().lower()
                        if vowel not in vowels:
                            print("Wybór musi być samogłoską!")
                            continue
                        if vowel in word:
                            hidden_word, points = check_guessed_letter(word, hidden_word, vowel, prizes)
                            if points == 0:
                                print("Wybrana samogłoska nie znajduje się w haśle.")
                                break
                            else:
                                player.remove_points(price_for_vowel)
                                print(f"Zakupiłeś samogłoskę '{vowel}'. Nowe ukryte hasło:\n{hidden_word}")
                                break
            elif choice_input == '3':
                print("Wybrałeś opcję odgadnięcia pełnego hasła!")
                guess = guess_full_password(players, word)
                if guess:
                    time.sleep(2)
                    for player in players:
                        player.add_perm_points(player.points())
                        round_over = True
                else:
                    player = players[(active_player + 1) % len(players)]
            else:
                print("Niepoprawne wejście, wybierz 1, 2 lub 3")
                continue


def inform_players(players):
    terminal_height = 24
    print('\n' * terminal_height - 3)
    print("======Aktualny stan graczy======")
    for player in players:
        print(player.info())
    print("================================")
    print('\033[F' * len((player) + 4))
    sys.stdout.flush()
