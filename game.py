import fortune_wheel


def main():
    fortune_wheel.clear_terminal()
    players = fortune_wheel.introduction()
    words_and_categories = fortune_wheel.load_from_json()

    while True:
        fortune_wheel.play_round(words_and_categories, players)
        fortune_wheel.inform_players(players)
        restart = input("Czy chcesz zagrać jeszcze raz? (tak/nie): ").lower()
        if restart != 'tak':
            break

    print("Dziękujemy za grę!")


if __name__ == '__main__':
    main()
