"""
Patch Search Strategy - Divides grid into 4×4 patches and searches within them.
"""

import time
from typing import Dict, List, Tuple, Set
from ..strategy import Strategy, SolutionResult, WordPosition
from ..generator import Wordsearch


class PatchSearchStrategy(Strategy):
    """
    Patch search strategy that divides the grid into 4×4 patches.
    
    Algorithm:
    1. Divide the grid into overlapping or non-overlapping 4×4 patches
    2. For each patch, extract all possible substrings (horizontal, vertical, diagonal)
    3. Check if any substring appears in any word from the word bank
    4. When a match is found, verify the complete word at that location
    5. Continue through all patches until all words are found
    
    This strategy mimics focused attention on small regions of the puzzle,
    similar to how humans might scan a wordsearch by looking at chunks
    rather than individual cells.
    
    Parameters:
        patch_size: Size of each patch (default 4×4)
        overlap: Whether patches should overlap (default True)
    
    Performance Characteristics:
    - Reduces search space by focusing on local regions
    - More efficient than random sampling for dense puzzles
    - May need multiple passes if patches don't overlap
    """
    
    def __init__(self, patch_size: int = 4, overlap: bool = True):
        """
        Initialize patch search strategy.
        
        Args:
            patch_size: Size of square patches to examine
            overlap: Whether patches should overlap by 1 cell
        """
        super().__init__()
        self.patch_size = patch_size
        self.overlap = overlap
    
    def get_name(self) -> str:
        return "Patch Search"
    
    def _extract_patch_substrings(self, grid: List[List[str]], 
                                   patch_row: int, patch_col: int, 
                                   size: int) -> Set[str]:
        """Extract all substrings of length 2+ from a patch."""
        substrings = set()
        patch_end_row = min(patch_row + self.patch_size, size)
        patch_end_col = min(patch_col + self.patch_size, size)
        
        # Extract horizontal and reverse horizontal
        for r in range(patch_row, patch_end_row):
            for c in range(patch_col, patch_end_col):
                for length in range(2, self.patch_size + 1):
                    if c + length <= patch_end_col:
                        substr = ''.join(grid[r][c:c + length])
                        substrings.add(substr)
                        substrings.add(substr[::-1])
        
        # Extract vertical and reverse vertical
        for c in range(patch_col, patch_end_col):
            for r in range(patch_row, patch_end_row):
                for length in range(2, self.patch_size + 1):
                    if r + length <= patch_end_row:
                        substr = ''.join(grid[r + i][c] for i in range(length))
                        substrings.add(substr)
                        substrings.add(substr[::-1])
        
        # Extract diagonal (both directions)
        for r in range(patch_row, patch_end_row):
            for c in range(patch_col, patch_end_col):
                # Down-right diagonal
                for length in range(2, self.patch_size + 1):
                    if r + length <= patch_end_row and c + length <= patch_end_col:
                        substr = ''.join(grid[r + i][c + i] for i in range(length))
                        substrings.add(substr)
                        substrings.add(substr[::-1])
                
                # Down-left diagonal
                for length in range(2, self.patch_size + 1):
                    if r + length <= patch_end_row and c - length + 1 >= patch_col:
                        substr = ''.join(grid[r + i][c - i] for i in range(length))
                        substrings.add(substr)
                        substrings.add(substr[::-1])
        
        return substrings
    
    def solve(self, wordsearch: Wordsearch) -> SolutionResult:
        """
        Solve by scanning grid in patches and checking for word fragments.
        """
        self._reset_metrics()
        start_time = time.time()
        
        grid = wordsearch.grid
        size = wordsearch.size
        word_bank = wordsearch.word_bank
        found_words: Dict[str, WordPosition] = {}
        remaining_words = set(word_bank)
        
        # Determine patch step size
        step = 1 if self.overlap else self.patch_size
        
        # Scan through patches
        for patch_row in range(0, size, step):
            for patch_col in range(0, size, step):
                if not remaining_words:
                    break
                
                # Extract substrings from this patch
                patch_substrings = self._extract_patch_substrings(grid, patch_row, patch_col, size)
                
                # Check if any remaining word has a substring in this patch
                for word in list(remaining_words):
                    # Check if any substring of the word appears in patch
                    word_found_in_patch = any(word[i:j] in patch_substrings 
                                              for i in range(len(word)) 
                                              for j in range(i + 2, len(word) + 1))
                    
                    if word_found_in_patch:
                        # Try to find the complete word in the entire grid
                        # Check all positions and directions
                        for row in range(size):
                            for col in range(size):
                                for direction in self.DIRECTIONS:
                                    if self._check_word_at_position(grid, word, row, col, direction):
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
                                        break
                                if word not in remaining_words:
                                    break
                            if word not in remaining_words:
                                break
        
        end_time = time.time()
        
        return SolutionResult(
            found_words=found_words,
            cells_examined=self.cells_examined,
            execution_time=end_time - start_time,
            strategy_name=self.get_name(),
            total_words=len(word_bank)
        )
