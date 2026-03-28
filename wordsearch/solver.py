"""
Solver class for running strategies and comparing performance.
"""

from typing import List
from .strategy import Strategy, SolutionResult
from .generator import Wordsearch


class Solver:
    """
    Solver class that runs a strategy on a word search and collects metrics.
    
    This class acts as a wrapper that:
    - Validates inputs
    - Executes the strategy
    - Collects and returns results
    - Provides easy comparison between strategies
    """
    
    def __init__(self, wordsearch: Wordsearch, strategy: Strategy):
        """
        Initialize solver with a word search and strategy.
        
        Args:
            wordsearch: The Wordsearch puzzle to solve
            strategy: The Strategy to use for solving
        """
        self.wordsearch = wordsearch
        self.strategy = strategy
    
    def run(self) -> SolutionResult:
        """
        Execute the strategy and return results.
        
        Returns:
            SolutionResult with found words and performance metrics
        """
        return self.strategy.solve(self.wordsearch)
    
    def run_and_display(self) -> SolutionResult:
        """
        Execute the strategy, print results, and return them.
        
        Returns:
            SolutionResult with found words and performance metrics
        """
        print(f"\n{'='*60}")
        print(f"Running: {self.strategy.get_name()}")
        print(f"Puzzle size: {self.wordsearch.size}×{self.wordsearch.size}")
        print(f"Words to find: {len(self.wordsearch.word_bank)}")
        print(f"{'='*60}\n")
        
        result = self.run()
        
        print(result)
        print(f"\n{'='*60}\n")
        
        return result


def compare_strategies(wordsearch: Wordsearch, strategies: List[Strategy]) -> List[SolutionResult]:
    """
    Run multiple strategies on the same puzzle and compare results.
    
    Args:
        wordsearch: The puzzle to solve
        strategies: List of strategies to compare
        
    Returns:
        List of SolutionResults, one per strategy
    """
    results = []
    
    print(f"\n{'#'*60}")
    print(f"COMPARING {len(strategies)} STRATEGIES")
    print(f"Puzzle: {wordsearch.size}×{wordsearch.size} with {len(wordsearch.word_bank)} words")
    print(f"{'#'*60}")
    
    for strategy in strategies:
        solver = Solver(wordsearch, strategy)
        result = solver.run_and_display()
        results.append(result)
    
    # Print comparison summary
    print(f"\n{'='*60}")
    print("COMPARISON SUMMARY")
    print(f"{'='*60}")
    print(f"{'Strategy':<25} {'Found':<10} {'Time (s)':<12} {'Cells':<15}")
    print(f"{'-'*60}")
    
    for result in results:
        print(f"{result.strategy_name:<25} "
              f"{result.words_found_count}/{result.total_words:<8} "
              f"{result.execution_time:<12.4f} "
              f"{result.cells_examined:<15,}")
    
    print(f"{'='*60}\n")
    
    return results
