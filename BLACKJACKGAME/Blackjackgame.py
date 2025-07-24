# We'll use this later
import random 
import time
'''This is the outside variables of the cards'''
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 
            'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

Casino_chips = {"Black":100, "Green": 25, "Red":5, "White":1}
'''
Creating a Card Class with outside variables¶
Here we will use some outside variables that we know don't change regardless of the situation, such as a deck of cards. 

'''

'''
Methods:(DECK CLASS)
__init__(self): The __init__ method to create the deck. The function needs to create all 52 cards and put them into the cards attribute.
shuffle(self): A function of randomly rearranging the deck cards.
deal_card(self): A function to discard and return the top card on the deck.
cards_left(self): A function to return how many cards are left in the deck.
__str__(self): An optional method to offer a string description of the deck.
'''
class Card:
    
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]
    
    def __eq__(self, other):
        return self.suit == other.suit and self.rank == other.rank
        
    def __str__(self):
        return self.rank + ' of ' + self.suit
    
        

new_deck = []
'''
Using a class within another class
'''
class Deck(Card):
    
    def __init__(self):
        self.shared_deck = []
        for suit in suits:
            for rank in ranks:
                self.shared_deck.append(Card(suit,rank))
    def deal_one(self):
        return self.shared_deck.pop()

    def shuffle(self):
        random.shuffle(self.shared_deck)
    

    
#testing...
mydeck = Deck()
mydeck.shuffle()

#This will be the player class that will be used in the game logic
class Player(Deck):
    
    def __init__(self, name,deck,balance = 0):
        Deck.__init__(self)
        self.name = name
        self.player_hand = []
        self.deck = deck
        self.balance = balance
        pass
        
    def Stand():
        pass
    
    
    def Hit(self):
        self.player_hand.append(mydeck.deal_one())
    
    def deposit(self):
        amount = int(input("How much would you like to wager? Note: The maximum bet is $2,500.25"))
        if amount > 0:
            self.balance += amount
            print(f"Deposited ${amount}. New balance: ${self.balance}")
        else:
            print("Invalid deposit amount.")
        
        
        
        
 
    
    def value_of_card(self):
        counter = 0
        for card in self.player_hand:
            counter += card.value
            
        if counter > 21:
            for card in self.player_hand:
                if card.rank == 'Ace':
                    counter -= 10
        return counter

    
        
    


#testing......


#Dealer Class is gonna be made with attributes and methods and will also be used in game logic

class Dealer(Deck):
    
    def __init__(self, deck):
        Deck.__init__(self)
        self.dealer_hand = []
        self.deck = deck
        pass
        
        
    def Hit(self):
        self.dealer_hand.append(mydeck.deal_one())

        
            
    def Stand(self):
        pass

    def value_of_card(self):
        total = 0
        for card in self.dealer_hand:
            total += card.value
        return total

#Create player and dealer, sharing a single deck through arguments
myplayer = Player("player one", mydeck)
mydealer = Dealer(mydeck)
        
#testing...







class Chips():

    def __init__(self, total=100):
        self.total = total  # This can be set to a default value or supplied by a user input
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet






def take_bet(chips):

    while True:

        try:
            chips.bet = int(input("How many chips would you like to bet?: "))
        except:
            print("Sorry please provide an intenger")
        else:
            if chips.bet > chips.total:
                print(f"Sorry, you do not have enough chips! You have: {chips.total}")
            else:
                break


#STEP 9: WRITE FUNCTIONS TO DISPLAY CARDS

def show_some(player,dealer):
    print("Your hand:")
    for card in player.player_hand:
        print(card)
    print("Values:",player.value_of_card())
    print("\n")
    print("Dealer's hand:")
    for card in dealer.dealer_hand[0:1]:
        print(card)
    print("Hidden Card")
    print("Values:",)
    print("\n")
            

