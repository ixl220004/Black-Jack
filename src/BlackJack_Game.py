import Blackjack

wallet = 100
current_bet = 0

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

def earnings(result):
    global wallet, current_bet

    if result == "win":
        wallet += current_bet
    elif result == "loss":
        wallet -= current_bet
    elif result == "push":
        pass


def Game():
    global current_bet
    while wallet > 0:
        current_bet = bets()
    
    while True:
        if input("play the game? y/n\n") == "y":
            Blackjack.deal()
            earnings()
            while input("play again? y/n") == "y":
                Blackjack.deal()
                earnings()
        else:
            return False


Game()