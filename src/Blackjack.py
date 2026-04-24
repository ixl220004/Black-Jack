
import random
import time




with open("deck.txt", 'r') as f:
  deck = [line.strip() for line in f]

hand = []
hand_value = []
dealer_hand = []
discard_pile = []

#counts the card of the hand put into the parameter
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


def discard(selected_hand):
   discard_pile.extend(selected_hand)
   selected_hand.clear()
    



def shuffle(deck):
   if len(deck) <10:
      deck.extend(discard_pile)
      discard_pile.clear()
      print("SHUFFLE")
      

def deck_check():
   time.sleep(1)
   discard(hand)
   discard(dealer_hand)
   


#draws a random card and puts it into the parameter.
#removes the card from the deck list aswell.
# if repeated within the script, it will just draw cards until the deck is empty.
# SHUFFLE FUNCTION NEEDED FOR LONG PLAY
def draw_card(selected_Hand):
    drawn_card = random.choice(deck)
    deck.remove(drawn_card)
    selected_Hand.append(drawn_card)
    

    if selected_Hand == hand:
        print(f"Your hand: {selected_Hand}")
        print(f"Your hand value: {calculate_hand(selected_Hand)}")

    if selected_Hand == dealer_hand:
       print(f"Dealer's hand: {dealer_hand}")
       print(f"Dealer's value: {calculate_hand(dealer_hand)}")

#basic game loop, player is given choice to draw cards or 
def player_choice(): 
  draw_card(hand)
  while True:
    choice = input("draw card y/n?\n")
    if choice == "y":
        draw_card(hand)
        if calculate_hand(hand) > 21:
           print("BUST!!!!")
           return True
    else:
      return False

#main game loop, first dealer draws card, then player, runs 
#the player's choice to see if the player draws or stands.
#then the dealer draws until 17, and checks if either player or dealer wins.
def deal():
   

   draw_card(dealer_hand)

   player_bust = player_choice()

  


   if player_bust == False:
        print("dealer_turn")
        

        
        while calculate_hand(dealer_hand) < 17:
            draw_card(dealer_hand)
            time.sleep(1)

        # check bust AFTER finishing drawing
        if calculate_hand(dealer_hand) > 21:
            print("dealer busts!!!")
            dealer_bust = True
        else:
            dealer_bust = False


        
   result = None

   if player_bust:
      result = "loss"
      print("YOU LOSE (player bust)")

   elif dealer_bust:
      result = "win"
      print("YOU WIN (dealer bust)")

   elif calculate_hand(hand) > calculate_hand(dealer_hand):
      result = "win"
      print("YOU WIN!!!")

   elif calculate_hand(hand) < calculate_hand(dealer_hand):
      result = "loss"
      print("YOU LOSE!!!")
   elif calculate_hand(hand) == 21:
      

   else:
      result = "push"
      print("TIE!!!")

   deck_check()
   return result


   

    



      
   


if __name__ == "__main__":
    deal()
