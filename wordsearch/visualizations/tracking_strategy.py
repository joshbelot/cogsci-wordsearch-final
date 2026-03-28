"""
Strategy wrapper that tracks cell examinations for visualization.
"""

from typing import List, Tuple, Dict
from ..strategy import Strategy, SolutionResult, WordPosition
from ..generator import Wordsearch


class TrackingStrategy(Strategy):
    """
    Wrapper around any strategy that tracks cell examinations for animation.
    
    This wrapper intercepts the strategy's execution and records:
    - Every cell examined (row, col) in order
    - When each word is found
    - The search progression over time
    
    This allows us to replay the strategy's search pattern visually.
    """
    
    def __init__(self, base_strategy: Strategy):
        """
        Initialize tracking wrapper.
        
        Args:
            base_strategy: The strategy to wrap and track
        """
        super().__init__()
        self.base_strategy = base_strategy
        
        # Tracking data
        self.cell_examinations: List[Tuple[int, int]] = []  # [(row, col), ...]
        self.word_found_at_step: Dict[str, int] = {}  # {word: step_number}
        self.found_words: Dict[str, WordPosition] = {}
        
    def get_name(self) -> str:
        """Return the base strategy's name."""
        return self.base_strategy.get_name()
    
    def reset_tracking(self):
        """Clear all tracking data."""
        self.cell_examinations = []
        self.word_found_at_step = {}
        self.found_words = {}
    
    def track_cell(self, row: int, col: int):
        """
        Record that a cell was examined.
        
        Args:
            row: Row index
            col: Column index
        """
        self.cell_examinations.append((row, col))
    
    def track_word_found(self, word: str, position: WordPosition):
        """
        Record that a word was found.
        
        Args:
            word: The word that was found
            position: Position information for the word
        """
        step = len(self.cell_examinations)
        self.word_found_at_step[word] = step
        self.found_words[word] = position
    
    def solve(self, wordsearch: Wordsearch) -> SolutionResult:
        """
        Solve with tracking by monkey-patching the grid access.
        
        We'll override the grid's __getitem__ to track accesses.
        """
        self.reset_tracking()
        
        # Store original grid
        original_grid = wordsearch.grid
        
        # Create tracking grid wrapper
        tracker = self
        
        class TrackingRow(list):
            """Wrapper for grid rows that tracks column access."""
            def __init__(self, row_data, row_index, tracker):
                super().__init__(row_data)
                self._row_index = row_index
                self._tracker = tracker
            
            def __getitem__(self, col_index):
                self._tracker.track_cell(self._row_index, col_index)
                return super().__getitem__(col_index)
        
        class TrackingGrid(list):
            """Wrapper for grid that returns TrackingRow objects."""
            def __init__(self, grid, tracker):
                # Create tracking rows for each row in the grid
                tracking_rows = [TrackingRow(row, i, tracker) for i, row in enumerate(grid)]
                super().__init__(tracking_rows)
                self._tracker = tracker
                self.size = len(grid)
        
        # Replace grid with tracking wrapper
        tracking_grid = TrackingGrid(original_grid, self)
        wordsearch.grid = tracking_grid
        
        # Run the base strategy
        result = self.base_strategy.solve(wordsearch)
        
        # Restore original grid
        wordsearch.grid = original_grid
        
        # Record found words
        for word, position in result.found_words.items():
            if word not in self.found_words:
                self.track_word_found(word, position)
        
        return result
    
    def get_tracking_data(self) -> Dict:
        """
        Get all tracking data for visualization.
        
        Returns:
            Dict with cell_examinations, word_found_at_step, and found_words
        """
        return {
            'cell_examinations': self.cell_examinations,
            'word_found_at_step': self.word_found_at_step,
            'found_words': self.found_words,
            'total_steps': len(self.cell_examinations)
        }
