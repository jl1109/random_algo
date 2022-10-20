import argparse
from dataclasses import dataclass
from enum import Enum
from random import randint
from typing import Dict, List

MAX_ATTEMPTS = 6

class word_hint(Enum):
    unknown = 0
    incorrect = 1
    wrong_pos = 2
    correct = 3

@dataclass
class word_attempt():
    word: str
    result: List[word_hint]

def get_attempt(charset: str, locked_chars: dict) -> str:
    indices = [randint(0, len(charset) - 1) for _ in range(5)]
    word = ''
    for i in range(5):
        if i in locked_chars:
            word += locked_chars[i]
        else:
            word += charset[indices[i]]
    return word

def test_solution(test: str, solution: str) -> List[word_hint]:
    # Create a list of only correct/not-in-word hints
    result = [word_hint.correct if test[i] == solution[i] \
        else word_hint.incorrect \
            for i in range(0, len(solution))]

    # Change not-in-word hints to wrong-position hints if needed
    for i, (c, h) in enumerate(zip(test, result)):
        if h is word_hint.correct:
            continue
        if c in solution:
            result[i] = word_hint.wrong_pos
    
    return result

def solve_wordle(solution: str, verbose: bool=False) -> word_attempt:
    # Create the initial list of possible characters
    charset = [chr(c) for c in range(ord('A'), ord('Z') + 1)]
    locked_chars: Dict[int, str] = {}
    history: List[word_attempt] = []

    # Solve for the solution
    for _ in range(MAX_ATTEMPTS):
        test = get_attempt(charset, locked_chars)
        result = test_solution(test, solution)
        history.append(word_attempt(test, result))

        for i, (c, h) in enumerate(zip(test, result)):
            # Remove characters from the charset that aren't in the solution
            if h == word_hint.incorrect and c in charset:
                charset.remove(c)
            elif h == word_hint.correct:
                locked_chars[i] = c

    if verbose:
        print('Full history:')
        for h in history:
            print(h)
    
    # Return the final attempt
    return history[len(history) - 1]

def main():
    parser = argparse.ArgumentParser(description='Solve a WORDLE problem.')
    parser.add_argument('--solution', type=str, required=True, help='The problem solution.')
    args = parser.parse_args()

    games = 100000
    successes = 0
    for _ in range(games):
        result = solve_wordle(args.solution, verbose=False)
        if result.word == args.solution:
            successes += 1
    print(f'Success rate over {games} games with {MAX_ATTEMPTS} attempts per game: {successes / games}%')

if __name__ == '__main__':
    main()