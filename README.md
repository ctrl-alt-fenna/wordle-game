# Wordle Clone

A command-line Wordle-style game written in Python. You have five guesses to find a hidden five-letter word. After each guess, letters are marked green, yellow, or grey.

## Run

From the project directory, run:

```bash
python main/game.py
```

On Windows, you can also use `py main/game.py`. The game uses only the Python standard library.

Choose whether to play manually or use the built-in solver when prompted. In manual mode, enter a valid five-letter word from the game dictionary.

## Solver

The solver evaluates guesses by how they divide the remaining possible answers, then chooses a guess expected to leave fewer candidates. Its answer pool is the first 500 words in `data/words.json`.

## Data

- `data/words.json` contains the game's word list.
- `data/word_history.txt` stores the selected answer for each date so the daily word stays the same when the game is run again that day.

## Author

[Fenna Ransijn](https://www.github.com/ctrl-alt-fenna)