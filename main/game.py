from collections import Counter
import json

from wordle import Wordle

GREEN = 2
YELLOW = 1
GREY = 0
FEEDBACK_LABELS = {GREEN: 'green', YELLOW: 'yellow', GREY: 'grey'}
WORD_LENGTH = 5
SOLVED_PATTERN = sum(GREEN << (2 * index) for index in range(WORD_LENGTH))

'''
Give feedback about the correctness of a guess
'''

def feedback_code(guess, answer):
    guess = guess.lower()
    answer = answer.lower()

    feedback = [GREY] * WORD_LENGTH
    remaining = Counter(answer)

    for index, letter in enumerate(guess):
        if letter == answer[index]:
            feedback[index] = GREEN
            remaining[letter] -= 1
    
    # Account for double letters. If one is correctly guessed, mark the other one accordingly. 
    for index, letter in enumerate(guess):
        if feedback[index] != GREEN and remaining[letter] > 0:
            feedback[index] = YELLOW
            remaining[letter] -= 1

    return sum(state << (2 * index) for index, state in enumerate(feedback))


class Game:
    def __init__(self, solver):
        self.wordle = Wordle()
        self.guesses = 0
        self.letter_placements = []
        self.solver = solver
        self.words = self.solver.words
        self.usesolver = self.use_solver()
    def use_solver(self):
        result = input('Do you wish to use a solver? Y/N\n')
        while result.upper() != 'Y' and result.upper() != 'N':
            result = input('INCORRECT INPUT\nDo you wish to use a solver? Y/N\n')
        return result.upper() == 'Y'

    def play(self):
        self.running = True
        while self.running and self.guesses < 5:
            if self.usesolver:
                guess = self.solver.find_choice()
            else:
                guess = input('Guess a 5 letter word: \n')
            if len(guess) != WORD_LENGTH:
                print('\n# # # # # \nINCORRECT WORD LENGTH\nWord must be 5 letters in length!\n# # # # # \n')
                continue
            if guess not in self.solver.words:
                self.running = False
                print('\n# # # # # \nUNKNOWN WORD \nWord is invalid English word and/or not found in game dictionary!\n# # # # # \n')
            else:
                print('\nYou guessed:\n', guess, sep='- ')
                feedback = self.check_word(guess)
                if self.usesolver:
                    self.solver.update_candidates(guess, feedback)
                if feedback == SOLVED_PATTERN:
                    print('You won! The word was ' + self.wordle.word)
                    self.running = False
                else:
                    print('\nIncorrect.')
                    print(self.letter_placements)
                        
                self.guesses += 1
    def check_word(self, guess):
        feedback = feedback_code(guess, self.wordle.word)
        self.letter_placements = [
            FEEDBACK_LABELS[(feedback >> (2 * index)) & 3]
            for index in range(WORD_LENGTH)
        ]
        return feedback


class Solver:
    def __init__(self):
        self.past_guesses = []
        self.words = []
        self.adapt_list = []
        self.startup()

    def startup(self):
        with open('./data/words.json', 'r') as f:
            self.words = json.load(f)['words']
        self.adapt_list = self.words[:500]
        self.game = Game(self)
        self.game.play()

    def find_choice(self):
        if not self.adapt_list:
            raise RuntimeError('No possible answers remain; feedback is inconsistent.')

        candidates = set(self.adapt_list)
        best_guess = None
        best_key = None

        for guess in self.words:
            pattern_counts = {}
            for answer in self.adapt_list:
                pattern = feedback_code(guess, answer)
                pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1

            expected_remaining = sum(count * count for count in pattern_counts.values())
            ranking = (expected_remaining, guess not in candidates)
            if best_key is None or ranking < best_key:
                best_guess = guess
                best_key = ranking

        self.past_guesses.append(best_guess)
        return best_guess

    def update_candidates(self, guess, feedback):
        self.adapt_list = [
            answer for answer in self.adapt_list
            if feedback_code(guess, answer) == feedback
        ]


def main():
    solver = Solver()
if __name__ == "__main__":
    main()
