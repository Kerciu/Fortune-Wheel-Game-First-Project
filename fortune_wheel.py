import random
import time
import os
import json
from players import Player, WordAndCategory


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_fences():
    print('--------------')


def fortune_wheel(choices):
    picked_up_prize = random.choice(choices)
    copied_choices = choices.copy()
    random.shuffle(copied_choices)
    delay = 0.03
    for i, element in enumerate(2 * copied_choices):
        clear_terminal()
        if i == len(copied_choices) - 1:
            print(picked_up_prize)
        else:
            print(element)
        time.sleep(delay)
        delay += 0.01
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


def guess_full_password(players, word):
    print("Wybrałeś opcję odgadnięcia pełnego hasła!")
    print("Wprowadź hasło i naciśnij enter by kontynuować: ")
    full_guess = input().lower()

    correct_guess = False
    formated_word = word.lower()
    for player in players:
        if full_guess == formated_word:
            correct_guess = True
            name = player.nickname()
            print(f"Gratulacje, {name}! Odgadłeś/aś hasło: {word}!")
            return True
    if not correct_guess:
        print("Niestety, to nieprawidłowe hasło. Kolej na następnego gracza.")
        time.sleep(2)
        clear_terminal()
    return False


def update_hidden_word(word, hidden_word, guessed_letter):
    updated_hidden_word = ''
    for i, (letter, hidden_char) in enumerate(zip(word, hidden_word)):
        if letter == guessed_letter and guessed_letter not in 'aeiou':
            updated_hidden_word += guessed_letter
        else:
            updated_hidden_word += hidden_char if hidden_char != '-' else '-'
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


def check_final_input_letters(word, hidden_word, guessed_letter_list):
    update_hidden_word = list(hidden_word)

    for guessed_letter in guessed_letter_list:
        letter_found = False
        for i, letter in enumerate(word):
            if letter == guessed_letter:
                update_hidden_word[i] = guessed_letter
                letter_found = True
        if letter_found:
            return ''.join(update_hidden_word)
        else:
            return hidden_word


def check_guessed_vowel(word, hidden_word, guessed):
    if guessed in 'aeiouąęó' and guessed in word:
        print(f"Zgadłeś! Litera {guessed} znajduje się w haśle")
        for i, letter in enumerate(word):
            if letter == guessed:
                hidden_word = hidden_word[:i] + guessed + hidden_word[i + 1:]
        return True, hidden_word
    else:
        print("Ups! Nie udało się! Kolejka przechodzi na kolejnego gracza")
        return False, hidden_word


