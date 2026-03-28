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
    1. Scan each row left to right
    2. At each cell, check all 8 directions for any word from word bank
    3. Mark found words to avoid duplicates
    
    This mimics a systematic scanning approach where the solver
    reads through the puzzle in a predictable pattern.
    
    Time Complexity: O(n^2 * d * w * l) where:
        n = grid size
        d = number of directions (8)
        w = number of words
        l = average word length
    
    Performance Characteristics:
    - More systematic than random search
    - Position-first rather than word-first
    - Models systematic visual scanning behavior
    """
    
    def __init__(self):
        """Initialize ordered search strategy with direction groups."""
        super().__init__()
        
        # Define direction groups for ordered scanning
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
        return "Ordered Search"
    
    def solve(self, wordsearch: Wordsearch) -> SolutionResult:
        """
        Solve by scanning horizontally first, then vertically, then diagonally.
        """
        self._reset_metrics()
        start_time = time.time()
        
        grid = wordsearch.grid
        size = wordsearch.size
        word_bank = wordsearch.word_bank
        found_words: Dict[str, WordPosition] = {}
        remaining_words = set(word_bank)
        
        # Search in order: horizontal, vertical, then diagonal
        direction_groups = [
            self.HORIZONTAL_DIRECTIONS,
            self.VERTICAL_DIRECTIONS,
            self.DIAGONAL_DIRECTIONS
        ]
        
        for direction_group in direction_groups:
            if not remaining_words:
                break
                
            # Scan each position in the grid
            for row in range(size):
                if not remaining_words:
                    break
                    
                for col in range(size):
                    if not remaining_words:
                        break
                        
                    # Try each direction in this group
                    for direction in direction_group:
                        # Check each remaining word
                        for word in list(remaining_words):
                            if self._check_word_at_position(grid, word, row, col, direction):
                                # Found a word! Record it
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
                                remaining_words.remove(word)
        
        end_time = time.time()
        
        return SolutionResult(
            found_words=found_words,
            cells_examined=self.cells_examined,
            execution_time=end_time - start_time,
            strategy_name=self.get_name(),
            total_words=len(word_bank)
        )
