"""
Shorter demo Python file (~130 lines) with LOTS of comments 😄🔥
Many of the comments below intentionally contain emojis 🎉✨🐍
The rest are plain technical comments.
"""

import random
import math
from typing import List


DEFAULT_SAMPLE_SIZE = 25


LOWER_BOUND = 1


UPPER_BOUND = 50


VERBOSE = True

something: str = 'single quoted string'


def generate_samples(count: int) -> List[int]:

    samples = []

    for _ in range(count):
        value = random.randint(LOWER_BOUND, UPPER_BOUND)
        samples.append(value)

    return samples


def main() -> None:

    samples = generate_samples(DEFAULT_SAMPLE_SIZE)

    midpoint = (LOWER_BOUND + UPPER_BOUND) // 2


if __name__ == "__main__":
    main()
