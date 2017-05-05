#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import random as rn

original_deck = [x for x in range(0,52)]
suites = "Diamonds Clubs Hearts Spades".split()
# suites = "♦ ♣ ♥ ♠".split()
royal_cards = {9: "Jack", 10 : "Queen", 11: "King", 12 : "Ace"}
hand_rankings = {
    'Straight-Flush': 8,
    '4-of-a-kind': 7,
    'Full-House': 6,
    'Flush': 5,
    'Straight': 4,
    '3-of-a-kind': 3,
    '2-of-a-kind': 2,
    'High-Card': 1,
}
rankings_to_string = dict(zip(hand_rankings.values(), hand_rankings.keys()))

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

def print_poker_hands(hands):
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

def best_hand_to_string(hand):
    h = hand[1]
    if h[0] == 1:
        return "{0}.".format(rankings_to_string[h[0]])
    else:
        return "{0}.".format(rankings_to_string[h[0]])

def rank_poker_hands(hands):
    """Accepts poker hands generated by poker_hands(...). Returns a list of tuples. This list is sorted! These tuples represent
    the ranking of each player's hands. The first element in the tuple is the "first-level" of the ranking system,
    and represents the rank of the poker hand based on its type, (e.g 3-kind, fullhouse, straight, flush). The second
    element in this tuple is the secondary level of the ranking system which is used to determine what hand is better
    within the same type of poker hand. So, this lets us determine which two-of-a-kind is better in a tie. This second
    element is simply the sum of all of the face values of the cards that make up this hand."""
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
    returns winning percentage. Plan to implement future hand possibilites after current best hand"""

    hand = p_hand + river
    hand_list = [x % 13 for x in hand]
    num_of_cards = len(hand)

    hand_rank = sum(hand_list)
    private_hand_rank = (p_hand[0] % 13) + (p_hand[1] % 13);  # low private cards or high private cards

    face_count = [[] for x in range(0, 13)]  # Store cards from the input into bins. They are divided by face value
    suite_count = [[] for x in range(0, 4)]

    rank_ordered = rank_poker_hands(poker_hands(hand))  # checking for ranked hands
    rank = rank_ordered[0][0]  # best hand currently

    twos = []
    threes = []
    straights = []
    flushes = []

	#DEBUG:
    #print(str([card_to_string(c) for c in hand]))

    # count suits in hand
    for card in hand:
        value, suite = (card % 13), (card // 13)
        face_count[value].append(card)
        suite_count[suite].append(card)

    for i in range(0, 4): # flush
        if len(suite_count[i]) == 5:
            fhand = ["Flush", suite_count[i]]
            flushes.append(fhand[1])
        elif len(suite_count[i]) > 5:
            for j in range(0, len(suite_count[i]) - 4 ):
                fhand = ["Flush", suite_count[i][j:j+5]]
                flushes.append(fhand[1])

    for index in range(0, 13): # Find n-pairs
        num = len(face_count[index])
        if num > 1:
            if num == 2:
                twos.append(face_count[index])
            if num == 3:
                threes.append(face_count[index])

    for i in range(0, (14 - 5)): # straight
        possible_straight = face_count[i:i+5]
        if all(c for c in possible_straight): # using implicitness of [] != True
            straights.append(sum(possible_straight, []))

    if (rank == 8): # Never will happen (one day maybe)
        percentage = .99
        return "{:.3f}".format(percentage)

    if (rank == 7):  # 4-of-a-kind
        percentage = .98
        return "{:.3f}".format(percentage)

    if (rank == 6):  # full house
        full_house_hand = twos[0] + threes[0]
        fhh_values = [x % 13 for x in full_house_hand]
        percentage = sum(fhh_values) / 58
        percentage = percentage/20 + .93
        return "{:.3f}".format(percentage)

    if (rank == 5):  # flush
        percentage = 0
        percentage = sum(flushes[0]) / 49

        if (num_of_cards == 5):
            percentage = percentage/5.65 + .66
        if (num_of_cards == 6):
            percentage = percentage/6 + .74
        if (num_of_cards == 7):
            percentage = percentage/6 + .74

        return "{:.3f}".format(percentage)

    if (rank == 4):  # straight
        straight_values = [x % 13 for x in straights[0]]
        percentage = sum(straight_values)/50 # 10+J+Q+K+Ace = 50 (value of straight)
        percentage = percentage/4.75 + .60
        return "{:.3f}".format(percentage)

    if (rank == 3):  # 3-of-a-kind
        percentage = 0

        if (threes[0][0] % 13) == 0:
            percentage = 2/36 # (value 2 / 36 total)
        else:
            percentage = (threes[0][0] % 13 * 3) / 36

        if (num_of_cards == 5):
            percentage = percentage/9 + .80
        if (num_of_cards == 6):
            percentage = percentage/4.5 + .60
        if (num_of_cards == 7):
            percentage = percentage/4.5 + .60
        return "{:.3f}".format(percentage)

    if (rank == 2):  # 2-pair
        if (rank_ordered[1][0] == 2):  # two 2-pairs

			# If 2 pairs detected
            if ((twos[1][0] % 13) == 0):
                percentage = (twos[0][0] % 13 + 1)/13
            elif ((twos[0][0] % 13) == 0):
                percentage = (twos[1][0] % 13 + 1)/13
            else:
                percentage = ((twos[0][0] % 13) + (twos[1][0] % 13)) / 26

			# Based on number of cards
            if (num_of_cards == 5):
                percentage = percentage/4 + .60
            if (num_of_cards == 6):
                percentage = percentage/2 + .40
            if (num_of_cards == 7):
                percentage = percentage/1.75 + .375
            return "{:.3f}".format(percentage)

        percentage = ((twos[0][0] % 13) / 13)

		# If 2 pairs detected
        if (percentage == 0):
            percentage = 1 / 13
		# Based on number of cards
        if (num_of_cards == 2): # Preflop
            percentage = percentage/2 + .50
        if (num_of_cards == 5): # Flop
            percentage = percentage/2 + .22
        if (num_of_cards == 6):
            percentage = percentage/3 + .20
        if (num_of_cards == 7):
            percentage = percentage/2 + .05
        return "{:.3f}".format(percentage)

    if (rank == 1):  # High Card
        percentage = (private_hand_rank / (13 * num_of_cards))  # checking highest card in private_hand
        percentage += (len(max(suite_count)) / 13) # flush detection
        if num_of_cards > 4: # after preflop
            percentage /= 2
        return "{:.3f}".format(percentage)


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

    def act(self, OPEN, pot, max_bet, current_bet, river, history):
        """ Player function to interact with the game. This function ought to return the action the
        player wants to take, up to and including the amount of money they want to bet. """
        best_hand = self.best_hand(river)[1]
        if OPEN:
            '''Available actions are RAISE, CALL, and FOLD'''
            if current_bet <= 15:
                return self.id, ["RAISE", 20]
            else:
                return self.id, ["CALL"]
        else:
            '''Available actions are BET, CHECK, and FOLD'''
            # FOLD if we only have a high card that's less than ~8
            if best_hand[0] == 1 and best_hand[1] < 9:
                return self.id, ["FOLD"]
            # If our hand is a 3-of-a-kind or better, make a BET
            elif best_hand[0] >= 2:
                return self.id, ["BET", 10*best_hand[0]]
            # Otherwise, we can check to see what comes next!
            else:
                return self.id, ["CHECK"]
    """
            # FOLD if we only have a high card that's less than ~8
            if float(win_percentage(self.cards, river)) <= .2:
                return self.id, ["FOLD"]
            # If our hand is a 3-of-a-kind or better, make a BET
            elif float(win_percentage(self.cards, river)) >= .8:
                return self.id, ["BET", 10*best_hand[0]]
            # Otherwise, we can check to see what comes next!
            else:
                return self.id, ["CHECK"]
    """


class Table:
    def __init__(self, players, debug=False):
        """Initialize a single round of the game. The cards start out as a fresh deck. River is empty."""
        self.debug = debug
        self.cards = original_deck
        self.river = []
        self.pot = 0
        self.ante = 10
        self.round_history = []
        self.turn = 0
        self.players = [p for p in players if p.chips >= self.ante] # Players, all ones without sufficient chips are filtered
        self.player_dict = {p.id : p for p in players} # All original players, indexed by their player ID

    def __str__(self):
        result = "Pot: {0}\nRiver: {1}\n".format(str(self.pot),self.print_river())
        for p in self.players:
            result += "P{0} Hand: {1}, Chips: {2}\n".format(p.id, str(p), p.chips)

        if self.debug:
            for p in self.players:
                result += "*P{0} Best Hand: {1}\n".format(p.id, best_hand_to_string(p.best_hand(self.river)))


        return result[:-1] # stripping last \n because i'm lazy

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
            if len(self.players) == 1:  # All but one players folded
                print("All other players folded!")
                print("Player {0} wins!".format(self.players[0].id))
                return [self.players[0].id]
            # DEBUG
            print("="*12)
            print(STAGES[self.turn])
            print("="*12)
            print(self)

            for p in self.players:
                print("P" + str(p.id) + " Win Probability: " + win_percentage(p.cards, self.river))

            # Players can only bet as many chips as the number of chips held by the player with the fewest chips
            max_bet = min(p.chips for p in self.players)
            moves = [] # History of moves
            OPEN = False
            player_bet = [None, 0] # Player bet is a tuple of (Player.ID, BET AMOUNT)
            player_raise = [None, 0]
            folded_players = []
            stage_history = []

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
                p_move = p.act(OPEN, self.pot, max_bet, 0, self.river, self.round_history)
                p_action = p_move[1]
                if p_action[0] == "BET":
                    if p_action[1] > max_bet: # Invalid bet, removing player
                        print("Player {0} made an invalid bet! Kicking from table".format(p.id))
                        folded_players.append(p)
                        p_move = (p.id, ["FOLD"]) # auto fold the player
                    else: # Otherwise, record the max bet so far
                        player_bet = (p.id, p_action[1]) if p_action[1] > player_bet[1] else player_bet
                elif p_action[0] == "FOLD":
                    print("Player " + str(p.id) + " has folded")
                    folded_players.append(p)
                elif p_action[0] == "CHECK":
                    pass
                else:
                    print(p_action)
                    print("Player {0} gave an invalid action! Kicking from table".format(p.id))
                    folded_players.append(p)
                    p_move = (p.id, ["FOLD"])  # auto fold the player

                moves.append(p_move) # Store the move a player makes

            # Filter out the players who folded
            self.players = [p for p in self.players if p not in folded_players]

            if len(self.players) == 0:
                print("All players folded! Splitting the spot amongst the players who folded last...")
                split_pot = self.pot / len(folded_players)
                for p in folded_players:
                    p.chips += split_pot
                return None

            folded_players.clear()

            OPEN = player_bet[0] != None

            stage_history = stage_history + moves
            print("Closed Pot History: {0}".format(stage_history))
            moves.clear()
            # At the end of the round, if a player made a bet, he/she must put their chips into the pot
            # if betting is open, we have to see if everyone calls/folds/raises.
            # RAISE round
            # -------------------
            if OPEN:
                print("Player(s) made bet(s)! Entering open pot round.")
                CLOSED = False
                while not CLOSED:
                    moves.clear()
                    for p in self.players:
                        # TODO: Fix up some of the problems that occur when all players fold
                        if len(self.players) == 1: # All but one players folded
                            print("Player" + int(p.id) + "wins!")
                            return p.id

                        p_move = p.act(OPEN, self.pot, max_bet, player_bet[1], self.river, self.round_history)
                        p_action = p_move[1]
                        if p_action[0] == "RAISE":
                            if p_action[1] > max_bet or p_action[1] <= player_bet[1]: # Invalid bet, removing player
                                print("Player {0} made an invalid bet! Kicking from table".format(p.id))
                                folded_players.append(p)
                            else: # Otherwise, record the bet if it's the minimum bet so far
                                player_raise = (p.id, p_action[1]) if player_raise[0] == None or p_action[1] < player_raise[2] else player_raise
                        elif p_action[0] == "FOLD":
                            folded_players.append(p)
                        elif p_action[0] == "CALL":
                            pass

                        moves.append(p_move) # Store the move a player makes

                    self.players = [p for p in self.players if p not in folded_players]
                    folded_players.clear()

                    CLOSED = all(m[1][0] == "CALL" or m[1][0] == "FOLD" for m in moves)
                    player_bet = player_raise if player_raise[0] != None else player_bet
                    stage_history = stage_history + moves
                    print("Open Pot History: {0}".format(moves))

                # At this point, all players have either called or folded to the current bet, so we can deduct all of
                # the chips from each player at this point
                for p in self.players:
                    if player_bet[1] > p.chips:
                        print("Player {0} is going all in with {1} chips!".format(p.id, p.chips))
                        self.pot += p.chips
                        p.chips = 0
                    elif p.chips == 0:
                        print("Player {0} is already all-in!".format(p.id))
                    else:
                        self.pot += player_bet[1]
                        p.chips -= player_bet[1]
            # END OPEN round

            # At this point, all players have called. We're ready to deduct bets
            # print("STAGE HISTORY: {0}".format(str(stage_history)))
            self.round_history.append((STAGES[self.turn], stage_history))
            self.add_to_river()

            if self.turn == 0:
                self.add_to_river()
                self.add_to_river()

            self.turn += 1

        p_hands = [p.best_hand(self.river) for p in self.players]
        winners = compare_hands(p_hands)
        print("=" * 12)
        print("GAME OVER!")
        if len(winners) == 1:
            print("Player {0} won".format(self.player_dict[winners[0]].id))
        else:
            print("Players {0} tied".format(", ".join(str(pid) for pid in winners)))

        print("=" * 12)
        print("GAME HISTORY: \n{0}".format("\n".join(str(stage) for stage in self.round_history)))
        print("=" * 12)

        return winners


# Testing Poker Hands detection
# print_poker_hands(poker_hands([0, 0+13, 0+26, 0+39, 1])) # 4-of-a-kind
# print_poker_hands(poker_hands([0, 0+13, 0+26, 2, 1])) # 3-of-a-kind
# print_poker_hands(poker_hands([0, 0+13, 3, 4, 1])) # 2-of-a-kind
# print_poker_hands(poker_hands([0, 2+13, 2, 4+13, 4])) # Two 2-of-a-kind's
# print_poker_hands(poker_hands([12, 5, 13])) # High Card with Ace
# print_poker_hands(poker_hands([12, 0, 1, 2, 3+13])) # Straight with an Ace
# print_poker_hands(poker_hands([0,1,2,3,5])) # Flush of Diamonds
# print_poker_hands(poker_hands([4+26, 2+13, 2, 4+13, 4])) # Full House


# Testing Poker Hand comparisons
# print(compare_ranks(poker_hands([0,1,2,3,4]), poker_hands([0,1,2,3,4]))) # Tied Straights
# print(compare_ranks(poker_hands([1,2,3,4,5]), poker_hands([0,1,2,3,4]))) # Better Straight, p1 wins
# print(compare_ranks(poker_hands([1,2,3,4,5]), poker_hands([2,3,4,5,6]))) # Better Straight, p2 wins
# print(compare_ranks(poker_hands([2,2,3]), poker_hands([2,2,3]))) # Same two-pair, same high card
# print(compare_ranks(poker_hands([2,2,4]), poker_hands([2,2,3]))) # Same two-pair, p1 higher card
# print(compare_ranks(poker_hands([2,2,3]), poker_hands([2,2,5]))) # Same two-pair, p2 high card
# print(compare_ranks(poker_hands([0,2,4,6,8]), poker_hands([0,2,4,6,8]))) # Tied flush
# print(compare_ranks(poker_hands([0,2,4,6,10]), poker_hands([0,2,4,6,8]))) # p1 better flush
# print(compare_ranks(poker_hands([0,2,4,6,8]), poker_hands([0,2,4,6,10]))) # p2 better flush
# print(compare_ranks(poker_hands([3,3,3]), poker_hands([3,3+13,3+26]))) # Tied 3-of-a-kind
# print(compare_ranks(poker_hands([4,4+13,4+26]), poker_hands([3,3+13,3+26]))) # p1 better 3-of-a-kind
# print(compare_ranks(poker_hands([4,4+13,4+26]), poker_hands([5,5+13,5+26]))) # p2 better 3-of-a-kind
# print(compare_ranks(poker_hands([2, 2+13, 4+13, 4]), poker_hands([2, 2+13, 4+13, 4]))) # Tied two 2-pairs
# print(compare_ranks(poker_hands([3, 3+13, 4+13, 4]), poker_hands([2, 2+13, 4+13, 4]))) # p1 better two 2-pairs
# print(compare_ranks(poker_hands([2, 2+13, 4+13, 4]), poker_hands([2, 2+13, 5+13, 5]))) # p2 better two 2-pairs
# print(compare_ranks(poker_hands([10, 9]), poker_hands([5, 10]))) # p1 wins, second highest card

# Testing Winning Percentage Based on Hand and River Cards
# print(win_percentage([1, 31], [2, 5, 7])) # Three 2-pairs
# print(win_percentage([1, 31], [14, 8, 27])) # 3-of-a-kind
# print(win_percentage([1, 2], [3, 17, 18])) # Straight
# print(win_percentage([1, 3], [5, 7, 9])) # Flush
# print(win_percentage([1, 4], [14, 17, 30])) # Full House
# print(win_percentage([1, 14], [27, 40, 9])) # 4-of-a-kind
# print(win_percentage([1, 2], [3, 4, 5])) # Straight-Flush

# Sample Game
p1 = Player(1, 1000)
p2 = Player(2, 1000)
p3 = Player(3, 1000)
t1 = Table([p1, p2, p3], debug=True)
t1.play()
