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


def guess_full_password(event, players, word):
    clear_terminal()
    if event.name == '9':
        print("Wprowadź hasło lub naciśnij enter by kontynuować: ")
        full_guess = input().lower()
        for player in players:
            if full_guess in word.lower():
                print(f"Gratulację graczu {player.name()}. Odgadłeś hasło.")
                return
        print("Niestety, to nieprawidłowe hasło. Kolej na następnego gracza.")
        time.sleep(2)  # Dodatkowe opóźnienie dla czytelności komunikatu
        clear_terminal()
        return


def check_guessed_letter(word, hidden_word, guessed_letter, prizes):
    if guessed_letter in word:
        print(f"Zgadłeś! Litera {guessed_letter} znajduje się w haśle")
        for i, letter in enumerate(word):
            if letter == guessed_letter:
                hidden_word = hidden_word[:1] + guessed_letter + hidden_word[i + 1:]
        points = random.choice(prizes)
        print(f"Zdobyłeś {points} punktów!")
        return hidden_word, points
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

        choice = fortune_wheel(prizes)
        choice
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
        print("Odgadnij hasło! Naciśnij '9' i wprowadź hasło:")
        key = guess_full_password(players, word)
        keyboard.on_press_key('9', lambda event: key)
        # Reszta kodu logiki gry

        consonants = set('bcdfghjklmnpqrstvwxyz')
        while '-' in hidden_word:
            guess = input("Podaj spółgłoskę: ").lower()
            if len(guess) != 1 or guess not in consonants:
                print("Podana wartość nie jest spółgłoską")
                continue

            hidden_word, points = check_guessed_letter(word, hidden_word, guess, prizes)
            if points > 0:
                print(f"Zgadłeś! Litera {guess} znajduje się w haśle!")
            else:
                print(f"Niestety litera {guess} nie znajduje się w haśle!")
                player = players[active_player + 1]
                break
        while True:
            choice_input = input("Co chcesz teraz zrobić?\n"
                    "1. Zakręć ponownie kołem\n"
                    "2. Kup samogłoskę\n"
                    "3. Spróbuj odgadnąć hasło\n"
                    "Wybierz opcję: ")
            if choice_input == 1:
                print("Koło się kręci ponownie...")
                time.sleep(1)
                break
            elif choice_input == 2:
                #Logika kupowania samogłoski
                #Aktualizacja stanu gracza
                break
            elif choice_input == 3:
                #Logika odgadnięcia hasła
                #Zakończenie rundy, wygrana, punkty, itp.
                round_over=True
                break
            else:
                print("Niepoprawne wejście, wybierz 1, 2 lub 3")
                continue

        keyboard.unhook_all()
        active_player = (active_player + 1) % len(players)


def inform_players(players):
    print("======Aktualny stan graczy======")
    for player in players:
        print(player.info())
    print("================================")
