import random as rn

original_deck = [x for x in range(0,52)]
suites = "Diamonds Clubs Hearts Spades".split()
royal_cards = {1 : "Ace", 11: "Jack", 12 : "Queen", 13: "King"}

def card_to_string(index):
    """Converts a single card index to a string representation with suite and face value"""
    value = (index % 13) + 1
    face = str(value) if value not in royal_cards else royal_cards[value]
    suite = suites[(index // 13)]
    return "{0} of {1}".format(face, suite)

def poker_hands(cards):
    """Determines what poker hands exist in the given cards. So, if we give this the cards+river,
    it will produce all of the hands (e.g flush, straight, two-pair) from all of those cards combined.
    The return type of this function is a list of all the poker hands this contains."""
    poker_hands = []
    face_count = [0 for x in range(0, 13)] # Create a frequency table of the cards
    suite_count = [0,0,0,0]

    for c in cards: # Go through every card and record the number of times each one occurs
        value, suite = (c % 13), (c // 13)
        face_count[value] += 1
        suite_count[suite] += 1

    for index in range(0, 13): # This will generate all of the occurences of pairs
        if face_count[index] > 1:
            poker_hands.append("{0}-of-a-kind".format(face_count[index]))

    for s in suite_count:
        if s >= 5:
            poker_hands.append("Flush")

    for i in range(0, (13 - 5)):
        possible_straight = face_count[i:i+5]
        if all(c > 0 for c in possible_straight):
            poker_hands.append("Straight")

    if any(h is "Straight" for h in poker_hands) and any(h is "Flush" for h in poker_hands):
        poker_hands.remove("Straight")
        poker_hands.remove("Flush")
        poker_hands.append("Straight-Flush")

    return poker_hands


class Player:
    def __init__(self, chips):
        """Initialize the Player class with some initial chips"""
        self.chips = chips
        self.cards = []

    def __str__(self):
        """Return a string representation of the player. In our case this is just the cards the player
        has in their hand. """
        return str([card_to_string(c) for c in self.cards])

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

    def __str__(self):
        result = ""
        for i in range(0, len(self.players)):
            result += "P{0}: {1}\n".format(i+1, str(self.players[i]))

        return result + "River: " + self.print_river()

    def random_card(self):
        """Pop a random card from this rounds' deck. """
        return self.cards.pop(rn.randrange(0, len(self.cards), 1))

    def print_river(self):
        return str([card_to_string(c) for c in self.river])

    def deal(self):
        """
        TODO:
            * Fix it so that players take turns doing actions with their initial cards, THEN place the river.

        Deal two random cards to every player and set up the initial three cards of the river.
        """
        for p in self.players:
            p.cards = [self.random_card(), self.random_card()]

        # Do some actions here...

        for i in xrange(3):
            self.river.append(self.random_card())

    def play(self):
        """
        This is the main game loop. It will go through each player and prompt them for an action until
        either the river has 5 cards or all but one player has folded.
        """

        self.deal()
        while len(self.players) > 1 and len(self.river) < 5:
            for p in self.players:
                # process player 'p' in some way...
                pass


# # Sample Game
# p1 = Player(100)
# p2 = Player(100)
# r1 = Round([p1, p2])
#
# r1.deal()
# print r1
# print poker_hands(r1.river + p1.cards)


# Testing Poker Hands detection
print(poker_hands([0, 1, 2, 3, 4])) # Straight Flush
print(poker_hands([0, 1 + 13, 2, 3, 4])) # Straight
print(poker_hands([0, 2, 4, 6, 8])) # Flush
print(poker_hands([0, 0+13, 0+26, 0+39, 1])) # Four-of-a-kind
print(poker_hands([0, 0+13, 0+26, 2, 1])) # Three-of-a-kind
print(poker_hands([0, 0+13, 3, 4, 1])) # Two Pair
