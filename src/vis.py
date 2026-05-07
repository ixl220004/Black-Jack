import pygame
import sys
import Blackjack

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


#buttons
hit_button = button(100, 500, 120, 50, "Hit")
stand_button = button(250, 500, 120, 50, "Stand")
play_button = button(300, 200, 200, 60, "play")
quit_button = button(300, 300, 200, 60, "Quit")

font = pygame.font.SysFont(None,36)

def draw_text(text, x, y, font, color=(255, 255, 255)):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x,y))



wallet = 100
state = "menu"
round_started = False
bet = 0
bet_input = ""


hand = []
hand_value = []
dealer_hand = []
discard_pile = []

with open("deck.txt", 'r') as f:
  deck = [line.strip() for line in f]


#game loop
running = True
while running:
    #event
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False



        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()


            if state == "menu":
                if play_button.is_clicked(mouse_pos):
                    if wallet <= 0:
                        state = "game_over"
                    else:
                        state = "betting"
                        round_starded = False

                if quit_button.is_clicked(mouse_pos):
                    state = "game_over"


            
                
        
            elif state == "playing":

                if hit_button.is_clicked(mouse_pos):
                
                    Blackjack.draw_card(hand)
                    print(hand)
                    

                    if Blackjack.calculate_hand(hand) > 21:
                        print("bust")
                        state = "round_over"
                            
                        
            
                if stand_button.is_clicked(mouse_pos):
                    print("stand")
                    state = "dealer_turn"
        
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

    if state == "playing" and not round_started:

        hand.clear()
        dealer_hand.clear()

        Blackjack.draw_card(hand)
        Blackjack.draw_card(hand)

        Blackjack.draw_card(dealer_hand)

        print(f"{hand}")

        round_started = True
        

        
    

    #draw
    screen.fill((0,0,0))
    if state == "playing":
        hit_button.draw(screen, font)
        stand_button.draw(screen, font)
    
    elif state == "menu":
        play_button.draw(screen, font)
        quit_button.draw(screen, font)

    elif state == "betting":
        draw_text("enter your bet:", 300, 200, font)
        draw_text(bet_input, 300, 250, font)
        draw_text(f"Wallet: ${wallet}", 300, 150, font)

    #dislpay flip
    pygame.display.flip()

pygame.quit()
sys.exit()