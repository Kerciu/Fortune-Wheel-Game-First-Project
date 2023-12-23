import random
import time
import os
import json
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
    print("Wybrałeś opcję odgadnięcia pełnego hasła!")
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


def update_hidden_word(word, hidden_word, guessed_letter):
    updated_hidden_word = ''
    for i, letter in enumerate(word):
        if letter == guessed_letter and guessed_letter not in 'aeiou':
            updated_hidden_word += guessed_letter
        else:
            updated_hidden_word += hidden_word[i]
    return updated_hidden_word


def check_guessed_letter(word, hidden_word, guessed_letter, points):
    update_hidden_word = list(hidden_word)
    letter_found = False

    for i, letter in enumerate(word):
        if letter == guessed_letter:
            update_hidden_word[i] = guessed_letter
            letter_found = True

    if letter_found:
        print(f"Zgadłeś! Litera {guessed_letter} znajduje się w haśle")
        joined_hidden_word = ''.join(update_hidden_word)
        print(f"Zdobyłeś {points} punktów!")
        return joined_hidden_word, points
    else:
        print("Ups! Nie udało się! Kolejka przechodzi na kolejnego gracza")
        return hidden_word, 0
    # if guessed_letter in word:
    #     print(f"Zgadłeś! Litera {guessed_letter} znajduje się w haśle")
    #     for i, letter in enumerate(word):
    #         if letter == guessed_letter:
    #             partly_hidden_word = hidden_word[:i] + guessed_letter + hidden_word[i + 1:]
    #     print(f"Zdobyłeś {points} punktów!")
    #     return partly_hidden_word, points
    # else:
    #     print("Ups! Nie udało się! Kolejka przechodzi na kolejnego gracza")
    #     return hidden_word, 0


def check_guessed_vowel(word, hidden_word, guessed_vowel):
    if guessed_vowel in 'aeiou' and guessed_vowel in word:
        print(f"Zgadłeś! Litera {guessed_vowel} znajduje się w haśle")
        for i, letter in enumerate(word):
            if letter == guessed_vowel:
                hidden_word = hidden_word[:i] + guessed_vowel + hidden_word[i + 1:]
        return True, hidden_word
    else:
        print("Ups! Nie udało się! Kolejka przechodzi na kolejnego gracza")
        return False, hidden_word


def hide_word(word, guessed_letters):
    hidden_word = ''
    for char in word:
        if char.isalpha() and char.lower() not in guessed_letters:
            hidden_word += '-'
        else:
            hidden_word += char
    return hidden_word


def play_round(list_of_words_and_categ, players):
    random_instance = random.choice(list_of_words_and_categ)
    word = random_instance.word().lower()
    category = random_instance.category()

    round_over = False
    active_player = 0
    guessed_consonants = set()
    guessed_vowels = set()
    guessed_letters = set()

    hidden_word = hide_word(word, guessed_letters)

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
            active_player = (active_player + 1) % len(players)
            player = players[active_player]
            continue
        elif choice == 'NIESPODZIANKA':
            random_surprise = random.choice(surprise)
            prizes.remove('NIESPODZIANKA')
            player.prizes().append(random_surprise)
            print(f'Wylosowana niespodzianka to... {random_surprise}')
            choice = 0
        elif choice == 'STOP':
            active_player = (active_player + 1) % len(players)
            player = players[active_player]
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
                        active_player = (active_player + 1) % len(players)
                        player = players[active_player]
                        choice = 0
                        break
                    else:
                        player.add_points(3000)
                        print("Gratulacje, udało ci się zdobyć 3000 zł !")
                        active_player = (active_player + 1) % len(players)
                        player = players[active_player]
                        choice = 3000
                        break
                elif decision == '2':
                    player.add_points(500)
                    choice = 500
                    print("Dodano 500 zl do twojego konta")
                    break
                else:
                    print("Nieprawidłowa wartość")
                    continue
        # Reszta kodu logiki gry
        while '-' in hidden_word:
            print(info)
            guess = input(f"Kolej gracza {player.nickname()}, podaj spółgłoskę: ").lower()
            if len(guess) == 1 and guess:
                if guess in guessed_consonants:
                    print("Ta litera spółgłoska już odgadnięta. Kolejka przechodzi na następnego gracza")
                    active_player = (active_player + 1) % len(players)
                    player = players[active_player]
                    continue

                guessed_consonants.add(guess)
                guessed_letters.add(guess)

                partly_hidden_word, points = check_guessed_letter(word, hidden_word, guess, choice)
                if points > 0:
                    hidden_word = partly_hidden_word
                    player.add_points(points)
                    break
                else:
                    hidden_word = hidden_word
                    active_player = (active_player + 1) % len(players)
                    player = players[active_player]
                    break
            else:
                print("Podana wartość nie jest spółgłoską, spróbuj ponownie.")
                continue
        hidden_word = update_hidden_word(word, hidden_word, guess)
        print(f"Zaktualizowane hasło: {hidden_word}")

        while True:
            time.sleep(3)
            clear_terminal()
            print(info)
            choice_input = input(f"Co chcesz teraz zrobić, graczu {player.nickname()}?\n"
                    "1. Zakręć ponownie kołem\n"
                    "2. Kup samogłoskę\n"
                    "3. Spróbuj odgadnąć hasło\n"
                    "Wybierz opcję: ")
            inform_players(players)
            if choice_input == '1':
                print("Wybrałeś opcję ponownego zakręcenia kołem...")
                time.sleep(1)
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
                        if vowel in guessed_vowels:
                            print("Ta samogłoska została już odgadnięta.")
                            continue

                        guessed_vowels.add(vowel)
                        guessed_letters.add(vowel)

                        correct_vowel = check_guessed_vowel(word, hidden_word, vowel)
                        if correct_vowel[0]:
                            hidden_word = check_guessed_vowel(word, hidden_word, vowel)[1]
                            if hidden_word:
                                player.remove_points(price_for_vowel)
                                print(f"Zakupiłeś samogłoskę '{vowel}'. Nowe ukryte hasło:\n{hidden_word}")
                            else:
                                print("Wybrana samogłoska nie znajduje się w haśle.")
                                break
                        else:
                            print("Wybrana samogłoska nie znajduje się w haśle.")
                            break
            elif choice_input == '3':
                info = f"Kategoria: {category}\nUkryte hasło:\n{hidden_word}"
                print(info)
                guess = guess_full_password(players, word)
                if guess:
                    time.sleep(2)
                    player.add_perm_points(player.points())
                    round_over = True
                    return True
                else:
                    active_player = (active_player + 1) % len(players)
                    player = players[active_player]
            else:
                print("Niepoprawne wejście, wybierz 1, 2 lub 3")
                continue
    return False


def winner(players):
    return max(players, key=lambda player: player.perm_points())


def final_round(list_of_words_and_categ, winner):
    random_instance = random.choice(list_of_words_and_categ)
    word = random_instance.word()
    category = random_instance.category()
    pass



def inform_players(players):
    print("======Aktualny stan graczy======")
    for player in players:
        print(player.info())
    print("================================")
