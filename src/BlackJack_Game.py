import pygame
import sys
import random
import BlackJack_functions


pygame.init()



class button:
    def __init__(self, x, y, width, height, text, color=(0, 200, 0)):
        self.rect = pygame.Rect(x,y,width,height)
        self.text = text
        self.color = color
        
    def draw(self, screen, font, color=None):
        draw_color = color if color else self.color
        pygame.draw.rect(screen, draw_color, self.rect)

        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    
    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)





#screen size
x, y = 800, 600
screen = pygame.display.set_mode((x,y))
pygame.display.set_caption("blackjack")

background = pygame.image.load("table.png")
background = pygame.transform.scale(background, (x, y))

#buttons and UI
hit_button = button(100, 350, 120, 50, "Hit")
stand_button = button(250, 350, 120, 50, "Stand")
play_button = button(300, 200, 200, 60, "play")
quit_button = button(300, 300, 200, 60, "Quit")
play_again_button = button(250, 250, 200, 60, "Play Again",)
quit_end_button = button(250, 330, 200, 60, "Quit",)
bet_5_button = button(150, 320, 120, 50, "Add $5")
bet_10_button = button(330, 320, 120, 50, "Add $10")
bet_20_button = button(510, 320, 120, 50, "Add $20")
bet_play_button = button(290, 420, 200, 60, "Play")


font = pygame.font.SysFont("arial",36)

#functions
def draw_text(text, x, y, font, color=(255, 255, 255)):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x,y))

def draw_hand(hand, area_rect, hide_first_card = False):
    x = area_rect.x + 10
    y = area_rect.y +20

    for i, card in enumerate(hand):

        card_rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        pygame.draw.rect(screen, (255, 255, 255), card_rect)
        pygame.draw.rect(screen, (0, 0, 0), card_rect, 2)

        if hide_first_card and i ==0:
            draw_text("?", x + 30, y+50, font, (0, 0, 0))
        else:
            card_text = f"{card['rank']}{card['suit']}"
            draw_text(card_text, x + 10, y + 45, font, (0,0,0))
        
        x += CARD_SPACING

def draw_card(hand):
    global deck, discard_pile

    if len(deck) == 0:
        if len(discard_pile) == 0:
            raise Exception("NO CARDS LEFT ANYWHERE")
        deck.extend(discard_pile)
        discard_pile.clear()
        random.shuffle(deck)
        print("RESHUFFLE")

    card = deck.pop()
    hand.append(card)

def calculate_hand(hand):
    total = 0
    aces = 0

    for card in hand:
        total += card["value"]
        if card["rank"] == "A":
            aces += 1

    while total > 21 and aces:
        total -= 10
        aces -= 1

    return total

def is_blackjack(hand):
    return len(hand) == 2 and calculate_hand(hand) == 21

def resolve_round(player, dealer):
    player_total = calculate_hand(player)
    dealer_total = calculate_hand(dealer)

    if player_total > 21:
        return "player_bust"
    if dealer_total > 21:
        return "dealer_bust"
    if player_total > dealer_total:
        return "win"
    if player_total < dealer_total:
        return "lose"
    return "push"



player_area = pygame.Rect(100, 400, 600, 150)
dealer_area = pygame.Rect(100, 100, 600, 150)
hand_value_box = pygame.Rect(420, 350, 250, 50)


#variables
wallet = 100
state = "menu"
round_started = False
bet = 0
bet_input = ""
dealer_draw_timer = 0
dealer_delay = 800

#win variables

result_applied = False
round_over_entered = False
game_over_reason = ""




CARD_WIDTH = 80
CARD_HEIGHT = 120
CARD_SPACING = 100
ranks = {
    "A": 11,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 10,
    "Q": 10,
    "K": 10
}

suits = ["♥", "♦", "♣", "♠"]

deck = []

for suit in suits:
    for rank, value in ranks.items():
        deck.append({
            "rank": rank,
            "value": value,
            "suit": suit
        })