def remove_player_points(players):
    for player in players:
        if player.points() > 0:
            player.remove_points(player.points())


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
    break_continue = False
    active_player = 0
    guessed_consonants = set()
    guessed_vowels = set()
    guessed_letters = set()

    hidden_word = hide_word(word, guessed_letters)

    while not round_over:
        info = f"Kategoria: {category}\nUkryte hasło:\n{hidden_word}"
        print(info)
        inform_players(players)
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
        match choice:
            case int():
                print(f"Otrzymane punkty: {choice}")
            case 'BANKRUT':
                print("Niestety, jesteś BANKRUTEM")
                player.remove_points(player.points())
                active_player = (active_player + 1) % len(players)
                player = players[active_player]
                choice = 0
                continue
            case 'NIESPODZIANKA':
                rand_surprise = random.choice(surprise)
                prizes.remove('NIESPODZIANKA')
                player.prizes().append(rand_surprise)
                bonus = '\nDo tego zdobyłeś 50 punktów.'
                print(f'Wylosowana niespodzianka to.. {rand_surprise}' + bonus)
                choice = 50
            case 'STOP':
                active_player = (active_player + 1) % len(players)
                player = players[active_player]
                choice = 0
                continue
            case '500?':
                while True:
                    decision = input("Odkrywasz pole czy "
                                     "obstawiasz za 500 zl?\n"
                                     "1. Odkrywam\n"
                                     "2. Obstawiam\n"
                                     "Decyzja: ")
                    if decision == '1':
                        random_choice = random.choice(['BANKRUT', 3000])
                        if random_choice == 'BANKRUT':
                            clear_terminal()
                            print("Niestety, jesteś BANKRUTEM\n")
                            print("Kolejka przechodzi na następnego gracza...")
                            player.remove_points(player.points())
                            choice = 0
                            active_player = (active_player + 1) % len(players)
                            player = players[active_player]
                            break_continue = True
                            time.sleep(2)
                            break
                        else:
                            player.add_points(3000)
                            print("Gratulacje, udało ci się zdobyć 3000 zł !")
                            active_player = (active_player + 1) % len(players)
                            player = players[active_player]
                            choice = 3000
                            time.sleep(2)
                            break
                    elif decision == '2':
                        player.add_points(500)
                        choice = 500
                        print("Dodano 500 zl do twojego konta")
                        time.sleep(2)
                        break
                    else:
                        print("Nieprawidłowa wartość")
                        continue
                if break_continue:
                    continue

        while '-' in hidden_word:
            consonants = set('qwrtypsdfghjklzxcvbnmśłżźćń')
            print(info)
            input_str = f"Kolej gracza {player.nickname()}, podaj spółgłoskę: "
            guess = input(input_str).lower()
            if len(guess) == 1 and guess:
                next_play = "Kolejka przechodzi na następnego gracza"
                if guess in guessed_consonants:
                    print("Ta litera spółgłoska już odgadnięta. " + next_play)
                    active_player = (active_player + 1) % len(players)
                    player = players[active_player]
                    time.sleep(2)
                    clear_terminal()
                    continue
                if guess not in consonants:
                    print("Ta litera nie jest samogłoską! " + next_play)
                    active_player = (active_player + 1) % len(players)
                    player = players[active_player]
                    time.sleep(2)
                    clear_terminal()
                    continue

                guessed_consonants.add(guess)
                guessed_letters.add(guess)

                x, points = check_guessed_letter(word, hidden_word,
                                                 guess, choice)
                if points > 0:
                    player.add_points(points)
                    updated_hidden_word = update_hidden_word(word, hidden_word,
                                                             guess)
                    hidden_word = updated_hidden_word
                    print(f"Zaktualizowane hasło: {hidden_word}")
                    break
                else:
                    active_player = (active_player + 1) % len(players)
                    player = players[active_player]
                    break
            else:
                print("Podana wartość nie jest spółgłoską, spróbuj ponownie.")
                continue

        while True:
            time.sleep(3)
            clear_terminal()
            inform_players(players)
            name = player.nickname()
            choice_input = input(f"Co chcesz teraz zrobić, graczu {name}?\n"
                                 "1. Zakręć ponownie kołem\n"
                                 "2. Kup samogłoskę\n"
                                 "3. Spróbuj odgadnąć hasło\n"
                                 "Wybierz opcję: ")
            if choice_input == '1':
                clear_terminal()
                print("Wybrałeś opcję ponownego zakręcenia kołem...")
                time.sleep(2)
                break
            elif choice_input == '2':
                while True:
                    vowel_price = 200
                    if player.points() < vowel_price:
                        print("Niewystarczająca ilość "
                              "punktów do zakupu samogłoski.")
                        break
                    else:
                        vowels = set('aeiou')
                        pricestr = f"Cena samogłoski to {vowel_price} punktów."
                        print(f"Masz {player.points()} punktów. " + pricestr)
                        print("Wybierz samogłoskę do kupienia: ")
                        vowel = input().lower()
                        if vowel not in vowels:
                            print("Wybór musi być samogłoską!")
                            continue
                        if vowel in guessed_vowels:
                            print("Ta samogłoska została już odgadnięta.")
                            break

                        guessed_vowels.add(vowel)
                        guessed_letters.add(vowel)

                        correct_vowel = check_guessed_vowel(word, hidden_word,
                                                            vowel)
                        if correct_vowel[0]:
                            hidden_word = correct_vowel[1]
                            if hidden_word:
                                player.remove_points(vowel_price)
                                print(f"Zakupiłeś samogłoskę '{vowel}'."
                                      f" Nowe ukryte hasło:\n{hidden_word}")
                                break
                            else:
                                print("Wybrana samogłoska nie znajduje się "
                                      "w haśle. Kolej na następnego gracza")
                                lenght = len(players)
                                active_player = (active_player + 1) % lenght
                                player = players[active_player]
                                break
                        else:
                            print("Wybrana samogłoska nie "
                                  "znajduje się w haśle.")
                            active_player = (active_player + 1) % lenght
                            player = players[active_player]
                            break
            elif choice_input == '3':
                clear_terminal()
                info = f"Kategoria: {category}\nUkryte hasło:\n{hidden_word}"
                print(info)
                time.sleep(1)
                guess = guess_full_password(players, word)
                if guess:
                    time.sleep(2)
                    player.add_perm_points(player.points())
                    remove_player_points(players)
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


