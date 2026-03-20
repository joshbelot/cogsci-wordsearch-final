"""
Conceptual animation builder for strategy visualizations.

This creates conceptual animations that demonstrate the strategy's approach
rather than mirroring the exact algorithm execution.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List, Tuple, Dict, Set
from PIL import Image
import numpy as np
import random
from visualizations.frame_generator import FrameGenerator
from Strategy import Strategy, WordPosition
from Wordsearch_Generator import Wordsearch


class ConceptualAnimator:
    """
    Creates conceptual animations for each strategy type.
    """
    
    def __init__(self, 
                 wordsearch: Wordsearch,
                 strategy: Strategy,
                 fps: int = 8):
        """
        Initialize conceptual animator.
        
        Args:
            wordsearch: The puzzle to solve and animate
            strategy: The strategy to demonstrate
            fps: Frames per second
        """
        self.wordsearch = wordsearch
        self.strategy = strategy
        self.fps = fps
        self.frame_generator = FrameGenerator(wordsearch, strategy.get_name())
        
        # Solve to get word positions
        result = strategy.solve(wordsearch)
        self.found_words = result.found_words
        
    def generate_animation(self, output_path: str, verbose: bool = True):
        """
        Generate the full animation based on strategy type.
        
        Args:
            output_path: Path to save GIF
            verbose: Print progress
        """
        strategy_name = self.strategy.get_name()
        
        if verbose:
            print(f"Building conceptual animation for {strategy_name}...")
        
        # Route to appropriate animator based on strategy
        if "Brute Force" in strategy_name:
            frames = self._animate_brute_force()
        elif "Ordered Search" in strategy_name:
            frames = self._animate_ordered_search()
        elif "Uncommon Letter" in strategy_name:
            frames = self._animate_uncommon_letter()
        elif "Random Sample" in strategy_name:
            frames = self._animate_random_sample()
        elif "Patch Search" in strategy_name:
            frames = self._animate_patch_search()
        elif "Random to Ordered" in strategy_name:
            frames = self._animate_random_to_ordered()
        else:
            # Default: simple scan
            frames = self._animate_brute_force()
        
        # Save as GIF
        if frames:
            duration = int(1000 / self.fps)
            frames[0].save(
                output_path,
                save_all=True,
                append_images=frames[1:],
                duration=duration,
                loop=0
            )
            
            if verbose:
                file_size = os.path.getsize(output_path) / (1024 * 1024)
                animation_length = len(frames) / self.fps
                print(f"  ✓ Saved to {output_path}")
                print(f"    Frames: {len(frames)} ({animation_length:.1f}s)")
                print(f"    Size: {file_size:.2f} MB")
                print(f"    Words found: {len(self.found_words)}")
    
    def _add_initial_pause(self, frames: List[Image.Image], seconds: float = 2.0):
        """Add initial frames showing just the puzzle."""
        initial_frame = self.frame_generator.create_frame()
        count = int(self.fps * seconds)
        for _ in range(count):
            frames.append(Image.fromarray(initial_frame))
    
    def _add_final_pause(self, frames: List[Image.Image], seconds: float = 2.0):
        """Add final frames showing all found words."""
        final_frame = self.frame_generator.create_frame(
            found_words=self.found_words
        )
        count = int(self.fps * seconds)
        for _ in range(count):
            frames.append(Image.fromarray(final_frame))
    
    def _animate_word_discovery(self, 
                                frames: List[Image.Image],
                                word_pos: WordPosition,
                                current_highlights: Set[Tuple[int, int]],
                                found_so_far: Dict[str, WordPosition]):
        """
        Animate a word being discovered letter by letter.
        
        Args:
            frames: List to append frames to
            word_pos: Position of word being discovered
            current_highlights: Current red highlighted cells
            found_so_far: Words found so far (will be updated)
        """
        # Get cells for this word
        cells = []
        row, col = word_pos.start_row, word_pos.start_col
        dr, dc = word_pos.direction
        for _ in word_pos.word:
            cells.append((row, col))
            row += dr
            col += dc
        
        # Animate each letter turning green
        partial_word_cells = set()
        for cell in cells:
            partial_word_cells.add(cell)
            frame = self.frame_generator.create_frame(
                current_cells=current_highlights,
                found_words=found_so_far,
                partial_found_cells=partial_word_cells
            )
            frames.append(Image.fromarray(frame))
        
        # Word fully found - add to found_words
        found_so_far[word_pos.word] = word_pos
        
        # Show complete word for a moment
        frame = self.frame_generator.create_frame(
            current_cells=current_highlights,
            found_words=found_so_far
        )
        for _ in range(self.fps // 2):  # 0.5 second pause
            frames.append(Image.fromarray(frame))
    
    def _animate_brute_force(self) -> List[Image.Image]:
        """Systematic row-by-row, position-by-position scan."""
        frames = []
        self._add_initial_pause(frames)
        
        found_so_far = {}
        size = len(self.wordsearch.grid)
        
        # Scan row by row, column by column
        for row in range(size):
            for col in range(size):
                # Highlight current position
                frame = self.frame_generator.create_frame(
                    current_cells={(row, col)},
                    found_words=found_so_far
                )
                frames.append(Image.fromarray(frame))
                
                # Check if this position starts any word
                for word, word_pos in self.found_words.items():
                    if word not in found_so_far:
                        if word_pos.start_row == row and word_pos.start_col == col:
                            self._animate_word_discovery(
                                frames, word_pos, {(row, col)}, found_so_far
                            )
        
        self._add_final_pause(frames)
        return frames
    
    def _animate_ordered_search(self) -> List[Image.Image]:
        """Horizontal lines first, then vertical, then diagonal."""
        frames = []
        self._add_initial_pause(frames)
        
        found_so_far = {}
        size = len(self.wordsearch.grid)
        
        # Phase 1: Horizontal scan (row by row)
        for row in range(size):
            for col in range(size):
                frame = self.frame_generator.create_frame(
                    current_cells={(row, col)},
                    found_words=found_so_far
                )
                frames.append(Image.fromarray(frame))
                
                for word, word_pos in self.found_words.items():
                    if word not in found_so_far and word_pos.start_row == row and word_pos.start_col == col:
                        if word_pos.direction in [(0, 1), (0, -1)]:  # Horizontal
                            self._animate_word_discovery(frames, word_pos, {(row, col)}, found_so_far)
        
        # Phase 2: Vertical scan (column by column)
        for col in range(size):
            for row in range(size):
                frame = self.frame_generator.create_frame(
                    current_cells={(row, col)},
                    found_words=found_so_far
                )
                frames.append(Image.fromarray(frame))
                
                for word, word_pos in self.found_words.items():
                    if word not in found_so_far and word_pos.start_row == row and word_pos.start_col == col:
                        if word_pos.direction in [(1, 0), (-1, 0)]:  # Vertical
                            self._animate_word_discovery(frames, word_pos, {(row, col)}, found_so_far)
        
        # Phase 3: Diagonal scan (scan diagonals systematically)
        # Scan all diagonals from top-left to bottom-right direction
        # Start from top row, then left column
        for start in range(size * 2 - 1):
            diagonal_cells = []
            if start < size:
                # Diagonals starting from top row
                row, col = 0, start
            else:
                # Diagonals starting from left column
                row, col = start - size + 1, 0
            
            # Trace the diagonal
            while row < size and col < size:
                diagonal_cells.append((row, col))
                row += 1
                col += 1
            
            # Scan this diagonal
            for row, col in diagonal_cells:
                frame = self.frame_generator.create_frame(
                    current_cells={(row, col)},
                    found_words=found_so_far
                )
                frames.append(Image.fromarray(frame))
                
                # Check for diagonal words at this position
                for word, word_pos in self.found_words.items():
                    if word not in found_so_far and word_pos.start_row == row and word_pos.start_col == col:
                        # Any diagonal direction
                        if word_pos.direction in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                            self._animate_word_discovery(frames, word_pos, {(row, col)}, found_so_far)
        
        self._add_final_pause(frames)
        return frames
    
    def _animate_uncommon_letter(self) -> List[Image.Image]:
        """For each word, find its rarest letter and search from those positions."""
        frames = []
        self._add_initial_pause(frames)
        
        found_so_far = {}
        
        # Letter rarity (higher = more rare)
        letter_rarity = {
            'Q': 26, 'Z': 25, 'X': 24, 'J': 23, 'K': 22, 'V': 21, 'W': 20, 'F': 19,
            'Y': 18, 'B': 17, 'G': 16, 'P': 15, 'M': 14, 'H': 13, 'C': 12, 'U': 11,
            'D': 10, 'L': 9, 'R': 8, 'S': 7, 'N': 6, 'I': 5, 'O': 4, 'A': 3, 'T': 2, 'E': 1
        }
        
        # For each word, find its rarest letter and search
        for word, word_pos in self.found_words.items():
            if word in found_so_far:
                continue
            
            # Find rarest letter in this word
            rarest_letter = max(word, key=lambda letter: letter_rarity.get(letter, 0))
            
            # Find all positions of that rare letter in the grid
            rare_letter_positions = []
            for row in range(len(self.wordsearch.grid)):
                for col in range(len(self.wordsearch.grid[0])):
                    if self.wordsearch.grid[row][col] == rarest_letter:
                        rare_letter_positions.append((row, col))
            
            # Highlight all instances of the rare letter
            for _ in range(self.fps):  # 1 second
                frame = self.frame_generator.create_frame(
                    current_cells=set(rare_letter_positions),
                    found_words=found_so_far
                )
                frames.append(Image.fromarray(frame))
            
            # Find which position contains the word
            for pos_row, pos_col in rare_letter_positions:
                # Check if this position is part of the word we're looking for
                word_cells = []
                row, col = word_pos.start_row, word_pos.start_col
                dr, dc = word_pos.direction
                for _ in word_pos.word:
                    word_cells.append((row, col))
                    row += dr
                    col += dc
                
                if (pos_row, pos_col) in word_cells:
                    # This is the right position! Highlight it specifically
                    for _ in range(self.fps // 4):
                        frame = self.frame_generator.create_frame(
                            current_cells={(pos_row, pos_col)},
                            found_words=found_so_far
                        )
                        frames.append(Image.fromarray(frame))
                    
                    # Discover the word letter by letter
                    self._animate_word_discovery(
                        frames, word_pos,
                        {(pos_row, pos_col)},
                        found_so_far
                    )
                    break
        
        self._add_final_pause(frames)
        return frames
    
    def _animate_random_sample(self) -> List[Image.Image]:
        """Random positions being sampled."""
        frames = []
        self._add_initial_pause(frames)
        
        found_so_far = {}
        size = len(self.wordsearch.grid)
        
        # Create list of all positions
        all_positions = [(r, c) for r in range(size) for c in range(size)]
        
        # Shuffle for random sampling
        random.seed(2026)
        random.shuffle(all_positions)
        
        # Sample random positions until all words found
        for row, col in all_positions:
            # Show random sample
            frame = self.frame_generator.create_frame(
                current_cells={(row, col)},
                found_words=found_so_far
            )
            frames.append(Image.fromarray(frame))
            
            # Check if we found a word
            for word, word_pos in self.found_words.items():
                if word not in found_so_far:
                    if word_pos.start_row == row and word_pos.start_col == col:
                        self._animate_word_discovery(frames, word_pos, {(row, col)}, found_so_far)
            
            # Stop if all words found
            if len(found_so_far) == len(self.found_words):
                break
        
        self._add_final_pause(frames)
        return frames
    
    def _animate_patch_search(self) -> List[Image.Image]:
        """Show 4×4 patches being examined."""
        frames = []
        self._add_initial_pause(frames)
        
        found_so_far = {}
        size = len(self.wordsearch.grid)
        patch_size = 4
        
        # Generate overlapping patches
        for start_row in range(0, size - patch_size + 1, 2):
            for start_col in range(0, size - patch_size + 1, 2):
                # Create patch cells
                patch_cells = set()
                for r in range(start_row, start_row + patch_size):
                    for c in range(start_col, start_col + patch_size):
                        if r < size and c < size:
                            patch_cells.add((r, c))
                
                # Show entire patch highlighted
                for _ in range(self.fps // 2):  # 0.5 seconds per patch
                    frame = self.frame_generator.create_frame(
                        current_cells=patch_cells,
                        found_words=found_so_far
                    )
                    frames.append(Image.fromarray(frame))
                
                # Check if any words start in this patch
                for word, word_pos in self.found_words.items():
                    if word not in found_so_far:
                        if (word_pos.start_row, word_pos.start_col) in patch_cells:
                            self._animate_word_discovery(frames, word_pos, patch_cells, found_so_far)
        
        self._add_final_pause(frames)
        return frames
    
    def _animate_random_to_ordered(self) -> List[Image.Image]:
        """Random sampling phase, then switch to systematic."""
        frames = []
        self._add_initial_pause(frames)
        
        found_so_far = {}
        size = len(self.wordsearch.grid)
        
        # Phase 1: Random sampling (find ~half the words)
        all_positions = [(r, c) for r in range(size) for c in range(size)]
        random.seed(2026)
        random.shuffle(all_positions)
        
        target_words = len(self.found_words) // 2
        
        for row, col in all_positions:
            frame = self.frame_generator.create_frame(
                current_cells={(row, col)},
                found_words=found_so_far
            )
            frames.append(Image.fromarray(frame))
            
            for word, word_pos in self.found_words.items():
                if word not in found_so_far:
                    if word_pos.start_row == row and word_pos.start_col == col:
                        self._animate_word_discovery(frames, word_pos, {(row, col)}, found_so_far)
            
            if len(found_so_far) >= target_words:
                break
        
        # Phase 2: Ordered scan for remaining words
        for row in range(size):
            for col in range(size):
                frame = self.frame_generator.create_frame(
                    current_cells={(row, col)},
                    found_words=found_so_far
                )
                frames.append(Image.fromarray(frame))
                
                for word, word_pos in self.found_words.items():
                    if word not in found_so_far:
                        if word_pos.start_row == row and word_pos.start_col == col:
                            self._animate_word_discovery(frames, word_pos, {(row, col)}, found_so_far)
            
            if len(found_so_far) == len(self.found_words):
                break
        
        self._add_final_pause(frames)
        return frames
