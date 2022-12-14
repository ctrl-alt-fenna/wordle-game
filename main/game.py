from wordle import Wordle
import importlib, json
# Main game class
wordle = importlib.import_module('wordle', '../wordle/wordle.py')
CORRECT = 1
PRESENT = 0
ABSENT = -1
class Game:
    def __init__(self, solver):
        self.wordle = Wordle()
        self.guesses = 0
        self.letter_guesses = {}
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
                guess = self.solver.find_choice(self.letter_guesses)
            else:
                guess = input('Guess a 5 letter word: \n')
            if len(guess) > 5 or len(guess) < 5:
                print('\n# # # # # \nINCORRECT WORD LENGTH\nWord must be 5 letters in length!\n# # # # # \n')
            if guess not in self.solver.words:
                self.running = False
                print('\n# # # # # \nUNKNOWN WORD \nWord is invalid English word and/or not found in game dictionary!\n# # # # # \n')
            else:
                print('\nYou guessed:\n', guess, sep='- ')
                correct = self.check_word(guess)
                # Word was guessed
                if correct:
                    print('You won! The word was ' + self.wordle.word)
                    self.running = False
                else:
                    print('\nIncorrect.')
                    print(self.letter_placements)
                        
                self.guesses += 1
    def check_word(self, guess):
        # Check if word is correct
        if guess.lower() == self.wordle.word:
            self.running = False
            return True
        # Check the letter placements
        else:
            ind = 0
            self.letter_placements = []
            for letter in guess.lower():
                # Letter is in word
                if self.wordle.word.lower().count(letter) > 0:
                    # Correct place
                    if self.wordle.word.lower().find(letter) == ind:
                        self.letter_placements.append('correct')    
                        type_place = (CORRECT, ind)
                    # Incorrect place
                    else:
                        type_place = (PRESENT, ind)
                        self.letter_placements.append('present')    
                # Letter is not in word 
                else:
                    type_place = (ABSENT, ind)
                    self.letter_placements.append('absent')    
                ind += 1
                self.letter_guesses[letter] = type_place

            return False
class Solver:
    def __init__(self):
        self.letter_count = {}
        self.word_probability = {}
        self.past_guesses = []
        self.words = []
        self.adapt_list = []
        self.startup()

    def startup(self):
        with open('./data/words.json') as f:
            self.words = json.load(f)['words']
        self.count_letters()
        self.adapt_list = self.words
        self.game = Game(self)
        for word in self.words:
            self.word_probability[word] = self.calc_probability(word)
        self.word_probability = self.sort_dict(list(self.word_probability.items()))
        self.game.play()
    '''
        Method to count letter-occurunces in main word list
    '''
    def count_letters(self):
        for word in self.words:
            for letter in word:
                if letter in self.letter_count:
                    self.letter_count[letter] += 1
                else:
                    self.letter_count[letter] = 1
        self.letter_count = self.sort_dict(list(self.letter_count.items()))

    def sort_dict(self, dict_list):
        for item in range(0, len(dict_list)-1):
            for neighbour in range(item + 1, len(dict_list)):
                if dict_list[item][1] < dict_list[neighbour][1]:
                    temp = dict_list[item]
                    dict_list[item] = dict_list[neighbour]
                    dict_list[neighbour] = temp
        return dict(dict_list)

    def calc_probability(self, word):
        total = 0
        for letter in word:
            # Check if letter was guessed
            if letter in self.game.letter_guesses.keys():
                total += (self.letter_count[letter] / (5 * len(self.words)))
                if self.game.letter_guesses[letter] == CORRECT:
                    total *= 4
                elif self.game.letter_guesses[letter] == PRESENT:
                    total *= 2
                else:
                    total /= 2
            else:
                # Initial guess: prioritise common letters that appear only once
                total += (self.letter_count[letter] / (5 * len(self.words)))
                if (word.count(letter) > 1):
                    total /= 2
        return total

    def find_choice(self, letter_guesses):
        letters = list(letter_guesses.keys())
        positions = list(letter_guesses.values())
        # 'a': (CORRECT,0)
        if len(letter_guesses) != 0:
            l = []
            for item in range(len(positions)):
                for word in self.adapt_list:
                    # Correct letter and position
                    if positions[item][0] == CORRECT:
                        # Check if word has letter and if it is in same place
                        if word.count(letters[item]) > 0 and word not in l:
                            l.append(word)
                        # Check if any words in current list do not contain the correct letter
                        elif word.count(letters[item]) == 0 and word in l:
                            l.remove(word)

                    # Present but wrong position
                    elif positions[item][0] == PRESENT:
                        # Check if word has letter and in different place
                        if word.count(letters[item]) > 0 and word not in l:
                            l.append(word)
                        # Check if any words in current list have letter in same location or not at all
                        for w in l:
                            if w.count(letters[item]) == 0:
                                l.remove(w)
                        # Absent
                    elif positions[item][0] == ABSENT:
                        # Remove all instances with this letter currently in l
                        for w in l:
                            if w.count(letters[item]) > 0:
                                l.remove(w)
            # Final check to remove any impossible guesses
            for i in range(len(letters)):
                if positions[i][0] == 0:
                    for word in l:
                        if word.find(letters[i]) == positions[i][1]:
                            l.remove(word)
                if positions[i][0] == -1:
                    for word in l:
                        if word.count(letters[i]) > 0:
                            l.remove(word)
            self.word_probability = {}
            self.adapt_list = l
            for word in self.adapt_list:
                self.word_probability[word] = self.calc_probability(word)
            self.word_probability = self.sort_dict(list(self.word_probability.items()))
        self.past_guesses.append(list(self.word_probability.keys())[0])
        return list(self.word_probability.keys())[0]
def main():
    solver = Solver()
if __name__ == "__main__":
    main()