random.shuffle(deck)



#lists
hand = []
hand_value = []
dealer_hand = []
discard_pile = []




#game loop
running = True
while running:

    #events

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        if state == "playing" and not round_started:
            result = None



        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # this is the first menu for the game
            #asks player if they want to play
            if state == "menu":
                if play_button.is_clicked(mouse_pos):
                    if wallet <= 0:
                        state = "game_over"
                    else:
                        state = "betting"
                        round_started = False

                if quit_button.is_clicked(mouse_pos):
                    state = "game_over"


            elif state == "betting":
                if bet_5_button.is_clicked(mouse_pos):
                    if bet + 5 <= wallet:
                        bet += 5
                        bet_input = str(bet)
                elif bet_10_button.is_clicked(mouse_pos):
                    if bet + 10 <= wallet:
                        bet += 10
                        bet_input = str(bet)
                elif bet_20_button.is_clicked(mouse_pos):
                    if bet + 20 <= wallet:
                        bet += 20
                        bet_input = str(bet)
                
                elif bet_play_button.is_clicked(mouse_pos):
                    if bet_input.isdigit():
                        bet = int(bet_input)

                        if bet > 0 and bet <= wallet:
                            state = "playing"
                            round_started = False


            #main playing phase
            #asks if player wants to hit or stand

            elif state == "playing":
                result = None

                if hit_button.is_clicked(mouse_pos):
                    draw_card(hand)

                    
                    

                    if calculate_hand(hand) > 21:
                        result = "player_bust"
                        state = "round_over"
                        round_over_entered = True

                        
                            
                        
            
                if stand_button.is_clicked(mouse_pos):
                    player_bj = is_blackjack(hand)
                    dealer_bj = is_blackjack(dealer_hand)

                    if player_bj or dealer_bj:
                        if player_bj and dealer_bj:
                            result = "push_blackjack"
                        elif player_bj:
                            result = "blackjack"
                        else:
                            result = "dealer_blackjack"

                        state = "round_over"
                        result_applied = False

                        continue



                    else:
                        state = "dealer_turn"
                        dealer_timer = pygame.time.get_ticks()




        if state == "game_over" and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
                    
            if play_again_button.is_clicked(mouse_pos):
                wallet = 100
                bet = 0
                bet_input = ""
                result_applied = False
                round_over_entered = False
                game_over_reason = ""

                hand.clear()
                dealer_hand.clear()

                deck = []
                for suit in suits:
                    for rank, value in ranks.items():
                        deck.append({"rank": rank, "value": value, "suit": suit})
                random.shuffle(deck)

                state = "betting"
                round_started = False


            if quit_end_button.is_clicked(mouse_pos):
                running = False
        #betting phase
        #asks player how much they want to bet before the playing phase
        if event.type ==pygame.KEYDOWN and state == "betting":

            if event.key == pygame.K_RETURN:
                if bet_input.isdigit():
                    bet = int(bet_input)

                    if bet > 0 and bet <= wallet:
                        state = "playing"
                        round_started = False
                bet_input = ""
            
            elif event.key == pygame.K_BACKSPACE:
                bet_input = bet_input[:-1]

            else:
                if event.unicode.isdigit():
                    bet_input += event.unicode

        
        
        if state == "round_over" and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            if play_again_button.is_clicked(mouse_pos):
                # reset round only
                hand.clear()
                dealer_hand.clear()

                bet = 0
                bet_input = ""

                result_applied = False
                round_over_entered = False

                state = "betting"

            elif quit_end_button.is_clicked(mouse_pos):
                state = "game_over"
                game_over_reason = "Player Quit"
                
            
        

    
    #game logic

    #main setup for the game at the beggining
    if state == "playing" and not round_started:

        hand.clear()
        dealer_hand.clear()

        draw_card(hand)
        draw_card(hand)

        draw_card(dealer_hand)
        draw_card(dealer_hand)

        

        

        round_started = True

        
    if state == "dealer_turn":
        current_time = pygame.time.get_ticks()

        if current_time - dealer_timer > dealer_delay:
            dealer_timer = current_time

            if calculate_hand(dealer_hand) < 17:
                draw_card(dealer_hand)
            else:
                result = resolve_round(hand, dealer_hand)
                state = "round_over"
                round_over_entered = True
                result_applied = False
        

        


    if state == "round_over" and round_over_entered and not result_applied:

    
        if not result_applied:

            
            if result == "blackjack":
                wallet += int(bet * 1.5)
            
            elif result == "win" or result == "dealer_bust":
                wallet += bet

            elif result == "push" or result == "push_blackjack":
                pass

            elif result in ["lose", "player_bust", "dealer_blackjack"]:
                wallet -= bet
            


            discard_pile.extend(hand)
            discard_pile.extend(dealer_hand)
            
            if wallet <= 0:
                state = "game_over"
                game_over_reason = "Out of Funds"

            # push = no change

            result_applied = True



        
                



        
    

    #DRAW
    screen.blit(background, (0, 0))

    # GLOBAL UI
    draw_text(f"Wallet: ${wallet}", 20, 20, font)

    # ---------------- MENU ----------------
    if state == "menu":
        play_button.draw(screen, font)
        quit_button.draw(screen, font)

    # ---------------- BETTING ----------------
    elif state == "betting":
        draw_text("Enter your bet:", 300, 200, font)

        if bet_input == "":
            draw_text("Type number...", 300, 250, font, (150, 150, 150))
        else:
            draw_text(f"${bet_input}", 300, 250, font)

        bet_5_button.draw(screen, font)
        bet_10_button.draw(screen, font)
        bet_20_button.draw(screen, font)
        bet_play_button.draw(screen, font)

    # ---------------- PLAYING + DEALER + ROUND OVER ----------------
    elif state in ["playing", "dealer_turn", "round_over", "game_over" ]:

        # table
        pygame.draw.rect(screen, (255, 255, 255), player_area, 2)
        pygame.draw.rect(screen, (255, 255, 255), dealer_area, 2)

        # hands
        hide_dealer = (state == "playing")
        if state == "game_over":
            hide_dealer = False
        draw_hand(hand, player_area)
        draw_hand(dealer_hand, dealer_area, hide_first_card=hide_dealer)

        # values ALWAYS updated
        player_value = calculate_hand(hand)
        dealer_value = calculate_hand(dealer_hand)

        # player value
        draw_text(
            f"Player: {player_value}",
            player_area.x,
            player_area.y + player_area.height + 10,
            font
        )

        # dealer value
        if state == "playing":
            draw_text(
                "Dealer: ?",
                dealer_area.x,
                dealer_area.y + dealer_area.height + 10,
                font
            )
        else:
            draw_text(
                f"Dealer: {dealer_value}",
                dealer_area.x,
                dealer_area.y + dealer_area.height + 10,
                font
            )

        # buttons only in playing
        if state == "playing":
            hit_button.draw(screen, font)
            stand_button.draw(screen, font)

        if state == "round_over":
            overlay = pygame.Surface((x, y))
            overlay.set_alpha(180)
            overlay.fill((0,0,0))
            screen.blit(overlay, (0, 0))
            draw_text(f"Results: {result}", 250, 200, font)

            
            quit_end_button.draw(screen, font)
            play_again_button.draw(screen, font)

        if state == "game_over":
            overlay = pygame.Surface((x, y))
            overlay.set_alpha(180)
            overlay.fill((0,0,0))
            screen.blit(overlay, (0, 0))
            

            draw_text("GAME OVER", 250, 200, font)
            draw_text(game_over_reason, 250, 260, font)

            play_again_button.draw(screen, font, (200, 0, 0))
            quit_end_button.draw(screen, font, (200, 0, 0))
            



        

    # ---------------- UPDATE SCREEN ----------------
    pygame.display.flip()

pygame.quit()
sys.exit()