import random as rn

original_deck = [x for x in range(0,52)]

class Player:
    def __init__(self, chips):
        """Initialize the Player class with some initial chips"""
        self.chips = chips
        self.cards = []

    def __str__(self):
        """Return a string representation of the player. In our case this is just the cards the player
        has in their hand. """
        return str(self.cards)

    def act(self):
        """ Player function to interact with the game. This function ought to return the action the
        player wants to take, up to and including the amount of money they want to bet. """
        pass

class Round:
    def __init__(self, players):
        """Initialize a single round of the game. The cards start out as a fresh deck. River is empty."""
        self.cards = original_deck
        self.river = []
        self.players = players

    def random_card(self):
        """Pop a random card from this rounds' deck. """
        return self.cards.pop(rn.randrange(0, len(self.cards), 1))

    def deal(self):
        """
        TODO:
            * Fix it so that players take turns doing actions with their initial cards, THEN place the river.

        Deal two random cards to every player and set up the initial three cards of the river.
        """
        for p in self.players:
            p.cards = [self.random_card(), self.random_card()]

        for i in xrange(3):
            self.river.append(self.random_card())

    def play(self):
        """
        This is the main game loop. It will go through each player and prompt them for an action until
        either the river has 5 cards or all but one player has folded. 
        """
        while len(self.players) > 1 and len(self.river) < 5:
            for p in self.players:
                # process player 'p' in some way...






p1 = Player(100)
p2 = Player(100)
r1 = Round([p1, p2])

r1.deal()
print "player1 cards: " + str(p1)
print "player2 cards: " + str(p2)
print "River: " + str(r1.river)
