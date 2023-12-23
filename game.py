import fortune_wheel
import time


def main():
    fortune_wheel.clear_terminal()
    players = fortune_wheel.introduction()
    words_and_categories = fortune_wheel.load_from_json()

    round_number = 1
    while round_number <= 3:
        fortune_wheel.clear_terminal()
        print(f"Runda numer {round_number} zaczyna się!")
        time.sleep(2)

        round_over = fortune_wheel.play_round(words_and_categories, players)
        fortune_wheel.inform_players(players)

        if round_over:
            print(f"Koniec rundy {round_number}.")
            time.sleep(2)
            round_number += 1

    print("Dziękujemy za grę!")


if __name__ == '__main__':
    main()
