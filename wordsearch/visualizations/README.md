# Strategy Visualization System

Generate animated GIFs showing how each word search strategy works.

## Overview

This visualization system creates animations that demonstrate the search patterns of all 6 cognitive-inspired strategies:

1. **Brute Force** - Systematic exhaustive search
2. **Ordered Search** - Top-to-bottom, left-to-right scanning
3. **Uncommon Letter Search** - Prioritizes rare letters as anchors
4. **Random Sample** - Monte Carlo sampling approach
5. **Patch Search** - Local region-based searching
6. **Random to Ordered** - Hybrid random/systematic strategy

## Animation Features

- **Red highlighting**: Current cell being examined
- **Green highlighting**: Found words
- **Fixed puzzle**: Same 10×10 puzzle across all strategies for fair comparison
- **Adjustable speed**: Control frames per second and frame skipping

## Quick Start

### Generate All 6 Animations

```bash
python generate_strategy_animations.py
```

This creates GIFs in `visualizations/outputs/`:
- `brute_force.gif`
- `ordered_search.gif`
- `uncommon_letter_search.gif`
- `random_sample.gif`
- `patch_search.gif`
- `random_to_ordered.gif`

### Generate Single Strategy

```bash
python generate_strategy_animations.py --strategy brute_force
```

Options: `brute_force`, `ordered`, `uncommon`, `random`, `patch`, `hybrid`

## Customization

### Adjust Animation Speed

```bash
# Faster animation (10 fps)
python generate_strategy_animations.py --fps 10

# Skip more frames for faster playback (show every 20th cell)
python generate_strategy_animations.py --skip 20

# Combine both
python generate_strategy_animations.py --fps 15 --skip 15
```

### Change Output Directory

```bash
python generate_strategy_animations.py --output-dir my_animations/
```

## How It Works

### 1. Tracking Strategy Wrapper

Wraps any strategy and records every cell examination by intercepting grid access:

```python
from visualizations import TrackingStrategy
from strategies import BruteForceStrategy

strategy = BruteForceStrategy()
tracking_strategy = TrackingStrategy(strategy)
result = tracking_strategy.solve(puzzle)

# Get tracking data
data = tracking_strategy.get_tracking_data()
# data['cell_examinations'] = [(row, col), ...]
# data['word_found_at_step'] = {word: step_number, ...}
```

### 2. Frame Generator

Creates visual frames using matplotlib:

```python
from visualizations import FrameGenerator

frame_gen = FrameGenerator(wordsearch, "Brute Force")
frame = frame_gen.create_frame(
    current_cell=(5, 3),  # Red highlight
    found_words={...}      # Green highlights
)
```

### 3. Animation Builder

Combines frames into GIF:

```python
from visualizations import AnimationBuilder

AnimationBuilder.generate_animation(
    wordsearch=puzzle,
    strategy=strategy,
    output_path="my_animation.gif",
    fps=8,
    skip_frames=1
)
```

## File Structure

```
visualizations/
├── __init__.py              # Module exports
├── tracking_strategy.py     # TrackingStrategy wrapper
├── frame_generator.py       # FrameGenerator for matplotlib frames
├── animation_builder.py     # AnimationBuilder for GIF creation
└── outputs/                 # Generated GIF files
    ├── brute_force.gif
    ├── ordered_search.gif
    ├── uncommon_letter_search.gif
    ├── random_sample.gif
    ├── patch_search.gif
    └── random_to_ordered.gif
```

## Dependencies

```bash
pip install matplotlib Pillow
```

Already included in `requirements.txt`:
- `matplotlib>=3.3.0` - Frame rendering
- `Pillow>=8.0.0` - GIF creation

## Animation Structure

Each animation consists of:

1. **Initial frames** (2 seconds) - Shows the puzzle grid
2. **Search frames** (variable) - Red highlights showing search progression
3. **Final frames** (2 seconds) - Shows all found words in green

## Performance Tips

### Large Animations

Some strategies examine many cells (especially Brute Force). For faster generation and smaller files:

```bash
# Skip every 20th frame
python generate_strategy_animations.py --skip 20
```

### File Sizes

Typical file sizes at 8 fps:
- **Brute Force**: ~0.5-2 MB (many cells examined)
- **Ordered Search**: ~0.5-2 MB (systematic scan)
- **Uncommon Letter**: ~0.3-0.8 MB (fewer cells)
- **Random Sample**: ~0.2-0.5 MB (stochastic)
- **Patch Search**: ~0.3-0.8 MB (region-based)
- **Random to Ordered**: ~0.4-1 MB (hybrid)

## Using in Streamlit

These GIFs can be embedded directly in Streamlit apps:

```python
import streamlit as st

st.title("Word Search Strategies")
st.image("visualizations/outputs/brute_force.gif")
st.image("visualizations/outputs/ordered_search.gif")
# ... etc
```

## Programmatic Usage

### Custom Puzzle

```python
from Wordsearch_Generator import WordsearchGenerator
from strategies import BruteForceStrategy
from visualizations import AnimationBuilder

# Generate custom puzzle
generator = WordsearchGenerator()
puzzle = generator.generate(size=10, min_word_length=4, max_word_length=8)

# Create animation
strategy = BruteForceStrategy()
AnimationBuilder.generate_animation(
    puzzle,
    strategy,
    "custom_animation.gif",
    fps=10,
    skip_frames=5
)
```

### Multiple Strategies Comparison

```python
from strategies import *

strategies = [
    BruteForceStrategy(),
    OrderedSearchStrategy(),
    UncommonLetterSearchStrategy(),
]

for strategy in strategies:
    filename = f"{strategy.get_name().lower().replace(' ', '_')}.gif"
    AnimationBuilder.generate_animation(puzzle, strategy, filename)
```

## Troubleshooting

### ModuleNotFoundError: No module named 'matplotlib'

```bash
pip install matplotlib Pillow
```

### GIFs too large

Increase `--skip` parameter to reduce frame count:

```bash
python generate_strategy_animations.py --skip 20  # Show every 20th cell
```

### Animation too fast/slow

Adjust `--fps`:

```bash
python generate_strategy_animations.py --fps 5   # Slower
python generate_strategy_animations.py --fps 15  # Faster
```

## Next Steps

1. **Generate all animations**: `python generate_strategy_animations.py`
2. **Review GIFs**: Check `visualizations/outputs/`
3. **Integrate with Streamlit**: Use GIFs in your frontend
4. **Customize**: Adjust fps/skip for optimal viewing

Perfect for demonstrating cognitive science concepts visually! 🎓
