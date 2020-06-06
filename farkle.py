import random

END_SCORE = 10000
TOTAL_DICE = 6
SCORING_DICE = {1: 100, 5:50}

class Game():
    def __init__(self, num_players):
        self.num_players = num_players
        self.turns = range(0, num_players)
        self.scores = [0] * num_players

    def is_done(self):
        for score in self.scores:
            if score >= END_SCORE:
                return True
        return False

    def play(self):
        while not self.is_done():
            for player in self.turns:
                # TODO if player 1 wins, player 2 gets an extra turn
                self.take_turn(player)

    def take_turn(self, player):
        print("-----------")
        print("Start Turn for player index {}".format(player))
        t = Turn()
        t.iterate_turn()

        self.scores[player] += t.score
        print("End of Turn")
        print("Current Scores")
        print(self.scores)

def roll_dice(num_dice):
    result = []
    for die in range(num_dice):
        result.append(random.randint(1,6))
    return sorted(result)

def score_duplicates(copies, array):
    score = 0
    for value in copies:
        count = array.count(value)
        score += value * count * 100
    return score

def get_duplicates(array):

    if len(array) <3:
        return [0, None]

    current_for_comparison = array[0]
    count = 1
    copies = set()

    for elt in array[1:]:
        if elt == current_for_comparison:
            count +=1
        else:
            current_for_comparison = elt
            count = 1
        if count >= 3:
            copies.add(elt)

    if bool(copies):
        score = score_duplicates(copies, array)
        results = [elt for elt in array if elt not in copies]

    else:
        score = 0
        results = None

    # TODO if 2 triplets, 0 dice to reroll -> farkle, when it should reroll all 6
    return [score, results]

class List_of_Results():
    def __init__(self, num_dice):
        self.results = roll_dice(num_dice)
        self.scoring_dictionary = SCORING_DICE

    def score(self):
        score = 0
        num_dice_to_reroll = 0

        res = get_duplicates(self.results)
        if res[1]:
            self.results = res[1]
        score += res[0]

        for die in self.results:
            if die in self.scoring_dictionary.keys():
                score += self.scoring_dictionary[die]
            else:
                num_dice_to_reroll+=1
        return [score, num_dice_to_reroll]

class Turn():
    def __init__(self):
        self.this_turn = True
        self.score = 0
        self.num_dice = TOTAL_DICE

    def iterate_turn(self):
        while self.this_turn:
            l = List_of_Results(self.num_dice)
            print(l.results)
            r = l.score()
            s = r[0]
            self.num_dice = r[1]
            if s == 0:
                self.this_turn = False
                self.score = 0
                print("Farkle!")
            else:
                print("Current score for this round: " + str(self.score))
                print("Score obtained with this roll: " + str(s))
                text_input = input("Continue or bank total " + str(self.score + s) + "?: ")
                self.this_turn = text_input == "Continue" or text_input == "c"
                self.score += s

def play_game():
    # num_players = int(input('Enter number of players: '))
    num_players = 2

    g = Game(num_players)

    g.play()

    print("Someone won!")

play_game()
