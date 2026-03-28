"""
Uncommon Letter Search Strategy - Prioritizes searching for least common letters.
"""

import time
from typing import Dict
from ..strategy import Strategy, SolutionResult, WordPosition
from ..generator import Wordsearch


class UncommonLetterSearchStrategy(Strategy):
    """
    Uncommon letter search strategy - find least common letters first.
    
    Algorithm:
    1. Use general English letter frequency knowledge (like a human would)
    2. For each word in word bank:
       a. Identify the least common letter based on general frequency
       b. Find all positions of that letter in the grid
       c. For each position, try all 8 directions
       d. Check if the word matches at that position/direction
    
    This models human behavior: recognizing that letters like Q, Z, X, J
    are rare and using them as anchor points for searching.
    
    Letter Rarity Ranking:
    Calculated from the word corpus used by the generator. Rarity scores
    are computed as the inverse of letter frequency in the corpus, so
    rare letters (Q, Z, X, J, etc.) get higher scores.
    
    Performance Characteristics:
    - More efficient than brute force
    - Models human cognitive strategy
    - Reduces search space significantly for words with uncommon letters
    - Uses corpus-specific letter frequencies rather than general statistics
    """
    
    def get_name(self) -> str:
        return "Uncommon Letter Search"
    
    def _get_least_common_letter(self, word, letter_rarity):
        """Find the least common letter in the word based on corpus frequency."""
        max_rarity = -1
        rarest_letter = word[0]
        
        for letter in word:
            rarity = letter_rarity.get(letter.upper(), 0.5)  # default for missing letters
            if rarity > max_rarity:
                max_rarity = rarity
                rarest_letter = letter
        
        return rarest_letter
    
    def solve(self, wordsearch: Wordsearch) -> SolutionResult:
        """
        Solve by finding the least common letter in each word first.
        Uses letter frequency calculated from the word corpus.
        """
        self._reset_metrics()
        start_time = time.time()
        
        grid = wordsearch.grid
        size = wordsearch.size
        word_bank = wordsearch.word_bank
        letter_rarity = wordsearch.letter_rarity
        found_words: Dict[str, WordPosition] = {}
        
        # For each word to find
        for word in word_bank:
            if not word:
                continue
            
            # Find the least common letter in this word (based on corpus frequency)
            search_letter = self._get_least_common_letter(word, letter_rarity)
            letter_index = word.index(search_letter)
            word_found = False
            
            # Find all positions with that rare letter
            for row in range(size):
                if word_found:
                    break
                    
                for col in range(size):
                    if word_found:
                        break
                        
                    # Check if this cell has the rare letter
                    if grid[row][col] == search_letter:
                        # Try all directions from this position
                        for direction in self.DIRECTIONS:
                            # Calculate where the word would start
                            dr, dc = direction
                            start_row = row - dr * letter_index
                            start_col = col - dc * letter_index
                            
                            # Check if start position is within bounds
                            if not (0 <= start_row < size and 0 <= start_col < size):
                                continue
                            
                            # Check if end position is within bounds
                            end_row = start_row + dr * (len(word) - 1)
                            end_col = start_col + dc * (len(word) - 1)
                            if not (0 <= end_row < size and 0 <= end_col < size):
                                continue
                            
                            if self._check_word_at_position(grid, word, start_row, start_col, direction):
                                # Found the word!
                                found_words[word] = WordPosition(
                                    word=word,
                                    start_row=start_row,
                                    start_col=start_col,
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
