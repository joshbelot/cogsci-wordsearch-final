"""
Brute Force Strategy - Exhaustive search through all positions and directions.
"""

import time
from typing import Dict
from ..strategy import Strategy, SolutionResult, WordPosition
from ..generator import Wordsearch


class BruteForceStrategy(Strategy):
    """
    Brute force word search strategy.
    
    Algorithm:
    1. For each word in the word bank:
       2. For each cell in the grid:
          3. For each of the 8 possible directions:
             4. Check if the word starts at this cell in this direction
             5. If found, record position and move to next word
    
    This is the simplest strategy but also the most thorough - it will
    always find all words if they exist in the puzzle.
    
    Time Complexity: O(w * n^2 * d * l) where:
        w = number of words
        n = grid size
        d = number of directions (8)
        l = average word length
    
    Performance Characteristics:
    - Guaranteed to find all words
    - Slowest for large puzzles
    - Good baseline for comparison
    """
    
    def get_name(self) -> str:
        return "Brute Force"
    
    def solve(self, wordsearch: Wordsearch) -> SolutionResult:
        """
        Solve using brute force: check every position in every direction for each word.
        """
        self._reset_metrics()
        start_time = time.time()
        
        grid = wordsearch.grid
        size = wordsearch.size
        word_bank = wordsearch.word_bank
        found_words: Dict[str, WordPosition] = {}
        
        # For each word in the word bank
        for word in word_bank:
            word_found = False
            
            # Try every position in the grid
            for row in range(size):
                if word_found:
                    break
                    
                for col in range(size):
                    if word_found:
                        break
                    
                    # Try every direction
                    for direction in self.DIRECTIONS:
                        if self._check_word_at_position(grid, word, row, col, direction):
                            # Found the word! Record its position
                            dr, dc = direction
                            end_row = row + dr * (len(word) - 1)
                            end_col = col + dc * (len(word) - 1)
                            
                            found_words[word] = WordPosition(
                                word=word,
                                start_row=row,
                                start_col=col,
                                end_row=end_row,
                                end_col=end_col,
                                direction=direction
                            )
                            word_found = True
                            break
        
        end_time = time.time()
        
        return SolutionResult(
            found_words=found_words,
            cells_examined=self.cells_examined,
            execution_time=end_time - start_time,
            strategy_name=self.get_name(),
            total_words=len(word_bank)
        )