def show_all(player,dealer):

    print("Dealer's hand:")
    for card in dealer.dealer_hand:
        print(card)
    print("Values:", dealer.value_of_card())
    print("\n")



def round_count():
    global choice
    while True:
            try:
                choice = int(input("Welcome to blackjack, how many games would you like to play?").lower())
                break
            except ValueError:
                print("Invalid input. Please enter an integer.")



def bet_count(chips):
    print('shuffling...')   
    time.sleep(4)
    print('Place your bets')
    time.sleep(4)  

    
    while True:
        try:
            chips.bet = int(input('How many chips would you like to bet? '))
        except ValueError:
            print('Sorry, a bet must be an integer!')
        else:
            if chips.bet > chips.total:
                print("Sorry, your bet can't exceed",chips.total)
            else:
                break              


        

        
        
        






#AND NOW ON TO THE GAME!!

#GAME LOGIC





#Deal two cards to player and dealer
myplayer.Hit()
myplayer.Hit()
mydealer.Hit()
mydealer.Hit()


def player_turn(chips):
    global num_of_round
    num_of_round = 0
    num_of_round +=1
    while True:

        
        #show cards, but keep one of the dealer's card hidden
        show_some(myplayer,mydealer)
        
        #User Input
        sec_choice = input("Please choose 'Hit' or 'Stand':").lower()

        if sec_choice == 'Hit'.lower():
            myplayer.Hit()
        elif sec_choice == 'Stand'.lower() or sec_choice == 'Quit'.lower():
            num_of_round += 1
            break
        if myplayer.value_of_card() > 21:
            num_of_round += 1
            print("\n")
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            print("Player BUSTS, Dealer wins!")
            chips.lose_bet()
            print("Final Value:",myplayer.value_of_card())
            print('Final Card:', myplayer.player_hand[-1] )
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            print("\n")
            break
    
  








            

def dealer_turn(chips):
    while mydealer.value_of_card() <= 17:
        mydealer.Hit()
        
        
    print("Dealer's hand:")
    for card in mydealer.dealer_hand:
        print(card)
    print("Values:", mydealer.value_of_card())
    print("\n")    
    
    if mydealer.value_of_card() > 21:
        print("\n")
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print("Dealer BUSTS, you win!")
        chips.win_bet()
        print("\n")
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    
    
    elif mydealer.value_of_card() > myplayer.value_of_card():
        print("\n")
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print("Dealer Wins!")
        chips.lose_bet()
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print("\n")
        
    elif myplayer.value_of_card() > mydealer.value_of_card():
        print("You win!")
        chips.win_bet()
    
    else:
        print("\n")
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print("Draw!")
        print("\n")
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    



#translates to dealer after, players turn


#play again function
def play_game(chips):  # Renamed for clarity
    myplayer.player_hand = []  # Clear player's hand
    mydealer.dealer_hand = []  # Clear dealer's hand
    chips.bet
    # ... (Other reset logic, like handling bets)
    myplayer.Hit()
    myplayer.Hit()
    mydealer.Hit()
    mydealer.Hit()
     
    
    # Prompt the Player for their bet
    take_bet(chips)
    player_turn(chips)
    if myplayer.value_of_card() <= 21:
        dealer_turn(chips)
    
    # Inform Player of their chips total 
    print("\nPlayer's winnings stand at",chips.total)


def main():  # Main game loop
    round_count()  # Get number of rounds
    mychips = Chips()
    for round_num in range(1, choice + 1):  # Loop for the specified number of rounds
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print(f'Game {round_num} of {choice}')
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        play_game(mychips) # Play a single round
        # Ask if the player wants to continue (if not the last round)
        if round_num < choice:
            if input("Play again? (y/n): ").lower() != 'y':
                break  # Exit the loop if the player doesn't want to continue
        
    print("@@@@@ Thanks for Playing!!!!! @@@@@@@")
# Trails to dealer turn....Organize it later

# Run the game
if __name__ == "__main__":
    main()






