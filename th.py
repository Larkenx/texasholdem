#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import random as rn

original_deck = [x for x in range(0,52)]
suites = "Diamonds Clubs Hearts Spades".split()
# suites = "♦ ♣ ♥ ♠".split()
royal_cards = {9: "Jack", 10 : "Queen", 11: "King", 12 : "Ace"}

def card_to_string(index):
    """Converts a single card index to a string representation with suite and face value"""
    value = (index % 13)
    face = str(value+2) if value not in royal_cards else royal_cards[value]
    suite = suites[(index // 13)]
    return "{0} of {1}".format(face, suite)
    # return "{0}{1}".format(face, suite)

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
    twos = []
    threes = []
    straights = []  # it's possible to have more than one...
    flushes = []  # same as above
    straight_flushes = [] # super unlikely...but same as above

    for c in cards:  # Go through every card and record the number of times each one occurs
        value, suite = (c % 13), (c // 13)
        face_count[value].append(c)
        suite_count[suite].append(c)

    for s in range(0,4):
        suite_count[s] = sorted(suite_count[s])

    for index in range(0, 13): # Find n-pairs
        num_of_cards = len(face_count[index])
        if num_of_cards > 1:
            hand = ["{0}-of-a-kind".format(num_of_cards), face_count[index]]
            if num_of_cards == 2:
                twos.append(face_count[index])
            if num_of_cards == 3:
                threes.append(face_count[index])

            poker_hands.append(hand)

    for i in range(0, 4): # flush
        if len(suite_count[i]) == 5:
            hand = ["Flush", suite_count[i]]
            poker_hands.append(hand)
            flushes.append(hand[1])
        elif len(suite_count[i]) > 5:
            for j in range(0, len(suite_count[i]) - 4 ):
                hand = ["Flush", suite_count[i][j:j+5]]
                poker_hands.append(hand)
                flushes.append(hand[1])

    # Special case for straights is that the Ace can sometimes count as a '1' for a straight!
    ace = face_count[12] # Get the face_count of the Ace
    possible_straight = [ace] + face_count[0:4]
    if all(c for c in possible_straight):
        poker_hands.append(["Straight", sum(possible_straight, [])])
        straights.append(sum(possible_straight, []))

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

    # Full House
    if twos and threes:
        for pair in twos:
            for three in threes:
                poker_hands.append(["Full-House", pair + three])

    # Every hand has a "high card" which may be used as a tie-breaker, particularly if the poker hands
    # above are as a result of poker hands from the river cards.
    for c in cards:
        poker_hands.append(["High-Card", [c]])

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

def rank_poker_hands(hands):
    """Accepts poker hands generated by poker_hands(...). Returns a list of tuples. This list is sorted! These tuples represent
    the ranking of each player's hands. The first element in the tuple is the "first-level" of the ranking system,
    and represents the rank of the poker hand based on its type, (e.g 3-kind, fullhouse, straight, flush). The second
    element in this tuple is the secondary level of the ranking system which is used to determine what hand is better
    within the same type of poker hand. So, this lets us determine which two-of-a-kind is better in a tie. This second
    element is simply the sum of all of the face values of the cards that make up this hand."""
    hand_rankings = {
        'Straight-Flush' : 8,
        '4-of-a-kind' :7,
        'Full-House' :6,
        'Flush' :5,
        'Straight':4,
        '3-of-a-kind':3 ,
        '2-of-a-kind':2,
        'High-Card':1,
    }

    ranked_hands = []

    for h in hands:
        first_rank = hand_rankings[h[0]]
        second_rank = sum([c % 13 for c in h[1]], 0)
        ranked_hands.append((first_rank, second_rank))

    return sorted(ranked_hands, key=lambda x: (-x[0], -x[1]))

def compare_hands(player_hands):
    """Accepts a list of tuples, where each tuple is a player ID (number) players' submitted best hands.
    Returns the player ID of the best hand. If there are ties, then it will return a list of player ID's that tied"""

    def compare_two(h1,h2):
        if h1[0] == h2[0]:
            # Check to see which hand is better
            if h1[1] > h2[1]: # First hand is better
                return 1

            if h1[1] < h2[1]: # Second hand is better
                return -1

            return 0

        # not the same type of hand, so one is strictly better than the other
        elif h1[0] > h2[0]: # p1 has the better hand
            return 1
        else:
            return -1 # p2 has the better hand

    best_so_far = [-1,-1]
    tied_players = []
    for pid, h in player_hands:
        comparison_result = compare_two(h, best_so_far)
        if comparison_result == 0: # This hand ties the previous best hand
            tied_players.append(pid)
        elif comparison_result == 1: # This hand is better than the prev best
            tied_players.clear() # Get rid of all the possibly tied players
            tied_players.append(pid)
            best_so_far = h # Set it to be the new best hand
        else: # This hand is worse than the best hand, so this player 'loses'
            pass

    return tied_players

# DEPRECATED
def compare_ranks(p1_hand, p2_hand):
    """Determines which player holds a better poker hand. Accepts input args from the poker_hands(...) fn.
    Outputs 1 for p1 better hand, -1 for p2 better hand, or 0 for tie.

    NOTE: This function is sort of deprecated since we only care about best hands
    """
    r1 = rank_poker_hands(p1_hand)
    r2 = rank_poker_hands(p2_hand)
    # iterate through every ranked tuple in both players...
    for i in range(0, min(len(r1), len(r2))):
        h1 = r1[i]
        h2 = r2[i]
        # Same type of poker hand
        if h1[0] == h2[0]:
            # Check to see which hand is better
            if h1[1] > h2[1]: # First hand is better
                return 1

            if h1[1] < h2[1]: # Second hand is better
                return -1

        # not the same type of hand, so one is strictly better than the other
        elif h1[0] > h2[0]: # p1 has the better hand
            return 1
        else:
            return -1 # p2 has the better hand

    return 0

""" Probability Outline:
	1) Check if you have a rank hand
	        If so: a) rank = certain hard percentage
				   b) what is value or highest value of ranked hand? (pairs of 3 = 3 | straight = [0, 1, 2, 3, 4] = 4)
				   c) depending on rank, check how many cards are made up by the river
				       *to see possiblility of another player having similar hand*

	2) Check how close you are to having straight/flush if you do not have ranked hand
		a)
		b) check each suit total (ex. 4 hearts - close - higher percentage)
		c) check possibility of straight (ex. 1, 2, 4, 5 - missing one card - higher percentage) """

def win_percentage(p_hand, river):
    """Determines probability of winning based ONLY ON current player's best hand
    returns winning percentage"""
    hand_probabilities = { # Total Frequency: 2,598,960
        'Straight-Flush' : 0.00139, # 36 frequency
        '4-of-a-kind' : 0.0240, 	# 624
        'Full-House' : 0.1441, 		# 3744
        'Flush' : 0.1965, 			# 5108
        'Straight': 0.3925, 		# 10200
        '3-of-a-kind': 2.1128, 		# 54912
        '2-of-a-kind': 42.2569, 	# 1,098,240
    }

    hand = p_hand + river
    ordered = rank_poker_hands(poker_hands(hand))
    num_of_cards = len(hand)

    # print(ordered)
    rank = ordered[0][0]

    """
	TODO: Create function to find possibility
	"""

    if (rank == 7): # 4-of-a-kind
        return "4-of-a-kind Probability"

    if (rank == 6): # full house
        return "Full House Probability"

    if (rank == 5): # flush
        return "Flush Probability"

    if (rank == 4): # straight
        return "Straight Probability"

    if (rank == 3): # 3-of-a-kind
        return "3-of-a-kind Probability"

    if (rank == 2): # 2-pair
        if (ordered[1][0] == 2): # two 2-pairs
            return "2 2-Pairs Probability"
        return "2-Pair Probability"

    if (rank == 1): # High Card
        return "High Card Probability"

class Player:
    def __init__(self, id, chips):
        """Initialize the Player class with some initial chips and a unique ID. """
        self.chips = chips
        self.id = id
        self.cards = []
        self.rank = -1

    def __str__(self):
        """Return a string representation of the player. In our case this is just the cards the player
        has in their hand. """
        return str([card_to_string(c) for c in self.cards])

    def best_hand(self, river):
        """Given any list of cards, it deteremines the best hand to pull from the cards. Output is
        in the format of a tuple, first ele string name/id of the poker hand and second ele is the cards"""
        return self.id, rank_poker_hands(poker_hands(self.cards + river))[0]

    def act(self, OPEN, max_bet, current_bet, river, history):
        """ Player function to interact with the game. This function returns the player ID, and action a player
        wishes to take. The available actions to them are dependent on whether or not the pot is open or closed.
        
        TODO:
            -Add AI elements to determine what action a player should choose
            -Make the player actively check their hand with the river, and determine what percentile rank their hand is
            -Add functionality to read the history of previous moves to affect current action
        """
        if OPEN:
            if current_bet < 15:
                return self.id, ["RAISE", 20]
            else:
                return self.id, ["CALL"]
        else:
            return self.id, ["BET", 10]



class Table:
    def __init__(self, players):
        """Initialize a single round of the game. The cards start out as a fresh deck. River is empty."""
        self.cards = original_deck
        self.river = []
        self.pot = 0
        self.ante = 10
        self.round_history = []
        self.turn = 0
        self.players = [p for p in players if p.chips >= self.ante] # Players, all ones without sufficient chips are filtered
        self.player_dict = {p.id : p for p in players} # All original players, indexed by their player ID

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

    def deal_two(self):
        for p in self.players:
            p.cards = [self.random_card(), self.random_card()]

    def add_to_river(self):
        self.river.append(self.random_card())

    def play(self):
        """ This is the main game loop. It will go through each player and prompt them for an action until
        either the river has 5 cards or all but one player has folded. """
        STAGES = ["PREFLOP", "FLOP", "TURN", "RIVER"]
        # PREFLOP
        # -------
        self.deal_two()
        # Substract the ante from everyones' chips and add it to the pot. Our constructor for this class guarantees
        # every player has atleast enough to pay the ante
        for p in self.players:
            self.pot += self.ante
            p.chips -= self.ante

        # FLOP, TURN, RIVER
        # -----------------
        while len(self.river) <= 5:
            # DEBUG
            print("==========")
            print(STAGES[self.turn])
            print("----------")
            print(self)
            for p in self.players:
                print("P" + str(p.id) + " Win Probability: " + win_percentage(p.cards, self.river))

            # Players can only bet as many chips as the number of chips held by the player with the fewest chips
            max_bet = min(p.chips for p in self.players)
            moves = [] # History of moves
            OPEN = False
            player_bet = [None, 0] # Player bet is a tuple of (Player.ID, BET AMOUNT)
            folded_players = []

            # If not OPEN, then this is the an initial betting round and is said to be an CLOSED pot.
            # Stage 1 possible actions are CHECK, FOLD, and BET+AMT

            # If OPEN, then this is an OPEN pot and someone has already made a BET. Available actions are...
            # RAISE+AMT, FOLD, CALL.

            # Initial round for betting. If one player bets, the pot is said to be 'open' and continues
            # onto another round of raising/folding/calling. Available actions here are FOLD, CHECK, RAISE
            # -------------------------
            for p in self.players:
                # We pass the current state (CLOSED or OPEN pot to indicate valid actions) to the player. We also pass
                # the max bet that can be placed, and the current bet. In the closed round, this is 0. We also
                # pass the river and round history.
                p_move = p.act(OPEN, max_bet, 0, self.river, self.round_history)
                p_action = p_move[1]
                # Player chose to bet...
                if p_action[0] == "BET":
                    if p_action[1] > max_bet: # Invalid bet, removing player
                        print("Player {0} made an invalid bet! Kicking from table".format(p.id))
                        self.players.remove(p)
                        p_move = (p.id, ["FOLD"])
                    else: # Otherwise, record the max bet so far
                        OPEN = True
                        player_bet = (p.id, p_action[1]) if p_action[1] > player_bet[1] else player_bet

                # Player folded..
                if p_action[0] == "FOLD":
                    print("Player " + str(p.id) + " has folded")
                    folded_players.append(p)

                # Otherwise, a player must have checked!
                moves.append(p_move) # Store the move a player makes

            # Filter out the players who folded
            self.players = [p for p in self.players if p not in folded_players]

            if len(self.players) == 0:
                print("All players folded! Splitting the spot amongst the players who folded last...")
                split_pot = self.pot / len(folded_players)
                for p in folded_players:
                    p.chips += split_pot

                return None

            self.round_history = self.round_history + moves
            moves.clear()
            # At the end of the round, if a player made a bet, he/she must put their chips into the pot
            # if betting is open, we have to see if everyone calls/folds/raises.
            # RAISE round
            # -------------------
            if OPEN:
                # Deduct the last bet from the player who bet, and add it to the pot
                player_who_bet = self.player_dict[player_bet[0]]
                self.pot += player_bet[1]
                player_who_bet.chips -= player_bet[1]

                while not all(m[1][0] == "CALL" or m[1][0] == "FOLD" for m in moves):
                    moves.clear()
                    for p in self.players:
                        # TODO: Fix up some of the problems that occur when all players fold
                        if len(self.players) == 1: # All but one players folded
                            print("Player" + p.id + "wins!")
                            return p.id

                        p_move = p.act(OPEN, max_bet, player_bet[1], self.river, self.round_history)
                        p_action = p_move[1]
                        if p_action[0] is "RAISE":
                            if p_action[1] > max_bet or p_action[1] <= player_bet[1]: # Invalid bet, removing player
                                print("Player {0} made an invalid bet! Kicking from table".format(p.id))
                                self.players.remove(p)
                            else: # Otherwise, record the bet if it's the minimum bet so far
                                player_raise = (p.id, p_action[1]) if not player_raise or p_move[1] < player_raise[2] else player_raise
                        if p_action[0] is "FOLD":
                            self.players.remove(p)

                        moves.append(p_move) # Store the move a player makes

                    player_bet = player_raise
                    self.round_history = self.round_history + moves

                self.round_history.append(moves)
                for p in self.players:
                    p.chips -= player_bet
                    if p.chips >= 0:
                        self.pot += player_bet

            # At this point, all players have called. We're ready to deduct bets
            self.add_to_river()

            if self.turn == 0:
                self.add_to_river()
                self.add_to_river()

            self.turn += 1

        print("ROUND_HISTORY: \n" + str(self.round_history))
        p_hands = [p.best_hand(self.river) for p in self.players]
        winners = compare_hands(p_hands)
        return winners


# Testing Poker Hands detection
"""
print_poker_hand(poker_hands([0, 0+13, 0+26, 0+39, 1])) # 4-of-a-kind
print_poker_hand(poker_hands([0, 0+13, 0+26, 2, 1])) # 3-of-a-kind
print_poker_hand(poker_hands([0, 0+13, 3, 4, 1])) # 2-of-a-kind
print_poker_hand(poker_hands([0, 2+13, 2, 4+13, 4])) # Two 2-of-a-kind's
print_poker_hand(poker_hands([12, 5, 13])) # High Card with Ace
print_poker_hand(poker_hands([12, 0, 1, 2, 3+13])) # Straight with an Ace
print_poker_hand(poker_hands([0,1,2,3,5])) # Flush of Diamonds
print_poker_hand(poker_hands([4+26, 2+13, 2, 4+13, 4])) # Full House
"""

# Testing Poker Hand comparisons
"""
print(compare_ranks(poker_hands([0,1,2,3,4]), poker_hands([0,1,2,3,4]))) # Tied Straights
print(compare_ranks(poker_hands([1,2,3,4,5]), poker_hands([0,1,2,3,4]))) # Better Straight, p1 wins
print(compare_ranks(poker_hands([1,2,3,4,5]), poker_hands([2,3,4,5,6]))) # Better Straight, p2 wins
print(compare_ranks(poker_hands([2,2,3]), poker_hands([2,2,3]))) # Same two-pair, same high card
print(compare_ranks(poker_hands([2,2,4]), poker_hands([2,2,3]))) # Same two-pair, p1 higher card
print(compare_ranks(poker_hands([2,2,3]), poker_hands([2,2,5]))) # Same two-pair, p2 high card
print(compare_ranks(poker_hands([0,2,4,6,8]), poker_hands([0,2,4,6,8]))) # Tied flush
print(compare_ranks(poker_hands([0,2,4,6,10]), poker_hands([0,2,4,6,8]))) # p1 better flush
print(compare_ranks(poker_hands([0,2,4,6,8]), poker_hands([0,2,4,6,10]))) # p2 better flush
print(compare_ranks(poker_hands([3,3,3]), poker_hands([3,3+13,3+26]))) # Tied 3-of-a-kind
print(compare_ranks(poker_hands([4,4+13,4+26]), poker_hands([3,3+13,3+26]))) # p1 better 3-of-a-kind
print(compare_ranks(poker_hands([4,4+13,4+26]), poker_hands([5,5+13,5+26]))) # p2 better 3-of-a-kind
print(compare_ranks(poker_hands([2, 2+13, 4+13, 4]), poker_hands([2, 2+13, 4+13, 4]))) # Tied two 2-pairs
print(compare_ranks(poker_hands([3, 3+13, 4+13, 4]), poker_hands([2, 2+13, 4+13, 4]))) # p1 better two 2-pairs
print(compare_ranks(poker_hands([2, 2+13, 4+13, 4]), poker_hands([2, 2+13, 5+13, 5]))) # p2 better two 2-pairs
print(compare_ranks(poker_hands([10, 9]), poker_hands([5, 10]))) # p1 wins, second highest card
"""

# Testing Winning Percentage Based on Hand and River Cards
"""
win_percentage([1, 31], [2, 5, 7]) # Three 2-pairs
win_percentage([1, 31], [14, 8, 27]) # 3-of-a-kind
win_percentage([1, 2], [3, 17, 18]) # Straight
win_percentage([1, 3], [5, 7, 9]) # Flush
win_percentage([1, 4], [14, 17, 30]) # Full House
win_percentage([1, 14], [27, 40, 9]) # 4-of-a-kind
win_percentage([1, 2], [3, 4, 5]) # Straight-Flush
"""

# Sample Game
p1 = Player(1, 1000)
p2 = Player(2, 1000)
t1 = Table([p1, p2])
print(t1.play())
