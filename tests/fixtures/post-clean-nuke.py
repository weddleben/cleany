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


                                                              
                           
                                                              

def generate_samples(count: int) -> List[int]:
                                                                   
    samples = []

                                
    for _ in range(count):
                                               
        value = random.randint(LOWER_BOUND, UPPER_BOUND)
        samples.append(value)

                              
    return samples


                                                              
                         
                                                              

def compute_mean(values: List[int]) -> float:
                                          
    if not values:
        return 0.0

    return sum(values) / len(values)


def compute_std_dev(values: List[int]) -> float:
                                   
    if not values:
        return 0.0

    mean = compute_mean(values)

                              
    variance = sum((x - mean) ** 2 for x in values) / len(values)

                                      
    return math.sqrt(variance)


def find_extremes(values: List[int]) -> tuple[int, int]:
                                          
    if not values:
        return (0, 0)

    return (min(values), max(values))


                                                              
                         
                                                              

def filter_even(values: List[int]) -> List[int]:
                               
    return [v for v in values if v % 2 == 0]


def filter_above(values: List[int], threshold: int) -> List[int]:
                                                    
    return [v for v in values if v > threshold]


                                                              
                       
                                                              

def print_report(values: List[int]) -> None:
                                             
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

                                              
    if VERBOSE:
        print("Values:", values)
        print("Report complete! ✅✨")


                                                              
                       
                                                              

def main() -> None:
                                         

                                       
    samples = generate_samples(DEFAULT_SAMPLE_SIZE)

                                   
    evens = filter_even(samples)

                                             
    midpoint = (LOWER_BOUND + UPPER_BOUND) // 2
    high_values = filter_above(evens, midpoint)

                            
    print_report(high_values)


                                       
if __name__ == "__main__":
                                           
    main()