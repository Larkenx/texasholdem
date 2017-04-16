# -*- coding: utf-8 -*-
import random as rn

original_deck = [x for x in range(0,52)]
# suites = "Diamonds Clubs Hearts Spades".split()
suites = "♦ ♣ ♥ ♠".split()
royal_cards = {9: "Jack", 10 : "Queen", 11: "King", 12 : "Ace"}

def card_to_string(index):
    """Converts a single card index to a string representation with suite and face value"""
    value = (index % 13)
    face = str(value+2) if value not in royal_cards else royal_cards[value]
    suite = suites[(index // 13)]
    # return "{0} of {1}".format(face, suite)
    return "{0}{1}".format(face, suite)

def poker_hands(cards):
    """Determines what poker hands exist in the given cards. So, if we give this the cards+river,
    it will produce all of the hands (e.g flush, straight, two-pair) from all of those cards combined.
    The return type of this function is a list of tuples, where the first element is the name/id of the poker
    hand (straight, flush, etc) and the second element of the tuple is a list of indices of the cards from the input
    that comprise of the poker hand.

    Input: cards as a list of integers
    [Integer ...]
    Output: List of tuples of poker hands
    [(String, [Integer ...]), ...]

    NOTE: In the API given for the final project, it may be necessary to differentiate the hands held
    by the player and the cards in the river. To do this, we program it such that the first two cards given
    to this function are always the player's cards, so cards[:2] will always yield the cards in our hand.
    """

    poker_hands = []
    face_count = [[] for x in range(0, 13)]  # Store cards from the input into bins. They are divided by face value
    suite_count = [[] for x in range(0, 4)] # Same for cards of the same suite
    straights = []  # it's possible to have more than one...
    flushes = []  # same as above
    straight_flushes = [] # super unlikely...but same as above

    for c in cards:  # Go through every card and record the number of times each one occurs
        value, suite = (c % 13), (c // 13)
        face_count[value].append(c)
        suite_count[suite].append(c)

    for index in range(0, 13): # Find n-pairs
        num_of_cards = len(face_count[index])
        if num_of_cards > 1:
            hand = ["{0}-of-a-kind".format(num_of_cards), face_count[index]]
            poker_hands.append(hand)

    for i in range(0, 4): # flush
        if len(suite_count[i]) >= 5:
            hand = ["Flush", suite_count[i]]
            poker_hands.append(hand)
            flushes.append(hand[1])

    for i in range(0, (14 - 5)): # straight
        possible_straight = face_count[i:i+5]
        if all(c for c in possible_straight): # using implicitness of [] != True
            poker_hands.append(["Straight", sum(possible_straight, [])])
            straights.append(sum(possible_straight, []))

    if straights and flushes: # check for straight-flush
        sorted_s = [sorted(s) for s in straights]
        sorted_f = [sorted(f) for f in flushes]
        for s in sorted_s:
            if s in sorted_f:
                poker_hands.append(["Straight-Flush", s])
                straight_flushes.append(s)

    if straight_flushes: # check for royal-flush
        for s in straight_flushes:
            face_vals = [c % 13 for c in s]
            if face_vals == [8, 9, 10, 11, 12]:
                poker_hands.append(["Royal-Flush", s])

    # Every hand has a "high card" which may be used as a tie-breaker, particularly if the poker hands
    # above are as a result of poker hands from the river cards.
    poker_hands.append(["High Card", [max([c % 13 for c in cards])]])

    return poker_hands

def print_poker_hand(hands):
    """Prints all of the poker hands and the cards that they are comprised of. Special case for high card."""
    result = ""
    for h in hands:
        if len(h[1]) == 1:
            result += "{0} with {1}.\n".format(h[0], card_to_string(h[1][0]))
        else:
            result += "{0} with {1} and {2}.\n".format(h[0],
                                            ", ".join([card_to_string(c) for c in h[1][:-1]]),
                                            card_to_string(h[1][-1]))
    print(result)


def best_hand(cards): # takes poker_hands, find exact cards
    if cards.contains("Straight-Flush"):
        return
    if cards.contains("4-of-a-kind"):
        return
    if cards.contains("Full House"):
        return
    if cards.contains("Flush"):
        return
    if cards.contains("Straight"):
        return
    if cards.contains("3-of-a-kind"):
        return
    if set(["2-of-a-kind", "2-of-a-kind"]):
        return
    if cards.contains("2-of-a-kind"):
        return

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



# Testing Index to Card Number
# print(card_to_string(0)) # 2 Diamonds
# print(card_to_string(9)) # Jack
# print(card_to_string(10)) # Queen
# print(card_to_string(11)) # King
# print(card_to_string(12)) # Ace
# print(card_to_string(13)) # 2 Clubs
# print(card_to_string(26)) # 2 Hearts
# print(card_to_string(39)) # 2 Spades
# print(card_to_string(51)) # Ace Spades

# Testing Poker Hands detection
print_poker_hand(poker_hands([8, 9, 10, 11, 12])) # Royal-Flush and Straight-Flush
print_poker_hand(poker_hands([0, 1 + 13, 2, 3, 4])) # Straight
print_poker_hand(poker_hands([0, 2, 4, 6, 8])) # Flush
print_poker_hand(poker_hands([0, 0+13, 0+26, 0+39, 1])) # Four-of-a-kind
print_poker_hand(poker_hands([0, 0+13, 0+26, 2, 1])) # Three-of-a-kind
print_poker_hand(poker_hands([0, 0+13, 3, 4, 1])) # Two Pair
print_poker_hand(poker_hands([0, 2+13, 2, 4+13, 4])) # 2 Two Pairs
print_poker_hand(poker_hands([4+26, 2+13, 2, 4+13, 4])) # Full House
print_poker_hand(poker_hands([12, 5, 13])) # High Card

# Sample Game
# p1 = Player(100)
# p2 = Player(100)
# r1 = Round([p1, p2])
#
# r1.deal()
# print r1
# print poker_hands(r1.river + p1.cards)
