# Texas Hold'em

1) Group Members: Steven Myers and Samuel Eleftheri

2) Responsibilities and Due Dates. 3 weeks until project is due.

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

3) Strategy

    - Come up with an API that can work with the template that we are given. It will be able to identify cards based on their number/index and use modulo arithmetic to determine suite/card value.

    - Make sure that all proper information is given from the Course API. If not, build a OOP approach for storing table/pot history.

    - Create ability to work with template in order to CALL, BET, or FOLD.

    - Create ability to identify different hands, e.g flush, royal flush, straight, pairs, full house, etc

    - Assign some kind of value to our current hand. Assign probabilistic values to other players' hands.

    - Compare the "value" or strength of our hand versus all other probabilistic hands - what's the probability that the others have a better hand than us?

    - fold if our hand is bad, call if our hand is ok,  bet if our hand is good

    - be able to call other players' bluffs. assign historical folding/betting to each player, and allow it to modify a player's propensity to bluff.
