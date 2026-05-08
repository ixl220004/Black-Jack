#This will be used to move my function into from the main game.

def calculate_hand(hand):
    total = 0
    aces = 0

    for card in hand:
        total += card["value"]

        if card["rank"] == "A":
            aces += 1

    # adjust aces from 11 → 1 if bust
    while total > 21 and aces:
        total -= 10
        aces -= 1

    return total