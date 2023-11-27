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

# prizes = [100, 200, 500, 1000, 1500, 2000, 2500, 3000]
# print(fortune_wheel(prizes))