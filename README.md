# Scrabble Character Mode Game (Python)

A simple Greek Scrabble-inspired game developed in Python.

## Features

- The player creates words using **uppercase Greek letters**.
- All playable Greek words are stored in the `greek7.txt` file.
- The game uses a **bag of Greek letter tiles** with different quantities and scores for each letter.
- The player can:
  - Create words using the available letters.
  - Exchange their letters.
  - Save an unfinished game and resume it later.
  - Quit an unfinished game and return to the main menu.
- The computer uses a **Smart-Fail algorithm** to choose its words.
- The results of completed games are saved in a **game history file**.

---

## Computer Algorithm - Smart-Fail

The computer searches for possible words that can be created using the letters in its current rack.

The algorithm:

1. Generates possible permutations of the available letters.
2. Checks whether each generated combination exists in `greek7.txt`.
3. Calculates the score of each valid word.
4. Sorts the valid words according to their score.
5. Uses a **softmax-based weighted random selection** to choose a word.

This means that the computer does not always choose the highest-scoring word. Higher-scoring words have a higher probability of being selected, while lower-scoring valid words can also be chosen.

---

## Object-Oriented Design

The project uses Object-Oriented Programming principles.
