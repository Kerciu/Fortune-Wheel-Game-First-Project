import random
import time
import os
from players import Player


def clear_terminal():
    # Czyszczenie terminala w zależności od systemu operacyjnego
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
    print(f"Witam was: {player_one}, {player_two} i {player_three}\nZaczynamy grę!")

    player1 = Player(player_one)
    player2 = Player(player_two)
    player3 = Player(player_three)

    return player1, player2, player3

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
            if guess == any(letters):
                hidden_word = hidden_word[:i] + letters + hidden_word[i+1:]
                found = True

        if found:
            print(f"Zgadłeś! Litera {guess} znajduje się w haśle!")
        else:
            print(f"Niestety litera {guess} nie znajduje się w haśle!") 
    
        print(f"Ukryte hasło:\n{hidden_word}")

    print("Gratulacje! Odgadłeś całe hasło!")
    return hidden_word


password = ['Kazakhstan', 'Poland', 'Ukraine', 'Republic of Korea']
chosen_password = random.choices(password)
# prizes = [100, 200, 500, 1000, 1500, 2000, 2500, 3000]
# print(fortune_wheel(prizes))
