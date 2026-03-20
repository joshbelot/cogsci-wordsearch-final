"""
Random to Ordered Strategy - Hybrid strategy that switches from random to systematic search.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
import random
from typing import Dict, List, Tuple
from Strategy import Strategy, SolutionResult, WordPosition
from Wordsearch_Generator import Wordsearch


class RandomToOrderedStrategy(Strategy):
    """
    Hybrid strategy that starts with random sampling and switches to ordered search.
    
    Algorithm:
    1. Phase 1 (Random): Try random positions and directions for a limited time
       - Similar to RandomSampleStrategy but with time limit per word
       - Quick wins for easy-to-find words
    2. Phase 2 (Ordered): If word not found within time limit, switch to systematic
       - Use OrderedSearchStrategy approach (horizontal → vertical → diagonal)
       - Guarantees finding remaining words
    
    This strategy models adaptive human behavior: starting with intuitive random
    attempts and falling back to systematic search when initial attempts fail.
    
    Parameters:
        random_time_limit: Seconds to spend on random search per word (default 0.001)
        max_random_attempts: Maximum random attempts per word (default 100)
        seed: Random seed for reproducibility
    
    Performance Characteristics:
    - Fast for puzzles with easy-to-find words
    - Graceful degradation: switches to systematic when random fails
    - Models human problem-solving: intuition first, then systematic
    - Balances speed (random) with completeness (ordered)
    """
    
    def __init__(self, random_time_limit: float = 0.001, 
                 max_random_attempts: int = 100,
                 seed: int = None):
        """
        Initialize hybrid strategy.
        
        Args:
            random_time_limit: Time limit for random phase per word (seconds)
            max_random_attempts: Max random attempts per word
            seed: Random seed for reproducibility
        """
        super().__init__()
        self.random_time_limit = random_time_limit
        self.max_random_attempts = max_random_attempts
        self.seed = seed
        
        # Direction groups for ordered search phase
        self.HORIZONTAL_DIRECTIONS = [
            (0, 1),   # Left to right
            (0, -1),  # Right to left
        ]
        
        self.VERTICAL_DIRECTIONS = [
            (1, 0),   # Top to bottom
            (-1, 0),  # Bottom to top
        ]
        
        self.DIAGONAL_DIRECTIONS = [
            (1, 1),   # Top-left to bottom-right
            (1, -1),  # Top-right to bottom-left
            (-1, 1),  # Bottom-left to top-right
            (-1, -1), # Bottom-right to top-left
        ]
    
    def get_name(self) -> str:
        return "Random to Ordered"
    
    def _try_random_search(self, grid: List[List[str]], word: str, size: int) -> tuple:
        """
        Try to find word using random search within time/attempt limits.
        Returns (found, position) tuple.
        """
        phase_start = time.time()
        attempts = 0
        
        while attempts < self.max_random_attempts:
            # Check time limit
            if time.time() - phase_start > self.random_time_limit:
                return (False, None)
            
            # Random position and direction
            row = random.randint(0, size - 1)
            col = random.randint(0, size - 1)
            direction = random.choice(self.DIRECTIONS)
            
            if self._check_word_at_position(grid, word, row, col, direction):
                dr, dc = direction
                end_row = row + dr * (len(word) - 1)
                end_col = col + dc * (len(word) - 1)
                
                position = WordPosition(
                    word=word,
                    start_row=row,
                    start_col=col,
                    end_row=end_row,
                    end_col=end_col,
                    direction=direction
                )
                return (True, position)
            
            attempts += 1
        
        return (False, None)
    
    def _try_ordered_search(self, grid: List[List[str]], word: str, size: int) -> tuple:
        """
        Find word using systematic ordered search.
        Returns (found, position) tuple.
        """
        # Group directions: horizontal, then vertical, then diagonal
        direction_groups = [
            self.HORIZONTAL_DIRECTIONS,
            self.VERTICAL_DIRECTIONS,
            self.DIAGONAL_DIRECTIONS
        ]
        
        for direction_group in direction_groups:
            for direction in direction_group:
                for row in range(size):
                    for col in range(size):
                        if self._check_word_at_position(grid, word, row, col, direction):
                            dr, dc = direction
                            end_row = row + dr * (len(word) - 1)
                            end_col = col + dc * (len(word) - 1)
                            
                            position = WordPosition(
                                word=word,
                                start_row=row,
                                start_col=col,
                                end_row=end_row,
                                end_col=end_col,
                                direction=direction
                            )
                            return (True, position)
        
        return (False, None)
    
    def solve(self, wordsearch: Wordsearch) -> SolutionResult:
        """
        Solve using hybrid random-then-ordered approach.
        """
        self._reset_metrics()
        start_time = time.time()
        
        # Set random seed if provided
        if self.seed is not None:
            random.seed(self.seed)
        
        grid = wordsearch.grid
        size = wordsearch.size
        word_bank = wordsearch.word_bank
        found_words: Dict[str, WordPosition] = {}
        
        # Try to find each word
        for word in word_bank:
            # Phase 1: Random search
            found, position = self._try_random_search(grid, word, size)
            
            if found:
                found_words[word] = position
            else:
                # Phase 2: Ordered search (fallback)
                found, position = self._try_ordered_search(grid, word, size)
                if found:
                    found_words[word] = position
        
        end_time = time.time()
        
        return SolutionResult(
            found_words=found_words,
            cells_examined=self.cells_examined,
            execution_time=end_time - start_time,
            strategy_name=self.get_name(),
            total_words=len(word_bank)
        )
