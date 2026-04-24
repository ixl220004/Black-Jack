import Blackjack

wallet = 100
current_bet = 0


def bets():
    while True:
        bet = input(
            f"How much will you bet?\n"
            f"Total: ${wallet}\nBet?: "
        )

        if not bet.isdigit():
            print("Enter a valid number")
            continue

        bet = int(bet)

        if bet <= 0:
            print("Bet must be greater than 0")
        elif bet > wallet:
            print("Insufficient funds")
        else:
            return bet


def earnings(result):
    global wallet, current_bet

    if result == "win":
        wallet += current_bet
        print(f"You won ${current_bet}")

    elif result == "loss":
        wallet -= current_bet
        print(f"You lost ${current_bet}")

    elif result == "push":
        print("Push (no money change)")
    elif result == "blackjack_win":
        wallet += current_bet *1.5

    print(f"Wallet: ${wallet}")


def Game():
    global current_bet

    while wallet > 0:
        if input("Play the game? y/n: ") != "y":
            break

        current_bet = bets()

        result = Blackjack.deal()   # ✅ capture result
        earnings(result)            # ✅ pass result

    print("Game over.")


Game()