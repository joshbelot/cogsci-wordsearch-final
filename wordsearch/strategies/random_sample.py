"""
Random Sample Strategy - Takes random length-4 samples and checks for overlap with words.
"""

import time
import random
from typing import Dict, Set
from ..strategy import Strategy, SolutionResult, WordPosition
from ..generator import Wordsearch


class RandomSampleStrategy(Strategy):
    """
    Random sample strategy with length-4 string sampling.
    
    Algorithm:
    1. Take random samples of length 4 from the grid
    2. Samples can be horizontal, vertical, diagonal, or backwards
    3. For each random string, scan the word bank for overlap > 1 letter
    4. If overlap found, try to extend the match to find the full word
    5. Continue until max attempts reached or all words found
    """
    
    def __init__(self, max_attempts: int = 2000, seed: int = 42):
        """
        Initialize random sample strategy.
        
        Args:
            max_attempts: How many random samples to take
            seed: Random seed for reproducibility
        """
        super().__init__()
        self.max_attempts = max_attempts
        self.seed = seed
    
    def get_name(self) -> str:
        return f"Random Sample (attempts={self.max_attempts})"
    
    def _extract_string_from_grid(self, grid, size, row, col, direction, length=4):
        """Extract a string of given length from grid at position/direction."""
        dr, dc = direction
        string = ""
        
        for i in range(length):
            r = row + dr * i
            c = col + dc * i
            
            if not (0 <= r < size and 0 <= c < size):
                return None
            
            # Track cognitive load of reading this cell
            self.cells_examined += 1
            string += grid[r][c]
        
        return string
    
    def _find_overlap(self, sample, word):
        """Find if there's > 1 letter overlap between sample and word."""
        # Check if sample is a substring of word
        if sample in word:
            return len(sample)
        
        # Check for overlaps at different positions
        max_overlap = 0
        for i in range(len(sample)):
            for j in range(len(word)):
                overlap = 0
                k = 0
                while (i + k < len(sample) and j + k < len(word) and 
                       sample[i + k] == word[j + k]):
                    overlap += 1
                    k += 1
                max_overlap = max(max_overlap, overlap)
        
        return max_overlap
    
    def solve(self, wordsearch: Wordsearch) -> SolutionResult:
        """
        Solve by taking random length-4 samples and checking for word overlaps.
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
        remaining_words = set(word_bank)
        
        attempts = 0
        
        while attempts < self.max_attempts and remaining_words:
            # Random position
            row = random.randint(0, size - 1)
            col = random.randint(0, size - 1)
            
            # Random direction
            direction = random.choice(self.DIRECTIONS)
            
            # Extract length-4 sample
            sample = self._extract_string_from_grid(grid, size, row, col, direction, length=4)
            
            if sample:
                # Check for overlap with remaining words
                for word in list(remaining_words):
                    overlap = self._find_overlap(sample, word)
                    
                    if overlap > 1:
                        # Found significant overlap, now search the entire grid for this word
                        # Try all positions and directions
                        word_found = False
                        for search_row in range(size):
                            if word_found:
                                break
                            for search_col in range(size):
                                if word_found:
                                    break
                                
                                # First letter check optimization
                                self.cells_examined += 1
                                if grid[search_row][search_col] == word[0]:
                                    
                                    for search_dir in self.DIRECTIONS:
                                        if self._check_word_at_position(grid, word, search_row, search_col, search_dir, start_index=1):
                                            dr, dc = search_dir
                                            end_row = search_row + dr * (len(word) - 1)
                                            end_col = search_col + dc * (len(word) - 1)
                                            
                                            found_words[word] = WordPosition(
                                                word=word,
                                                start_row=search_row,
                                                start_col=search_col,
                                                end_row=end_row,
                                                end_col=end_col,
                                                direction=search_dir
                                            )
                                            remaining_words.remove(word)
                                            word_found = True
                                            break
            
            attempts += 1
        
        end_time = time.time()
        
        return SolutionResult(
            found_words=found_words,
            cells_examined=self.cells_examined,
            execution_time=end_time - start_time,
            strategy_name=self.get_name(),
            total_words=len(word_bank)
        )