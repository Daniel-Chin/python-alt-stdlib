'''
Liwei's gamble with 语文课代表  
'''

import numpy as np
from math import comb
from functools import lru_cache

import numpy as np
from matplotlib import pyplot as plt
from tqdm import tqdm

N_QUESTIONS = 100
QUESTION_N_OPTIONS = 4

right_prob = 1 / QUESTION_N_OPTIONS
wrong_prob = 1 - right_prob

@lru_cache(maxsize=N_QUESTIONS ** 2)
def strategy(n_questions_diffused: int, exact_score: int):
    n_questions_to_guess = N_QUESTIONS - n_questions_diffused
    mean_score_from_guess = n_questions_to_guess * right_prob
    need_score = exact_score - mean_score_from_guess
    def constrain(x):
        x = min(x, n_questions_diffused)
        x = max(x, 0)
        return round(x)
    return constrain(need_score)

@lru_cache(maxsize=N_QUESTIONS * 10)
def winningChance(
    knowledge_coverage: float, exact_score: int, 
    subjective_exact_score: int, 
):
    n_questions_diffused = round(N_QUESTIONS * knowledge_coverage)
    n_questions_to_guess = N_QUESTIONS - n_questions_diffused
    guess_must_right = exact_score - strategy(
        n_questions_diffused, subjective_exact_score, 
    )
    if guess_must_right < 0:
        return 0
    guess_must_wrong = n_questions_to_guess - guess_must_right
    return (
        right_prob ** guess_must_right
        * wrong_prob ** guess_must_wrong
        * comb(n_questions_to_guess, guess_must_right)
    )

def verify_winningChance():
    print(f'{winningChance(1, 4, 4) = }')
    print(f'{winningChance(1, 75, 75) = }')
    print(f'{winningChance(0, 25, 25) = }')
    print(f'{winningChance(0, 20, 20) = }')
    print(f'{winningChance(0, 100, 100) = }')
    print(f'{winningChance(0.5, 100, 100) = }')
    print(f'{winningChance(0.9, 100, 100) = }')

def integrate(knowledge_coverage: float, score_range: slice):
    subjecive_aim = np.mean([*score_range])
    acc = 0.0
    for score in score_range:
        acc += winningChance(knowledge_coverage, score, subjecive_aim)
    return acc

def verify_integrate():
    print(f'{integrate(.8, range(70, 101)) = }')
    print(f'{integrate(.8, range(80, 101)) = }')
    print(f'{integrate(.8, range(85, 101)) = }')
    print(f'{integrate(.8, range(90, 101)) = }')
    print(f'{integrate(.8, range(95, 101)) = }')
    print(f'{integrate(.8, range(100, 101)) = }')
    print(f'{integrate(.95, range(85, 101)) = }')

def main():
    knowledge_coverage = np.linspace(0, 1, 101)
    liwei = []
    chinese_class_rep = []
    for kc in tqdm(knowledge_coverage):
        liwei            .append(integrate(kc, range(0, 4)))
        chinese_class_rep.append(integrate(kc, range(86, 101)))
    plt.plot(knowledge_coverage, liwei, label='Liwei')
    plt.plot(knowledge_coverage, chinese_class_rep, label='Chinese class rep')
    plt.legend()
    plt.xlabel('Knowledge coverage')
    plt.ylabel('Success probability')
    plt.show()

main()
# verify_integrate()
