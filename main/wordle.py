import json, datetime, random
class Wordle:
    def __init__(self):
        time = datetime.time()
        date = datetime.date.today()
        self.date = str(date.day) + "-" + str(date.month) + "-" + str(date.year)
        self.hour = time.hour
        self.history = {}
        self.words = []
        self.minute = time.minute
        self.word = self.pick_word().lower()
    def pick_word(self):
        with open('./data/word_history.txt', 'r') as file:
            random_pick = random.randint(0, 499)
            for line in file:
                (k, v) = line.split()
                self.history[k] = v
            if not self.date in self.history:
                with open('./data/words.json') as f:
                    json_file = json.load(f)['words']
                    self.words = json_file
                    self.history[self.date] = json_file[random_pick]
                    with open('./data/word_history.txt', 'a') as fn:    
                        fn.write(self.date + " " + self.history[self.date] + "\n")
            return self.history[self.date]