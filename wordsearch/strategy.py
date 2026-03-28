"""
Base classes and data structures for word search solving strategies.
"""

from abc import ABC, abstractmethod
from typing import List, Tuple, Dict
from dataclasses import dataclass, field


@dataclass
class WordPosition:
    """Represents the position and orientation of a found word."""
    word: str
    start_row: int
    start_col: int
    end_row: int
    end_col: int
    direction: Tuple[int, int]  # (row_delta, col_delta)
    
    def __str__(self):
        directions = {
            (0, 1): "horizontal right",
            (0, -1): "horizontal left",
            (1, 0): "vertical down",
            (-1, 0): "vertical up",
            (1, 1): "diagonal down-right",
            (1, -1): "diagonal down-left",
            (-1, 1): "diagonal up-right",
            (-1, -1): "diagonal up-left"
        }
        dir_name = directions.get(self.direction, "unknown")
        return f"{self.word} at ({self.start_row}, {self.start_col}) -> ({self.end_row}, {self.end_col}) [{dir_name}]"


@dataclass
class SolutionResult:
    """
    Container for word search solution results and performance metrics.
    """
    found_words: Dict[str, WordPosition] = field(default_factory=dict)
    cells_examined: int = 0
    execution_time: float = 0.0
    strategy_name: str = ""
    total_words: int = 0
    
    @property
    def words_found_count(self) -> int:
        """Number of words successfully found."""
        return len(self.found_words)
    
    @property
    def success_rate(self) -> float:
        """Percentage of words found (0.0 to 1.0)."""
        if self.total_words == 0:
            return 0.0
        return self.words_found_count / self.total_words
    
    @property
    def cells_per_second(self) -> float:
        """Rate of cell examination."""
        if self.execution_time == 0:
            return 0.0
        return self.cells_examined / self.execution_time
    
    def __str__(self):
        result = [
            f"Strategy: {self.strategy_name}",
            f"Found: {self.words_found_count}/{self.total_words} words ({self.success_rate*100:.1f}%)",
            f"Time: {self.execution_time:.4f} seconds",
            f"Cells examined: {self.cells_examined:,}",
            f"Speed: {self.cells_per_second:.0f} cells/second",
            f"\nWords found:"
        ]
        for word_pos in self.found_words.values():
            result.append(f"  - {word_pos}")
        
        missing = self.total_words - self.words_found_count
        if missing > 0:
            result.append(f"\nMissing {missing} words")
        
        return "\n".join(result)


class Strategy(ABC):
    """
    Abstract base class for word search solving strategies.
    
    All strategies must implement the solve() method which takes a Wordsearch
    object and returns a SolutionResult with found words and metrics.
    """
    
    # Common directions used by most strategies
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
    
    def __init__(self):
        self.cells_examined = 0
    
    @abstractmethod
    def solve(self, wordsearch) -> SolutionResult:
        """
        Solve the word search puzzle.
        
        Args:
            wordsearch: The Wordsearch object to solve
            
        Returns:
            SolutionResult containing found words and performance metrics
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Return the name of this strategy."""
        pass
    
    def _check_word_at_position(self, grid: List[List[str]], word: str,
                                row: int, col: int, direction: Tuple[int, int]) -> bool:
        """
        Helper method: Check if a word exists at a specific position and direction.
        
        Args:
            grid: The word search grid
            word: Word to search for
            row: Starting row
            col: Starting column
            direction: Direction tuple (row_delta, col_delta)
            
        Returns:
            True if word is found at this position/direction
        """
        dr, dc = direction
        size = len(grid)
        
        # Check bounds
        end_row = row + dr * (len(word) - 1)
        end_col = col + dc * (len(word) - 1)
        
        if not (0 <= end_row < size and 0 <= end_col < size):
            return False
        
        # Check each letter
        for i, letter in enumerate(word):
            r = row + dr * i
            c = col + dc * i
            self.cells_examined += 1
            
            if grid[r][c] != letter:
                return False
        
        return True
    
    def _reset_metrics(self):
        """Reset performance counters."""
        self.cells_examined = 0
