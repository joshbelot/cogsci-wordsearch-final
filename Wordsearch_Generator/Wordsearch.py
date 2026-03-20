import random
import os
from typing import List, Tuple, Optional


class Wordsearch:
    """
    Represents a generated word search puzzle.
    """
    def __init__(self, grid: List[List[str]], word_bank: List[str], size: int, letter_rarity: dict = None):
        self.grid = grid
        self.word_bank = word_bank
        self.size = size
        self.letter_rarity = letter_rarity if letter_rarity else {}
    
    def __str__(self):
        """Returns a string representation of the word search grid."""
        result = []
        for row in self.grid:
            result.append(' '.join(row))
        result.append('\nWord Bank:')
        result.append(', '.join(self.word_bank))
        return '\n'.join(result)
    
    def display(self):
        """Prints the word search puzzle."""
        print(self)


class WordsearchGenerator:
    """
    Generates word search puzzles with customizable parameters.
    """
    
    # English letter frequency distribution (approximate percentages)
    # Used for filling empty cells to create natural-looking puzzles
    LETTER_FREQUENCIES = {
        'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97,
        'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25,
        'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36,
        'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29,
        'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10,
        'Z': 0.07
    }
    
    # 8 directions: horizontal (L-R, R-L), vertical (T-B, B-T), diagonal (4 directions)
    DIRECTIONS = [
        (0, 1),   # horizontal right
        (0, -1),  # horizontal left
        (1, 0),   # vertical down
        (-1, 0),  # vertical up
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
        (-1, 1),  # diagonal up-right
        (-1, -1)  # diagonal up-left
    ]
    
    def __init__(self, word_file: Optional[str] = None):
        """
        Initialize the word search generator.
        
        Args:
            word_file: Path to a text file containing words (one per line).
                      If None, defaults to the provided word list.
        """
        if word_file is None:
            # Default to the provided word list in the same directory
            current_dir = os.path.dirname(os.path.abspath(__file__))
            word_file = os.path.join(current_dir, 'google-10000-english-usa-no-swears-medium.txt')
        
        self.word_corpus = self._load_words(word_file)
        
        # Calculate letter frequencies from the corpus
        corpus_frequencies = self._calculate_corpus_letter_frequencies()
        
        # Calculate rarity scores (inverse of frequency) for search strategies
        self.letter_rarity = {}
        for letter, freq in corpus_frequencies.items():
            if freq > 0:
                self.letter_rarity[letter] = 1.0 / freq
            else:
                self.letter_rarity[letter] = 0.0
        
        # Prepare letter sampling based on frequency distribution
        # Use the general English frequencies for filling empty cells (more natural looking)
        self.letters = list(self.LETTER_FREQUENCIES.keys())
        self.weights = list(self.LETTER_FREQUENCIES.values())
    
    def _load_words(self, file_path: str) -> List[str]:
        """Load words from a file."""
        with open(file_path, 'r') as f:
            words = [line.strip().upper() for line in f if line.strip()]
        return words
    
    def _calculate_corpus_letter_frequencies(self) -> dict:
        """
        Calculate letter frequency distribution from the word corpus.
        Returns frequencies as percentages (like LETTER_FREQUENCIES).
        """
        from collections import Counter
        
        # Count all letters in the corpus
        letter_counts = Counter()
        total_letters = 0
        
        for word in self.word_corpus:
            for letter in word:
                if letter.isalpha():
                    letter_counts[letter.upper()] += 1
                    total_letters += 1
        
        # Convert to percentages
        letter_frequencies = {}
        for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            count = letter_counts.get(letter, 0)
            letter_frequencies[letter] = (count / total_letters * 100) if total_letters > 0 else 0.0
        
        return letter_frequencies
    
    def _get_random_letter(self) -> str:
        """Get a random letter based on English letter frequency."""
        return random.choices(self.letters, weights=self.weights, k=1)[0]
    
    def _calculate_word_count(self, size: int) -> int:
        """
        Calculate an appropriate number of words based on grid size.
        Larger grids can accommodate more words.
        """
        # Use a formula that scales with grid size
        # For a 10x10 grid, this gives 5-8 words
        # For a 20x20 grid, this gives 10-16 words
        min_words = max(3, size // 2)
        max_words = max(5, int(size * 0.8))
        return random.randint(min_words, max_words)
    
    def _filter_words(self, min_length: Optional[int] = None, 
                     max_length: Optional[int] = None, 
                     size: int = 10) -> List[str]:
        """
        Filter words based on length constraints.
        
        Args:
            min_length: Minimum word length (default: 3)
            max_length: Maximum word length (default: grid size)
            size: Grid size
        
        Returns:
            Filtered list of words
        """
        if min_length is None:
            min_length = 3
        if max_length is None:
            max_length = size
        
        filtered = [word for word in self.word_corpus 
                   if min_length <= len(word) <= max_length]
        return filtered
    
    def _can_place_word(self, grid: List[List[str]], word: str, 
                       row: int, col: int, direction: Tuple[int, int]) -> bool:
        """
        Check if a word can be placed at the given position and direction.
        """
        dr, dc = direction
        size = len(grid)
        
        # Check if word fits within grid bounds
        end_row = row + dr * (len(word) - 1)
        end_col = col + dc * (len(word) - 1)
        
        if not (0 <= end_row < size and 0 <= end_col < size):
            return False
        
        # Check if cells are empty or match the word letter
        for i, letter in enumerate(word):
            r = row + dr * i
            c = col + dc * i
            if grid[r][c] != '' and grid[r][c] != letter:
                return False
        
        return True
    
    def _place_word(self, grid: List[List[str]], word: str, 
                   row: int, col: int, direction: Tuple[int, int]) -> bool:
        """
        Place a word in the grid at the given position and direction.
        """
        dr, dc = direction
        
        for i, letter in enumerate(word):
            r = row + dr * i
            c = col + dc * i
            grid[r][c] = letter
        
        return True
    
    def _try_place_word(self, grid: List[List[str]], word: str, 
                       max_attempts: int = 100) -> bool:
        """
        Try to place a word in the grid. Returns True if successful.
        """
        size = len(grid)
        
        for _ in range(max_attempts):
            # Random starting position
            row = random.randint(0, size - 1)
            col = random.randint(0, size - 1)
            
            # Random direction
            direction = random.choice(self.DIRECTIONS)
            
            if self._can_place_word(grid, word, row, col, direction):
                self._place_word(grid, word, row, col, direction)
                return True
        
        return False
    
    def _remove_substring_words(self, words: List[str]) -> List[str]:
        """
        Remove words that are substrings of other words in the list.
        Keeps longer words and removes shorter ones.
        
        Args:
            words: List of words to filter
        
        Returns:
            Filtered list with no substring duplicates
        """
        # Sort by length (longest first) to prioritize keeping longer words
        sorted_words = sorted(words, key=len, reverse=True)
        filtered = []
        
        for word in sorted_words:
            # Check if this word is a substring of any already-kept word
            is_substring = False
            for kept_word in filtered:
                if word in kept_word and word != kept_word:
                    is_substring = True
                    break
            
            if not is_substring:
                filtered.append(word)
        
        return filtered
    
    def _fill_empty_cells(self, grid: List[List[str]]) -> None:
        """
        Fill empty cells with random letters based on frequency distribution.
        """
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] == '':
                    grid[i][j] = self._get_random_letter()
    
    def generate(self, size: int, min_word_length: Optional[int] = None, 
                max_word_length: Optional[int] = None) -> Wordsearch:
        """
        Generate a new word search puzzle.
        
        Args:
            size: The size of the grid (size x size)
            min_word_length: Minimum length of words to include (default: 3)
            max_word_length: Maximum length of words to include (default: grid size)
        
        Returns:
            A Wordsearch object containing the generated puzzle
        """
        # Initialize empty grid
        grid = [['' for _ in range(size)] for _ in range(size)]
        
        # Filter words based on length constraints
        available_words = self._filter_words(min_word_length, max_word_length, size)
        
        if not available_words:
            raise ValueError("No words available matching the given constraints")
        
        # Determine how many words to include
        word_count = self._calculate_word_count(size)
        word_count = min(word_count, len(available_words))
        
        # Randomly select words from the corpus
        selected_words = random.sample(available_words, word_count)
        
        # Remove substring words to avoid redundancy (e.g., CAT inside CATCH)
        selected_words = self._remove_substring_words(selected_words)
        
        # Try to place each word
        placed_words = []
        for word in selected_words:
            if self._try_place_word(grid, word):
                placed_words.append(word)
        
        # Fill remaining empty cells with random letters
        self._fill_empty_cells(grid)
        
        return Wordsearch(grid, placed_words, size, self.letter_rarity)


# Example usage
if __name__ == "__main__":
    # Create generator with default word list
    generator = WordsearchGenerator()
    
    # Generate a 10x10 word search
    puzzle = generator.generate(size=10, min_word_length=4, max_word_length=8)
    
    # Display the puzzle
    puzzle.display()
