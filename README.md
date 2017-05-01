# Texas Hold'em
Information:
	Overall poker hand rankings table:

	1 - Royal Flush - [10, J, Q, K, A] Same Suit
	2 - Straight Flush - [3, 4, 5, 6, 7] Same Suit
	3 - Four of a kind - [2, J, J, J, J]
	4 - Full House - [2, 2, Q, Q, Q] (pair and three of kind)
	5 - Flush - [3, 6, 9, Q, K] Same Suit
	6 - Straight - [3, 4, 5, 6, 7]
	7 - Three of a kind - [4, 2, A, A, A]
	8 - Two pairs - [4, 8, 8, A, A]
	9 - Pair - [3, 6, 7, Q, Q]
	10 - High Card

	deck: [0...51]
	card = int
	ranking = int (poker ranking above represent hand)
	highcard = int


Overall Evaulating Idea:

	Royal flush / Straight flush / Flush (checking suits):
		1) Seperate suits:

	Pairs / # of a kind / Full house (not checking suits):
		1) Find pairs:
			create temp array
			var x = mod 13 on each card in hand and on table, push into temp
			pass through temp, counting each x
			if there is exactly 4 x's present, record x as var fok (four of kind) and remove x's
			if there is exactly 3 x's present, record x as var tok (three of kind) and remove x
			if there is exactly 2 x's present, add x to pairs array and remove x
				*if len(pairs) > 2, remove smallest number pair*
			once pairs removed, record highcard of whats left in temp.

		2) Check hand:
			if fok (four of kind) not None:
				ranking = 3, (use fok and highcard variables when comparing multiple four of kinds hands)
				return/break
			if (lens(pairs) >= 1) && tok not None:
				ranking = 4
				find highest number pair, assign to var pair (use vars pair and tok when comparing multiple full houses)
				return/break
			if tok not None:
				ranking = 7 (use variable tok and highcard when comparing multiple 3 of a kind hands)
				return/break
			if pairs not None (empty?):
				if lens(pairs) = 2:


	Set ranking while finding hands (unless if current ranking smaller than replacement)


Notes:
	Efficiency improvements can/will be made.

- Group Members: Steven Myers and Samuel Eleftheri

- Responsibilities and Due Dates. 3 weeks until project is due.

    First Week (4/10 - 4/16):
    - Get card identification working.
    - Identify possible hands.
    - Assign values to hands, determine if one hand is strictly better than another
    - Do some research on how likely or unlikely some combinations of hands are

    Second Week (4/17 - 4/24):
    - Start adapting our first week functions to work properly with the template. Successfully write some unit tests to receive cards from Course API and determine hands, and send responses.
    - Start to brainstorm and skeleton the algorithm/heuristic to determine best moves (call, bet, fold) based on card values.
    - Run some tests to make sure AI does the proper thing under right circumstances. Adjust as necessary.
    - Finalize bare-bones gameplay. Begin to create histories of other players. Come up with test suites to play against other players.

    Third Week ( 4/25 - 4/30):
    - Add in extra features. This includes alpha-beta search over probabilistic data. We assign percentile ranks or percentile chances of having "the best hand".
    - Add in a quick look up table of probabilities for cards. Peak ahead to see what the chances of better cards for us is.
    - Make risks based on the percentage of our chips/pots. Really conservative/safe play when chips are low, a little less so when we have lots of chips.

- Strategy

    - Come up with an API that can work with the template that we are given. It will be able to identify cards based on their number/index and use modulo arithmetic to determine suite/card value.

    - Make sure that all proper information is given from the Course API. If not, build a OOP approach for storing table/pot history.

    - Create ability to work with template in order to CALL, BET, or FOLD.

    - Create ability to identify different hands, e.g flush, royal flush, straight, pairs, full house, etc

    - Assign some kind of value to our current hand. Assign probabilistic values to other players' hands.

    - Compare the "value" or strength of our hand versus all other probabilistic hands - what's the probability that the others have a better hand than us?

    - fold if our hand is bad, call if our hand is ok,  bet if our hand is good

    - be able to call other players' bluffs. assign historical folding/betting to each player, and allow it to modify a player's propensity to bluff.
