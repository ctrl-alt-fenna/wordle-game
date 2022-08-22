import json, datetime, random
class Wordle:
    def __init__(self):
        time = datetime.time()
        date = datetime.date.today()
        self.date = str(date.day) + "-" + str(date.month) + "-" + str(date.year)
        self.hour = time.hour
        self.words = {}
        self.minute = time.minute
        self.word = self.pick_word()
    def pick_word(self):
        with open('word_history.txt') as file:
            random_pick = random.randint(0, 499)
            needs_writing = False
            for line in file:
                (k, v) = line.split()
                self.words[k] = v
            if len(self.words) == 0:
                needs_writing = True
                with open('words.json') as f:
                    json_file = json.load(f)
                    json_file = json_file['words']
                    self.words[self.date] = json_file[random_pick]
            else:
                if self.words[self.date] != None:
                    needs_writing = False
                else:
                    needs_writing = True
            if needs_writing:
                for date in self.words:
                    file.write(date + " " + self.words[date] + "\n")
            return self.words[self.date]