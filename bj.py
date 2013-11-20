# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = "KA AH"
score = 0
player_BJ = False
dealer_BJ = False
dealer_dealing = False
player_number_color = "Black"

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0]*1.2, pos[1] + CARD_CENTER[1]*1.2], [CARD_SIZE[0]*1.5, CARD_SIZE[1]*1.5])

# define hand class
class Hand:
    def __init__(self):
        self.hand = []
        self.value = 0
        self.A_in_hand = 0
        self.ValueType = ""

    def __str__(self):
        s = "Hand contains: "
        for c in self.hand:
            s += str(c) + " "
        return s

    def add_card(self, card):
        self.hand.append(card)

    def get_value(self):
        self.value = 0
        self.ValueType = ""
        for i in range(len(self.hand)):  
            if self.ValueType == "Soft" and len(self.hand) != 2:
                self.value += VALUES.get(self.hand[i].get_rank()) - 10
                self.ValueType = "Hard"
            else:
                self.value += VALUES.get(self.hand[i].get_rank())
                self.ValueType = "Hard"
                if self.hand[i].get_rank() == 'A' and self.value <= 11:
                    self.value += 10
                    self.ValueType = "Soft"
        if len(self.hand) == 2:
            self.ValueType = "Soft"
        return self.value
   
    def draw(self, canvas, pos):
        for c in self.hand:
            c.draw(canvas, [pos[0] + self.hand.index(c) * 25, pos[1]])

# define Deck class
class Deck:
    def __init__(self):
        self.dealt_card = []
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit, rank))

    def shuffle(self):
        for c in self.dealt_card:
            self.deck.append(c)    
        random.shuffle(self.deck)

    def deal_card(self):
        self.dealt_card = self.deck.pop(0)
        return self.dealt_card
    
    def __str__(self):
        s = "Deck contains: "
        for c in self.deck:
            s += str(c) + " "
        return s

#define event handlers for buttons
def deal():
    global score, outcome, in_play, DEALER_HAND, PLAYER_HAND, current_deck, player_BJ, dealer_BJ, dealer_dealing, player_number_color
    player_number_color = "Black"
    if in_play == False:
        DEALER_HAND = Hand()
        PLAYER_HAND = Hand()
        current_deck = Deck()
        current_deck.shuffle()
        PLAYER_HAND.add_card(current_deck.deal_card())
        DEALER_HAND.add_card(current_deck.deal_card())
        dealer_dealing = True
        PLAYER_HAND.add_card(current_deck.deal_card())
        DEALER_HAND.add_card(current_deck.deal_card())
        outcome = "Dealer showing " + str(DEALER_HAND.hand[1].get_rank()) + ", hit or stand?"
        if PLAYER_HAND.get_value() == 21: 
            outcome = "BLACKJACK! Click stand!"
            player_BJ = True
        elif DEALER_HAND.get_value() == 21:
            dealer_BJ = True
        in_play = True
    else: 
        outcome = "Don't click deal during a round!"
        score -= 1
        in_play = False
        
def hit():
    global outcome, in_play, score, current_deck, player_number_color
    #print in_play, player_BJ
    if in_play == True and PLAYER_HAND.get_value() < 21:
        PLAYER_HAND.add_card(current_deck.deal_card())
        #print current_deck
        #print "Player value: " + str(PLAYER_HAND.get_value())
        if PLAYER_HAND.get_value() > 21:
            outcome = "Oh boy..BUSTED! Click stand!"
            player_number_color = "Red"
            #print "value: " + str(PLAYER_HAND.get_value()) + " outcome: " + str(outcome) + " score: " + str(score)
        elif PLAYER_HAND.get_value() == 21: 
            outcome = "NICE! 21! Click stand!"
            #print outcome
    pass

def stand():
    global outcome, in_play, score, player_BJ, dealer_BJ, dealer_dealing, current_deck
    if in_play == True and dealer_BJ == False:
        while DEALER_HAND.get_value() < 17:
            DEALER_HAND.add_card(current_deck.deal_card())
        dealer_dealing = False
        in_play = False
        if DEALER_HAND.get_value() >= PLAYER_HAND.get_value() and DEALER_HAND.get_value() <= 21:
            if DEALER_HAND.get_value() == PLAYER_HAND.get_value():
                outcome = "LOL too bad! teacher says dealer wins ties! New deal?"
                score -= 1
            else:
                outcome = "Dealer has " + str(DEALER_HAND.get_value()) + "...You lose! New deal?"
                score -= 1
        elif PLAYER_HAND.get_value() > 21:
            outcome = "and..Dealer would've had " + str(DEALER_HAND.get_value()) + "! New deal?"
            score -= 1
        else: 
            outcome = "Dealer has " + str(DEALER_HAND.get_value()) + " You win! New deal?"
            score += 1
        pass
    elif in_play == True and dealer_BJ == True:
        dealer_dealing = False
        outcome = "LOL game is rigged! You lose! New deal?"
        score -= 1    
    in_play = False
    player_BJ = False
    dealer_BJ = False

# draw handler    
def draw(canvas):
    canvas.draw_circle([500, -100], 700, 36, "Maroon", "Green")
    
    # draw player circles
    canvas.draw_circle([90, 300], 50, 8, "Gray")
    canvas.draw_circle([909, 300], 50, 8, "Gray")
    canvas.draw_circle([739, 420], 50, 8, "Gray")
    canvas.draw_circle([500, 490], 50, 8, "Gray")
    canvas.draw_circle([260, 420], 50, 8, "Gray")
    
    # draw dealer line
    canvas.draw_polyline([[210, 140], [380, 260], [500, 290], [619, 260], [789, 140]], 10, "Gold")
   
    # draw dealer deck
    for i in range(20):
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [900, 110-i*10], [CARD_BACK_SIZE[0]*1.3, CARD_BACK_SIZE[1]*1.55])
    
    # draw hands
    PLAYER_HAND.draw(canvas, [400, 350])
    DEALER_HAND.draw(canvas, [400, 70])
    if dealer_dealing == True:
        canvas.draw_image(card_back, [12.5, 48], [24, 96], [400, 130], [25*1.3, 96*1.55])
    
    # draw outcomes
    canvas.draw_text(outcome, (10, 55), 20, "Lime", "sans-serif")
    canvas.draw_text("Money: $" + str(score * 100), (689, 550), 50, "Lime", "sans-serif")
    canvas.draw_text("Dummy addition:", (130, 415), 25, "Black", "sans-serif")
    canvas.draw_text(str(PLAYER_HAND.get_value()), (325, 425), 50, player_number_color, "sans-serif")
    canvas.draw_text("BlackJack", (390, 30), 35, "Black", "sans-serif")

# initialization frame
frame = simplegui.create_frame("Blackjack", 1000, 600)
frame.set_canvas_background("Black")

#create buttons and canvas callback
label = frame.add_label("Welcome to Albert's Casino!")
label2 = frame.add_label("Rules:")
label3 = frame.add_label("1. Click Deal to start")
label4 = frame.add_label("2. Dealer wins ties!")
label5 = frame.add_label("3. Click 'Stand' when you bust or have Blackjack to see what the dealer has.")

frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
frame.start()
PLAYER_HAND = Hand()
DEALER_HAND = Hand()
current_deck = Deck()

# remember to review the gradic rubric