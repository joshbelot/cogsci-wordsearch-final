#!/usr/bin/env python3
"""
Generate animated GIFs for all 6 word search strategies.

This script creates visualizations showing how each strategy searches
through a fixed 10×10 word search puzzle.

Usage:
    python generate_strategy_animations.py
    python generate_strategy_animations.py --strategy brute_force
    python generate_strategy_animations.py --fps 10 --skip 2
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import argparse
from Wordsearch_Generator import WordsearchGenerator
from strategies import (
    BruteForceStrategy,
    OrderedSearchStrategy,
    UncommonLetterSearchStrategy,
    RandomSampleStrategy,
    PatchSearchStrategy,
    RandomToOrderedStrategy
)
from visualizations import ConceptualAnimator


def generate_fixed_puzzle():
    """
    Generate a fixed 10×10 word search puzzle for visualization.
    
    Returns:
        Wordsearch object
    """
    print("Generating 10×10 word search puzzle...")
    
    # Try different seed for more common/interesting words
    import random
    random.seed(12345)
    
    generator = WordsearchGenerator()
    
    # Generate a 10×10 puzzle with good visual words
    puzzle = generator.generate(size=10, min_word_length=4, max_word_length=7)
    
    print(f"  Grid size: 10×10")
    print(f"  Words: {', '.join(puzzle.word_bank)}")
    print()
    
    return puzzle


def generate_animation_for_strategy(strategy, puzzle, output_dir, fps=8):
    """
    Generate conceptual animation for a single strategy.
    
    Args:
        strategy: Strategy instance to visualize
        puzzle: Wordsearch puzzle to solve
        output_dir: Directory to save GIF
        fps: Frames per second
    """
    # Create output filename
    strategy_name = strategy.get_name()
    filename = strategy_name.lower().replace(' ', '_').replace('(', '').replace(')', '').replace('=', '') + '.gif'
    output_path = os.path.join(output_dir, filename)
    
    print(f"\n{'='*60}")
    print(f"STRATEGY: {strategy_name}")
    print(f"{'='*60}")
    
    # Generate conceptual animation
    animator = ConceptualAnimator(puzzle, strategy, fps)
    animator.generate_animation(output_path, verbose=True)
    
    print()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Generate animated GIFs for word search strategies'
    )
    parser.add_argument(
        '--strategy',
        choices=['brute_force', 'ordered', 'uncommon', 'random', 'patch', 'hybrid', 'all'],
        default='all',
        help='Which strategy to animate (default: all)'
    )
    parser.add_argument(
        '--fps',
        type=int,
        default=8,
        help='Frames per second (default: 8)'
    )
    parser.add_argument(
        '--output-dir',
        default='visualizations/outputs',
        help='Output directory for GIFs'
    )
    
    args = parser.parse_args()
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Generate fixed puzzle
    puzzle = generate_fixed_puzzle()
    
    # Display puzzle
    print("Puzzle grid:")
    puzzle.display()
    print()
    
    # Initialize strategies
    strategies = {
        'brute_force': BruteForceStrategy(),
        'ordered': OrderedSearchStrategy(),
        'uncommon': UncommonLetterSearchStrategy(),
        'random': RandomSampleStrategy(max_attempts=1000),
        'patch': PatchSearchStrategy(),
        'hybrid': RandomToOrderedStrategy(),
    }
    
    # Generate animations
    if args.strategy == 'all':
        print(f"Generating conceptual animations for all 6 strategies...")
        print(f"Settings: {args.fps} fps")
        print()
        
        for strategy in strategies.values():
            generate_animation_for_strategy(
                strategy,
                puzzle,
                args.output_dir,
                args.fps
            )
    else:
        strategy = strategies[args.strategy]
        generate_animation_for_strategy(
            strategy,
            puzzle,
            args.output_dir,
            args.fps
        )
    
    print(f"\n{'='*60}")
    print("ALL ANIMATIONS COMPLETE!")
    print(f"{'='*60}")
    print(f"Output directory: {args.output_dir}")
    print(f"Generated files:")
    for filename in sorted(os.listdir(args.output_dir)):
        if filename.endswith('.gif'):
            filepath = os.path.join(args.output_dir, filename)
            size = os.path.getsize(filepath) / (1024 * 1024)
            print(f"  - {filename} ({size:.2f} MB)")
    print()


if __name__ == '__main__':
    main()
