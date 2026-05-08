import pygame
import sys
import random
import BlackJack_functions


pygame.init()



class button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x,y,width,height)
        self.text = text

    def draw(self, screen, font):
        pygame.draw.rect(screen, (0, 200, 0), self.rect)

        text_surface = font.render(self.text, True, (255, 255, 255))
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 10))
    
    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)





#screen size
x, y = 800, 600
screen = pygame.display.set_mode((x,y))
pygame.display.set_caption("blackjack")


#buttons and UI
hit_button = button(100, 350, 120, 50, "Hit")
stand_button = button(250, 350, 120, 50, "Stand")
play_button = button(300, 200, 200, 60, "play")
quit_button = button(300, 300, 200, 60, "Quit")

font = pygame.font.SysFont("arial",36)

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
    card = deck.pop()
    hand.append(card)


player_area = pygame.Rect(100, 400, 600, 150)
dealer_area = pygame.Rect(100, 100, 600, 150)
hand_value_box = pygame.Rect(420, 350, 250, 50)

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

#variables
wallet = 100
state = "menu"
round_started = False
bet = 0
bet_input = ""



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


            
                
            #main playing phase
            #asks if player wants to hit or stand

            elif state == "playing":

                if hit_button.is_clicked(mouse_pos):
                
                    draw_card(hand)
                    
                    

                    if calculate_hand(hand) > 21:
                        print("bust")
                        state = "round_over"
                            
                        
            
                if stand_button.is_clicked(mouse_pos):
                    print("stand")
                    state = "dealer_turn"
        

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
        
        

    
    #game logic

    #main setup for the game at the beggining
    if state == "playing" and not round_started:

        hand.clear()
        dealer_hand.clear()

        draw_card(hand)
        draw_card(hand)

        draw_card(dealer_hand)

        

        round_started = True
        

        
    

    #DRAW
    screen.fill((0,0,0))
    #global UI
    draw_text(f"Wallet:${wallet}", 20, 20, font)
    #state UI
    if state == "playing":
        hit_button.draw(screen, font)
        stand_button.draw(screen, font)

        pygame.draw.rect(screen, (255,255,255), player_area, 2)
        pygame.draw.rect(screen, (255,255,255), dealer_area, 2)

        draw_hand(hand, player_area)
        draw_hand(dealer_hand, dealer_area, hide_first_card=(state=="playing"))

        pygame.draw.rect(screen, (255, 255, 255), hand_value_box, 2)
        current_value = BlackJack_functions.calculate_hand(hand)
        draw_text(
    f"Hand value: {BlackJack_functions.calculate_hand(hand)}",
    hand_value_box.x + 10,
    hand_value_box.y + 10,
    font,
    (255, 255, 255)
)


    
    elif state == "menu":
        play_button.draw(screen, font)
        quit_button.draw(screen, font)

    elif state == "betting":
        draw_text("enter your bet:", 300, 200, font)
        if bet_input == "":
            draw_text("Type number...", 300, 250, font, (150, 150, 150))
        else:
            draw_text(f"${bet_input}", 300, 250, font)
    #dislpay flip
    pygame.display.flip()

pygame.quit()
sys.exit()