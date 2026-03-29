"""
Ordered Search Strategy - Scans horizontally first, then vertically, then diagonally.
"""

import time
from typing import Dict
from ..strategy import Strategy, SolutionResult, WordPosition
from ..generator import Wordsearch


class OrderedSearchStrategy(Strategy):
    """
    Linear scan strategy that reads the grid systematically.
    
    Algorithm:
    1. For each word in the word bank:
       2. Scan the grid horizontally
       3. If not found, scan the grid vertically
       4. If not found, scan the grid diagonally
    
    This mimics a systematic scanning approach where the solver
    reads through the puzzle looking for a specific word in a predictable pattern.
    """
    
    def __init__(self):
        super().__init__()
        
        self.HORIZONTAL_DIRECTIONS = [(0, 1), (0, -1)]
        self.VERTICAL_DIRECTIONS = [(1, 0), (-1, 0)]
        self.DIAGONAL_DIRECTIONS = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    
    def get_name(self) -> str:
        return "Ordered Search"
    
    def solve(self, wordsearch: Wordsearch) -> SolutionResult:
        self._reset_metrics()
        start_time = time.time()
        
        grid = wordsearch.grid
        size = wordsearch.size
        word_bank = wordsearch.word_bank
        found_words: Dict[str, WordPosition] = {}
        
        direction_groups = [
            self.HORIZONTAL_DIRECTIONS,
            self.VERTICAL_DIRECTIONS,
            self.DIAGONAL_DIRECTIONS
        ]
        
        # Outer loop: Word-by-Word (mimicking human working memory)
        for word in word_bank:
            word_found = False
            
            # Single sweep across the grid for this word
            for row in range(size):
                if word_found:
                    break
                    
                for col in range(size):
                    if word_found:
                        break
                        
                    # Track the cognitive load of scanning the cell
                    self.cells_examined += 1
                    
                    if grid[row][col] == word[0]:
                        # Apply ordered directions at this specific cell
                        for direction_group in direction_groups:
                            if word_found:
                                break
                                
                            for direction in direction_group:
                                if self._check_word_at_position(grid, row=row, col=col, direction=direction, word=word, start_index=1):
                                    
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