def pre_final(players):
    winner_player = winner(players)
    losers = [player for player in players if player != winner_player]

    clear_terminal()
    losers_name = [loser.nickname() for loser in losers]
    print("Dziękujemy wszystkim graczom za grę:")
    for name in losers_name:
        print(name)
    time.sleep(3)
    print("Przechodzimy teraz do finału...")
    time.sleep(3)


def reveal_letters(hidden_word, actual_word):
    revealed_word = list(hidden_word)
    alpha = 'abcdfghijkmopquvwxyz'
    reveal_idx = set()
    time_limit = 10
    start_time = time.time()

    while len(reveal_idx) < 5 and time.time() - start_time < time_limit:
        guess_index = random.randint(0, len(actual_word) - 1)
        if actual_word[guess_index] in alpha and guess_index not in reveal_idx:
            revealed_word[guess_index] = actual_word[guess_index]
            reveal_idx.add(guess_index)
            print(''.join(revealed_word), end='\r')
            time.sleep(1)

    return ''.join(revealed_word)


def countdown():
    for i in range(10, -1, -1):
        if i == 1:
            seconds = 'sekunda'
        elif i in (2, 3, 4):
            seconds = 'sekundy'
        else:
            seconds = 'sekund'

        print(f'Pozostało: {i} {seconds}', end='\r')
        time.sleep(1)


def guess_final_password(player, word, update_word):
    hidden_word = update_word

    reveal_letters(hidden_word, word)
    print('\n')
    countdown()
    print('\n')
    full_guess = input("Podaj hasło: ").lower()

    correct_guess = False
    if full_guess == word.lower():
        correct_guess = True
        clear_terminal()
        print(f"Gratulacje, {player.nickname()}! Odgadłeś/aś hasło: {word}!")
        time.sleep(2)
        print(f"Twoja wygrana: {player.perm_points()} zł i Polonez Caro!")
        time.sleep(2)
        print("Szukaj go w swoim garażu :)\nDo zobaczenia wkrótce!!!")
        time.sleep(5)
    if not correct_guess:
        clear_terminal()
        print("Niestety, to nieprawidłowe hasło, ale i tak...\n")
        time.sleep(2)
        print(f"Wygrałeś {player.perm_points()} zł !!!")
        time.sleep(2)
        print("Do zobaczenia wkrótce!!!")
        time.sleep(5)


def final_round(list_of_words_and_categ, winner):
    random_instance = random.choice(list_of_words_and_categ)
    word = random_instance.word()
    category = random_instance.category()
    guessed_letters = set()
    list_of_letters = ['r', 's', 't', 'l', 'n', 'e']
    hidden_word = hide_word(word, guessed_letters)
    name = winner.nickname()
    print(f"Zaczynamy rundę finałową. Finalistą jest gracz {name}.\n")
    time.sleep(3)
    print(f"Hasło finałowe: {hidden_word}\nKategora: {category}.")
    time.sleep(3)
    print("Podaję zestaw liter: R, S, T, L, N, E")
    time.sleep(3)
    clear_terminal()
    update_word = check_final_input_letters(word, hidden_word, list_of_letters)
    print(f"Hasło finałowe: {update_word}\nKategora: {category}.")
    guess_final_password(winner, word, update_word)


def inform_players(players):
    print("======Aktualny stan graczy======")
    for player in players:
        print(player.info())
    print("================================")


def end_inform_players(players):
    print("====== Stan graczy na koniec rundy ======")
    for player in players:
        print(player.end_info())
    print("=========================================")
