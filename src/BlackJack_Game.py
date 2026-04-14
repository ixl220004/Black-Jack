import Blackjack

def Game():
    while True:
        if input("play the game? y/n") == "y":
            Blackjack.deal()
            while input("play again? y/n") == "y":
                Blackjack.deal()


Game()