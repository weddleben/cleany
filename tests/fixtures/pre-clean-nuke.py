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

something:str = 'single quoted string'


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

def main() -> None:
    # Entry point for script execution 🎬✨

    # Step 1: Generate random samples 🎲
    samples = generate_samples(DEFAULT_SAMPLE_SIZE)

    # Step 3: Filter numbers above midpoint 🚀
    midpoint = (LOWER_BOUND + UPPER_BOUND) // 2


# Standard Python entry-point guard 🛡️✨
if __name__ == "__main__":
    # Execute main only when run directly 🎯
    main()