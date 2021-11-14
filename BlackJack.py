import random 
suits = ["Spades","Hearts","Clubs","Diamonds"]
numbers = ["Two","Three","Four","Five","Six","Seven","Eight","Nine","Ten","Jack","Queen","King","Ace"]
point_dic = {"Two":2,"Three":3,"Four":4,"Five":5,"Six":6,"Seven":7,"Eight":8,"Nine":9,"Ten":10,"Jack":10,"Queen":10,"King":10,"Ace":[1,11]}

class card:
    """
    A class that defines what attributes a card in a deck should have and allows us to print that information
    """
    
    def __init__(self,suit,number):
        self.suit = suit
        self.number = number
    # Standard card attributes defined in the init method
        
    def __str__(self):
        return "The {} of {}".format(self.number,self.suit)
    # An easy way to print the info from the card

class bankroll:
    """
    Essentially the amount of money a player has
    """
    
    def __init__(self,amount):
        self.amount = amount
    # the amount of money we start with
    
    def deposit(self,winnings):
        self.amount = self.amount + winnings
        print("You now have {} gazillion dollars".format(self.amount))
    # the amount of money we win
    
    def withdraw(self,bet):
        if bet <= self.amount:
            self.amount = self.amount - bet
            print("You now have {} gazillion dollars".format(self.amount))
        else:
            print("Looks like you gambled your life away, you only have {} gazillion dollars".format(self.amount))
    # the amount of money we use
    
    def __str__(self):
        return str(self.amount)
        
class Deck:
    """
    A deck of 52 cards with their suits and numbers
    """
    
    def __init__(self,suits,numbers):
        self.cards = []
        # empty list right now
        for suit in suits:
            for number in numbers:
                self.cards.append(card(suit,number))
    # creates a deck of cards
    
    def __str__(self):
        return str(self.cards[0])
    # shows the entire deck
    # apparently this method is supposed to return a string always so I put my value in there
    
    def shuffle(self):
        random.shuffle(self.cards)
    # shuffles the deck, cool
    
    def draw(self):
        return self.cards.pop(0)
    # ok so using this you can take card from the deck and give it to something like a player
    

class player:
    """
    Attributes specific to players
    """
    
    def __init__(self,hand):
        self.hand = hand
    # the initial hand the player gets
    
    def hit(self,new_card):
        self.hand.append(new_card)
    # and this should get the player a new card when he asks for a hit
    
    def points(self,point_dic,Ace_val=0):
        """
        function that calculates the points in a hand of cards
        """
        sum = 0
        for card in self.hand:
            if card.number == "Ace":
                sum = sum + point_dic[card.number][Ace_val]
            else:
                sum = sum + point_dic[card.number]
        return sum
        # a method that returns the amount of points a player has
        
    def __str__(self):
        return (self.hand)
    
    #def __len__(self):
     #   return (self.hand)
        
    def hand_printer(self):
        i = 0
        while i < len(self.hand):
            print(self.hand[i])
            i += 1
    # method that prints the cards in the hand but can hide one for the computer
        
def choice():
    """ 
    function that asks the player what to do
    """
    choose = False
    
    while choose not in ["Hit","Stay"]:
        choose = input("So you wanna 'Hit' or 'Stay'?:")
    
    return choose


def ask_bet():
    
    try:
        bet = int(input("How much are you willing to bet kiddo? in gazillions of dollars btw"))
        
    except ValueError:
        print("A bet has to be a non zero number come on")
        bet = int(input("A number this time please"))

    return bet 

def ask_ACE():
    """ 
    function that asks the player what to count Ace as, either 1 or 11
    """
    choose = False
    
    while choose not in [1,11]:
        choose = int(input("Ace should be 1 or 11? :"))
    
    if choose == 1:
        return 0
    elif choose == 11:
        return 1
    
def rerun():
    """
    checks if players want to play again
    """
    choice = False
    
    while choice not in ["Y","N"]:
        
        choice = input("Do you want to play again? Y or N")
        
        if choice not in ["Y","N"]:
            print("Please choose either Y or N")
        
    return choice
    

def BlackJack():
    """
    A game of BlackJack with one dealer and one player
    """
    
    myfunds = bankroll(100)
    # create some pocket money
    print("You have {} gazillion dollars".format(myfunds))
    
    game_cont = "Y"
    # for multiple games
    
    while myfunds.amount > 0 and game_cont == "Y": 
    # this loop is reserved for multiple games
            
        mydeck = Deck(suits,numbers)
        # initialize a deck of cards for each game
        mydeck.shuffle()
        # shuffle said deck

        bet = ask_bet()
        # ask the player how much he/she would like to bet
        myfunds.withdraw(bet)

        Computer = player([mydeck.draw(),mydeck.draw()])
        # so we are essentially popping off cards from the deck and giving them to the hand
        print("The dealer has a:")
        print(Computer.hand[0])
        # give cards to the dealer and reveal one

        Player1 = player([mydeck.draw(),mydeck.draw()])
        print("You have:")
        print(Player1.hand[0])
        print(Player1.hand[1])
        # give cards to player and reveal both

        Ace_type = 0
        # by default the ACE value is 1, but if player gets one then we ask 
        Player1_turn = True
        # initially it will be player 1 turn

        while True:

            #Player1_turn != Player1_turn
            # this will set the player 1 turn to true the first time this loop runs

            if Player1_turn == True:
                for card in Player1.hand:
                    if card.number == "Ace":
                        Ace_type = ask_ACE()

            if Player1.points(point_dic,Ace_type) > 21:
                print("\nUnfortunately you've gone bust!")
                break
            elif Computer.points(point_dic,1) > 21:
                print("\nDealer went bust! but you double your money!")
                myfunds.deposit(bet*2)
                break
                # the computer/dealer always uses the same value for ACE, its 11
            elif Player1_turn == False and Computer.points(point_dic,1) > Player1.points(point_dic,Ace_type):
                print("\nUnfortunately you've lost")
                break
                # only check this condition if player 1 has had his turn
            elif Player1.points(point_dic,Ace_type) == 21:
                print("\nWinner Winner Chicken Dinner! 21 baby!")
                myfunds.deposit(bet*2)
                break
                # only check 
            else:
                pass
            # if none of these conditions is met it means game is still continuing

            #print("and now you've gotten past the win checks")

            if Player1_turn == True:
                Hit_Stay = choice()
                if Hit_Stay == "Hit":
                    Player1_turn == True
                    Player1.hit(mydeck.draw())
                    i = 0
                    print("\nYour hand is:")
                    Player1.hand_printer()
                    continue
                    # check whether new card made a difference
                elif Hit_Stay == "Stay":
                    #print("Do we ever understand whether its stay?")
                    Player1_turn = False
                    continue
                    # would like to start the loop again as part of a new turn

            #print("Does the code ever reach here when stay?")

            if Player1_turn == False:
                Computer.hit(mydeck.draw())
                i = 0
                print("\nThe Dealer's hand is:")
                Computer.hand_printer()
                continue
                # the computer will continue like this
                
        if myfunds.amount <= 0:
            print ("Looks like someone is out of money :(")

        game_cont = rerun()
        