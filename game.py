import fortune_wheel
import time


def main():
    fortune_wheel.clear_terminal()
    players = fortune_wheel.introduction()
    time.sleep(3)
    words_and_categories = fortune_wheel.load_from_json()
    round_number = 1
    while round_number <= 3:
        fortune_wheel.clear_terminal()
        print(f"Runda numer {round_number} zaczyna się!")
        time.sleep(2)
        fortune_wheel.clear_terminal()

        round_over = fortune_wheel.play_round(words_and_categories, players)

        if round_over:
            print(f"Koniec rundy {round_number}.")
            fortune_wheel.end_inform_players(players)
            time.sleep(2)
            round_number += 1
    winner = fortune_wheel.winner(players)
    fortune_wheel.clear_terminal()
    fortune_wheel.pre_final(players)
    fortune_wheel.clear_terminal()
    print("======================= FINAŁ =======================")
    time.sleep(3)
    fortune_wheel.final_round(words_and_categories, winner)

    print("Dziękujemy za grę!")


if __name__ == '__main__':
    main()
    input("Naciśnij Enter, aby zamknąć program...")
