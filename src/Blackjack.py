
import random
import time




with open("deck.txt", 'r') as f:
  deck = [line.strip() for line in f]

hand = []
hand_value = []

def calculate_hand(hand):
    total = 0
    aces = 0

    for card in hand:
        value = card.split()[0]

        if value in ["Jack", "Queen", "King"]:
            total += 10
        elif value == "Ace":
            total += 11
            aces += 1
        else:
            total += int(value)

    while total > 21 and aces > 0:
        total -= 10
        aces -= 1

    return total

def draw_card():
    drawn_card = random.choice(deck)
    hand.append(drawn_card)

    print(f"Your hand: {hand}")
    print(f"Your hand value: {calculate_hand(hand)}")


def player_choice(): 
  draw_card()
  while True:
    choice = input("draw card y/n?\n")
    if choice == "y":
        draw_card()
        if calculate_hand(hand) > 21:
           print("BUST!!!!")
           return True
    else:
      return False

    

def deal():
   dealer_hand = []

   draw_card = random.choice(deck)
   dealer_hand.append(draw_card)
   
   print(f"Dealer's hand:{dealer_hand}")
   print(f"Dealer's value: {calculate_hand(dealer_hand)}")

   player_bust = player_choice()


   if player_bust == True:
      print("YOU LOSE (player bust)")
      return



   if player_bust == False:
        print("dealer_turn")
        

        
        while calculate_hand(dealer_hand) < 17:
            draw_card2 = random.choice(deck)
            dealer_hand.append(draw_card2)

            print(f"Dealer's hand: {dealer_hand}")
            print(f"Dealer's value: {calculate_hand(dealer_hand)}")
            time.sleep(1)

        # check bust AFTER finishing drawing
        if calculate_hand(dealer_hand) > 21:
            print("dealer busts!!!")
            dealer_bust = True
        else:
            dealer_bust = False
        
   if player_bust:
    print("YOU LOSE (player bust)")
   elif dealer_bust:
    print("YOU WIN (dealer bust)")
   elif calculate_hand(hand) > calculate_hand(dealer_hand):
    print("YOU WIN!!!")
   elif calculate_hand(hand) < calculate_hand(dealer_hand):
    print("YOU LOSE!!!")
   else:
    print("TIE!!!")

      
   



deal()