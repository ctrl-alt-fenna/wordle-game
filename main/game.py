from wordle import Wordle
import os
# Main game class
class Game:
    def __init__(self):
        self.wordle = Wordle()
        self.guess = 0
        self.letter_guesses = {}
        self.letter_placements = []
    def play(self):
        self.running = True
        while self.running and self.guess < 5:
            answer = {} 
            guess = input('Make a guess:\n')
            if len(guess) > 5 or len(guess) < 5:
                print('\n# # # # # \nINCORRECT WORD LENGTH\nWord must be 5 letters in length!\n# # # # # \n')
                self.play()
            if guess not in self.wordle.words:
                print('\n# # # # # \nUNKNOWN WORD \nWord is invalid English word and/or not found in game dictionary!\n# # # # # \n')
                self.play()
            else:
                correct = self.check_word(guess)
                ind = 0
                # Word wasn't guessed
                if not correct:
                    for placement in self.letter_placements[self.guess]:
                        if placement == 'correct':
                            answer[guess[ind]] = '='
                        if placement == 'present':
                            answer[guess[ind]] = '+'
                        if placement == 'absent':
                            answer[guess[ind]] = '-'
                        ind += 1
                    print(answer)
                    self.guess += 1
                # Word was guessed
                else:
                    print('You won! The word was ' + self.wordle.word)
    def check_word(self, guess):
        # Check if word is correct
        if guess.lower() == self.wordle.word.lower():
            self.running = False
            return True
        # Check the letter placements
        else:
            ind = 0
            self.letter_placements.append(['', '', '', '', ''])
            for letter in guess.lower():
                placement = ''
                # Letter is in word
                if self.wordle.word.lower().count(letter) > 0:
                    # Correct place
                    if self.wordle.word.lower().find(letter) == ind:    
                        placement = 'correct'
                    # Incorrect place
                    else:
                        placement = 'present'
                    self.letter_guesses[letter] = 1 
                # Letter is not in word
                else:
                    placement = 'absent'
                self.letter_placements[self.guess][ind] = placement
                ind+=1
            return False
def main():
    game = Game()
    game.play()
if __name__ == "__main__":
    main()
