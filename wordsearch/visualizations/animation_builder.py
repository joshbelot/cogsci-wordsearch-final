"""
Animation builder for creating GIFs from strategy visualization frames.
"""

from typing import List, Dict
from PIL import Image
import numpy as np
from .frame_generator import FrameGenerator
from .tracking_strategy import TrackingStrategy
from ..generator import Wordsearch


class AnimationBuilder:
    """
    Builds animated GIFs from strategy tracking data.
    
    Creates smooth animations showing:
    1. Initial puzzle (2 seconds)
    2. Search progression (red highlights on examined cells)
    3. Found words highlighted in green
    4. Final state (2 seconds)
    """
    
    def __init__(self, 
                 wordsearch: Wordsearch,
                 tracking_strategy: TrackingStrategy,
                 fps: int = 8,
                 skip_frames: int = 1):
        """
        Initialize animation builder.
        
        Args:
            wordsearch: The puzzle being solved
            tracking_strategy: Strategy wrapper with tracking data
            fps: Frames per second for the animation
            skip_frames: Show every Nth cell examination (1 = show all, 2 = show half)
        """
        self.wordsearch = wordsearch
        self.tracking_strategy = tracking_strategy
        self.fps = fps
        self.skip_frames = skip_frames
        
        self.frame_generator = FrameGenerator(
            wordsearch, 
            tracking_strategy.get_name()
        )
        
    def build_animation(self, output_path: str, verbose: bool = True):
        """
        Build the complete animation and save as GIF.
        
        Args:
            output_path: Path to save the GIF file
            verbose: Print progress messages
        """
        if verbose:
            print(f"Building animation for {self.tracking_strategy.get_name()}...")
        
        frames = []
        tracking_data = self.tracking_strategy.get_tracking_data()
        cell_examinations = tracking_data['cell_examinations']
        word_found_at_step = tracking_data['word_found_at_step']
        found_words = tracking_data['found_words']
        
        # 1. Initial frame (show puzzle for 2 seconds)
        initial_frame = self.frame_generator.create_initial_frame()
        initial_frame_count = self.fps * 2  # 2 seconds
        for _ in range(initial_frame_count):
            frames.append(Image.fromarray(initial_frame))
        
        if verbose:
            print(f"  Added {initial_frame_count} initial frames")
        
        # 2. Search progression frames
        current_found_words = {}
        
        for step, (row, col) in enumerate(cell_examinations):
            # Skip frames for speed control
            if step % self.skip_frames != 0:
                continue
            
            # Check if any words were found at this step
            for word, found_step in word_found_at_step.items():
                if found_step <= step and word not in current_found_words:
                    current_found_words[word] = found_words[word]
            
            # Create frame with current cell and found words
            frame = self.frame_generator.create_frame(
                current_cell=(row, col),
                found_words=current_found_words
            )
            frames.append(Image.fromarray(frame))
        
        if verbose:
            total_steps = len(cell_examinations)
            frames_generated = len(cell_examinations) // self.skip_frames
            print(f"  Added {frames_generated} search frames ({total_steps} cells examined)")
        
        # 3. Final frame (show result for 2 seconds)
        final_frame = self.frame_generator.create_final_frame(found_words)
        final_frame_count = self.fps * 2  # 2 seconds
        for _ in range(final_frame_count):
            frames.append(Image.fromarray(final_frame))
        
        if verbose:
            print(f"  Added {final_frame_count} final frames")
        
        # Save as GIF
        if frames:
            duration = int(1000 / self.fps)  # milliseconds per frame
            frames[0].save(
                output_path,
                save_all=True,
                append_images=frames[1:],
                duration=duration,
                loop=0  # Loop forever
            )
            
            if verbose:
                file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
                animation_length = len(frames) / self.fps
                print(f"  ✓ Saved to {output_path}")
                print(f"    Total frames: {len(frames)}")
                print(f"    Duration: {animation_length:.1f} seconds")
                print(f"    File size: {file_size:.2f} MB")
                print(f"    Words found: {len(found_words)}")
        else:
            print(f"  ✗ No frames generated!")
    
    @staticmethod
    def generate_animation(wordsearch: Wordsearch,
                          strategy,
                          output_path: str,
                          fps: int = 8,
                          skip_frames: int = 1,
                          verbose: bool = True):
        """
        Convenience method to generate animation from a strategy.
        
        Args:
            wordsearch: The puzzle to solve
            strategy: The strategy to visualize
            output_path: Path to save the GIF
            fps: Frames per second
            skip_frames: Show every Nth cell (1 = all, 2 = half, etc.)
            verbose: Print progress
        """
        # Wrap strategy with tracking
        tracking_strategy = TrackingStrategy(strategy)
        
        # Solve the puzzle
        if verbose:
            print(f"Solving with {strategy.get_name()}...")
        result = tracking_strategy.solve(wordsearch)
        
        if verbose:
            print(f"  Found {len(result.found_words)} words")
            print(f"  Examined {result.cells_examined} cells")
            print(f"  Time: {result.execution_time:.3f}s")
        
        # Build animation
        builder = AnimationBuilder(wordsearch, tracking_strategy, fps, skip_frames)
        builder.build_animation(output_path, verbose)
