from collections import defaultdict
from functools import reduce

import itertools
import math


def get_sum_dice_probabilities(count_dice=2):
    count_by_sum = defaultdict(int)
    total_throws = 6 ** count_dice

    for dice_roll in itertools.product(range(1, 7), repeat=count_dice):
        current_sum = sum(dice_roll)
        count_by_sum[current_sum] += 1
    return {k: v / total_throws for k, v in count_by_sum.items()}

def get_multiplication_probabilities(count_dice=2):
    count_by_multiplication = defaultdict(int)
    total_throws = 6 ** count_dice

    for dice_roll in itertools.product(range(1, 7), repeat=count_dice):
        current_multiplication = reduce(lambda x, y: x * y, dice_roll)
        count_by_multiplication[current_multiplication] += 1

    return {k: v / total_throws for k, v in count_by_multiplication.items()}

def get_multiplication_and_sum_probabilities(count_dice=2):
    multiplication_and_sum_probabilities = defaultdict(int)

    total_throws = 6 ** count_dice

    for dice_roll in itertools.product(range(1, 7), repeat=count_dice):
        current_multiplication = reduce(lambda x, y: x * y, dice_roll)
        current_sum = sum(dice_roll)
        multiplication_and_sum_probabilities[f"sum-{current_sum}:multiplication{current_multiplication}"] += 1

    return {k: v / total_throws for k, v in multiplication_and_sum_probabilities.items()}

def calculate_entropy(probabilities):
    entropy = 0
    for p in probabilities.values():
        entropy -= p * math.log2(p)
    return entropy

def main():
    ab = get_multiplication_and_sum_probabilities()
    entropy_ab = calculate_entropy(ab)

    a = get_sum_dice_probabilities()
    entropy_a = calculate_entropy(a)

    b = get_multiplication_probabilities()
    entropy_b = calculate_entropy(b)

    conditional_entropy_b = entropy_ab - entropy_a

    inf_b_in_a = entropy_b - conditional_entropy_b
    return list(map(lambda x: round(x, 2), [entropy_ab, entropy_a, entropy_b, conditional_entropy_b, inf_b_in_a]))

if __name__ == "__main__":
    res = main()
    print(res)