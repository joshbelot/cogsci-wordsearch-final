"""
Frame generator for word search strategy visualizations.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from typing import List, Tuple, Dict, Set
from PIL import Image
import io
from Strategy import WordPosition
from Wordsearch_Generator import Wordsearch


class FrameGenerator:
    """
    Generates visual frames for word search strategy animations.
    
    Each frame shows:
    - The word search grid with letters
    - Red highlight on currently examined cell
    - Green highlights on found words
    - Strategy name as title
    """
    
    def __init__(self, wordsearch: Wordsearch, strategy_name: str):
        """
        Initialize frame generator.
        
        Args:
            wordsearch: The puzzle to visualize
            strategy_name: Name of the strategy being animated
        """
        self.wordsearch = wordsearch
        self.strategy_name = strategy_name
        self.grid_size = len(wordsearch.grid)
        
        # Visual settings
        self.cell_size = 1.0
        self.font_size = 14
        self.title_font_size = 16
        self.dpi = 100
        
    def create_frame(self, 
                     current_cells: Set[Tuple[int, int]] = None,
                     found_words: Dict[str, WordPosition] = None,
                     partial_found_cells: Set[Tuple[int, int]] = None) -> np.ndarray:
        """
        Create a single frame of the animation.
        
        Args:
            current_cells: Set of (row, col) cells currently being examined (red highlight)
            found_words: Dictionary of words found so far (green highlights)
            partial_found_cells: Cells of word being discovered letter-by-letter (green)
            
        Returns:
            Frame as numpy array (RGB image)
        """
        if current_cells is None:
            current_cells = set()
        if found_words is None:
            found_words = {}
        if partial_found_cells is None:
            partial_found_cells = set()
        
        # Create figure
        fig, ax = plt.subplots(figsize=(8, 8), dpi=self.dpi)
        ax.set_xlim(-0.5, self.grid_size - 0.5)
        ax.set_ylim(-0.5, self.grid_size - 0.5)
        ax.set_aspect('equal')
        ax.invert_yaxis()  # Row 0 at top
        
        # Remove axes
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        
        # Add title
        ax.set_title(self.strategy_name, fontsize=self.title_font_size, 
                    fontweight='bold', pad=20)
        
        # Collect all cells that are part of found words
        found_cells: Set[Tuple[int, int]] = set()
        for word_pos in found_words.values():
            cells = self._get_word_cells(word_pos)
            found_cells.update(cells)
        
        # Draw grid and letters
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                # Determine cell color (priority: partial > found > current > default)
                is_partial = (row, col) in partial_found_cells
                is_found = (row, col) in found_cells
                is_current = (row, col) in current_cells
                
                # Draw cell background
                if is_partial:
                    # Bright green for word being discovered
                    color = '#51CF66'
                elif is_found:
                    # Darker green for already found words
                    color = '#37B24D'
                elif is_current:
                    # Red for current examination
                    color = '#FF6B6B'
                else:
                    # White for unexamined
                    color = 'white'
                
                rect = patches.Rectangle((col - 0.45, row - 0.45), 0.9, 0.9,
                                         linewidth=1, edgecolor='#CCCCCC',
                                         facecolor=color)
                ax.add_patch(rect)
                
                # Draw letter
                letter = self.wordsearch.grid[row][col]
                text_color = 'white' if (is_current or is_found or is_partial) else 'black'
                ax.text(col, row, letter, ha='center', va='center',
                       fontsize=self.font_size, fontweight='bold',
                       color=text_color, family='monospace')
        
        # Convert to numpy array using PIL for cross-platform compatibility
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=self.dpi, bbox_inches='tight', pad_inches=0.1)
        buf.seek(0)
        
        # Load as PIL Image then convert to numpy
        img = Image.open(buf)
        frame = np.array(img)
        
        # Convert RGBA to RGB if needed
        if frame.shape[2] == 4:
            frame = frame[:, :, :3]
        
        plt.close(fig)
        buf.close()
        
        return frame
    
    def _get_word_cells(self, word_pos: WordPosition) -> List[Tuple[int, int]]:
        """
        Get all cells occupied by a found word.
        
        Args:
            word_pos: Position of the found word
            
        Returns:
            List of (row, col) tuples for each letter
        """
        cells = []
        row, col = word_pos.start_row, word_pos.start_col
        dr, dc = word_pos.direction
        
        for _ in word_pos.word:
            cells.append((row, col))
            row += dr
            col += dc
        
        return cells
    
    def create_initial_frame(self) -> np.ndarray:
        """
        Create the initial frame showing just the puzzle.
        
        Returns:
            Frame as numpy array
        """
        return self.create_frame(current_cell=None, found_words={})
    
    def create_final_frame(self, found_words: Dict[str, WordPosition]) -> np.ndarray:
        """
        Create the final frame showing all found words.
        
        Args:
            found_words: All words found by the strategy
            
        Returns:
            Frame as numpy array
        """
        return self.create_frame(current_cell=None, found_words=found_words)
