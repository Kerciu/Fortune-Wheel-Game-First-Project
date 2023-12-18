import fortune_wheel
from players import Player
import time


def main():
    fortune_wheel.introduction()
    time.sleep(3)
    fortune_wheel.clear_terminal()
    fortune_wheel.inform_players()

    # players = fortune_wheel.introduction()
    # words_and_categories = fortune_wheel.load_from_json()
    # for round in (1, 4):
    #     print(f"Runda nr. {round}")
    #     fortune_wheel.play_round(words_and_categories, players)
    # print("Runda Finałowa!")
    # fortune_wheel.final_round(words_and_categories, players)
    # end_game(players)


if __name__ == '__main__':
    main()
