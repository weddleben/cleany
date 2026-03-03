"""
Shorter demo Python file (~130 lines) with LOTS of comments 😄🔥
Many of the comments below intentionally contain emojis 🎉✨🐍
The rest are plain technical comments.
"""

import random
import math 
from typing import List


# ============================================================
# CONFIGURATION SECTION ⚙️🛠️
# ============================================================

# Default number of samples to generate 🎲
DEFAULT_SAMPLE_SIZE = 25

# Lower bound for random values 🔽
LOWER_BOUND = 1

# Upper bound for random values 🔼
UPPER_BOUND = 50

# Toggle verbose output 🗣️
VERBOSE = True


# ============================================================
# RANDOM DATA GENERATION 🎲✨
# ============================================================

def generate_samples(count: int) -> List[int]:
    # Generate a list of random integers within configured bounds 🎉
    samples = []

    # Loop exactly "count" times
    for _ in range(count):
        # Append a random integer to the list 🎯
        value = random.randint(LOWER_BOUND, UPPER_BOUND)
        samples.append(value)

    # Return completed list 📦✨
    return samples


# ============================================================
# STATISTICS FUNCTIONS 📊📈
# ============================================================

def compute_mean(values: List[int]) -> float:
    # Compute arithmetic mean of values 🧮✨
    if not values:
        return 0.0

    return sum(values) / len(values)


def compute_std_dev(values: List[int]) -> float:
    # Compute standard deviation 📉📐
    if not values:
        return 0.0

    mean = compute_mean(values)

    # Calculate variance first
    variance = sum((x - mean) ** 2 for x in values) / len(values)

    # Return square root of variance 🌿
    return math.sqrt(variance)


def find_extremes(values: List[int]) -> tuple[int, int]:
    # Return minimum and maximum values 🔎✨
    if not values:
        return (0, 0)

    return (min(values), max(values))


# ============================================================
# DATA FILTERING LOGIC 🚦🧹
# ============================================================

def filter_even(values: List[int]) -> List[int]:
    # Keep only even numbers 🧩✨
    return [v for v in values if v % 2 == 0]


def filter_above(values: List[int], threshold: int) -> List[int]:
    # Keep values strictly greater than threshold 🚀🔥
    return [v for v in values if v > threshold]


# ============================================================
# REPORTING FUNCTION 📝📣
# ============================================================

def print_report(values: List[int]) -> None:
    # Print a formatted statistical report 📊✨
    mean = compute_mean(values)
    std = compute_std_dev(values)
    minimum, maximum = find_extremes(values)

    print("----- REPORT -----")
    print(f"Count: {len(values)}")
    print(f"Mean: {mean:.2f}")
    print(f"Std Dev: {std:.2f}")
    print(f"Min: {minimum}")
    print(f"Max: {maximum}")
    print("------------------")

    # Extra flair if verbose mode is enabled 🎉
    if VERBOSE:
        print("Values:", values)
        print("Report complete! ✅✨")


# ============================================================
# MAIN PROGRAM ENTRY 🚀🐍
# ============================================================

def main() -> None:
    # Entry point for script execution 🎬✨

    # Step 1: Generate random samples 🎲
    samples = generate_samples(DEFAULT_SAMPLE_SIZE)

    # Step 2: Filter even numbers 🧹
    evens = filter_even(samples)

    # Step 3: Filter numbers above midpoint 🚀
    midpoint = (LOWER_BOUND + UPPER_BOUND) // 2
    high_values = filter_above(evens, midpoint)

    # Step 4: Print report 📊
    print_report(high_values)


# Standard Python entry-point guard 🛡️✨
if __name__ == "__main__":
    # Execute main only when run directly 🎯
    main()