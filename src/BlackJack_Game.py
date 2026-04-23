import Blackjack

wallet = 100


def bets():
    while True:
        bet = input("how much will you bet?\n"
        f"total: ${wallet}\nbet?:")
        if not bet.isdigit():
            print("enter a valid number")
            continue

        bet = int(bet)

        if bet > wallet:
            print("insufficient funds")
        else:
            return bet

def Game():
    bets()
    
    
    while True:
        if input("play the game? y/n\n") == "y":
            Blackjack.deal()
            while input("play again? y/n") == "y":
                Blackjack.deal()


Game()