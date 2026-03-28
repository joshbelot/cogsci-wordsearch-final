"""
Example usage and testing of word search strategies.
"""

from wordsearch.generator import WordsearchGenerator
from wordsearch.strategies import (
    BruteForceStrategy,
    OrderedSearchStrategy,
    UncommonLetterSearchStrategy,
    RandomSampleStrategy,
    PatchSearchStrategy,
    RandomToOrderedStrategy
)
from wordsearch.solver import Solver, compare_strategies


def main():
    # Generate a puzzle
    print("Generating word search puzzle...")
    generator = WordsearchGenerator()
    puzzle = generator.generate(size=10, min_word_length=4, max_word_length=8)
    
    print("\nGenerated Puzzle:")
    puzzle.display()
    
    # Test individual strategy
    print("\n" + "="*60)
    print("TESTING INDIVIDUAL STRATEGY")
    print("="*60)
    
    strategy = BruteForceStrategy()
    solver = Solver(puzzle, strategy)
    result = solver.run_and_display()
    
    # Compare all strategies
    print("\n" + "="*60)
    print("COMPARING ALL STRATEGIES")
    print("="*60)
    
    strategies = [
        BruteForceStrategy(),
        OrderedSearchStrategy(),
        UncommonLetterSearchStrategy(),
        RandomSampleStrategy(max_attempts=1000),
        PatchSearchStrategy(),
        RandomToOrderedStrategy(),
    ]
    
    results = compare_strategies(puzzle, strategies)
    
    print("\nAll strategies have been implemented and tested!")


if __name__ == "__main__":
    main()
