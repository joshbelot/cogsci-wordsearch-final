# Word Search Generator API Documentation

Complete reference for the word search puzzle generator classes and methods.

## Table of Contents
- [Overview](#overview)
- [Classes](#classes)
  - [WordsearchGenerator](#wordsearchgenerator)
  - [Wordsearch](#wordsearch)
- [Usage Examples](#usage-examples)
- [Advanced Features](#advanced-features)
- [Algorithm Details](#algorithm-details)

---

## Overview

This module provides two main classes:
- **`WordsearchGenerator`**: Creates word search puzzles with customizable parameters
- **`Wordsearch`**: Represents a generated puzzle with grid, word bank, and display methods

---

## Classes

### WordsearchGenerator

The main class for generating word search puzzles.

#### Constructor

```python
WordsearchGenerator(word_file: Optional[str] = None)
```

**Parameters:**
- `word_file` (optional): Path to a text file containing words (one per line)
  - If `None`, uses the default word corpus (`google-10000-english-usa-no-swears-medium.txt`)
  - Words in file should be one per line, any case (will be converted to uppercase)

**Example:**
```python
# Use default word list
generator = WordsearchGenerator()

# Use custom word list
generator = WordsearchGenerator(word_file='custom_words.txt')
```

---

#### Methods

##### `generate()`

Generates a new word search puzzle.

```python
generate(size: int, 
         min_word_length: Optional[int] = None, 
         max_word_length: Optional[int] = None) -> Wordsearch
```

**Parameters:**
- `size` (required): Grid dimensions (size × size)
  - Minimum recommended: 5
  - Maximum: Limited only by memory
  - Typical range: 10-20 for human puzzles

- `min_word_length` (optional): Minimum word length to include
  - Default: 3
  - Words shorter than this are filtered out

- `max_word_length` (optional): Maximum word length to include
  - Default: Grid size
  - Words longer than this are filtered out (they wouldn't fit)

**Returns:**
- `Wordsearch` object containing the generated puzzle

**Raises:**
- `ValueError`: If no words match the given constraints

**Example:**
```python
# Generate 10×10 puzzle with 4-8 letter words
puzzle = generator.generate(size=10, min_word_length=4, max_word_length=8)

# Generate 15×15 puzzle with default word lengths
puzzle = generator.generate(size=15)

# Small puzzle with short words
puzzle = generator.generate(size=8, min_word_length=3, max_word_length=5)
```

---

#### Class Attributes

##### `LETTER_FREQUENCIES`
```python
LETTER_FREQUENCIES: Dict[str, float]
```
Letter frequency distribution based on English language usage. Used to fill empty cells with realistic letter distributions.

```python
{
    'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97,
    'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25,
    'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36,
    'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29,
    'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10,
    'Z': 0.07
}
```

##### `DIRECTIONS`
```python
DIRECTIONS: List[Tuple[int, int]]
```
Eight possible word placement directions:
- `(0, 1)`: Horizontal right →
- `(0, -1)`: Horizontal left ←
- `(1, 0)`: Vertical down ↓
- `(-1, 0)`: Vertical up ↑
- `(1, 1)`: Diagonal down-right ↘
- `(1, -1)`: Diagonal down-left ↙
- `(-1, 1)`: Diagonal up-right ↗
- `(-1, -1)`: Diagonal up-left ↖

---

### Wordsearch

Represents a generated word search puzzle.

#### Constructor

```python
Wordsearch(grid: List[List[str]], word_bank: List[str], size: int)
```

**Note:** Typically created by `WordsearchGenerator.generate()`, not instantiated directly.

**Parameters:**
- `grid`: 2D list of letters (size × size)
- `word_bank`: List of words hidden in the puzzle
- `size`: Grid dimensions

---

#### Attributes

##### `grid`
```python
grid: List[List[str]]
```
2D array representing the puzzle grid. Each element is a single uppercase letter.

**Example:**
```python
# Access a specific cell
letter = puzzle.grid[0][0]  # Top-left corner

# Iterate through grid
for row in puzzle.grid:
    for cell in row:
        print(cell, end=' ')
    print()
```

##### `word_bank`
```python
word_bank: List[str]
```
List of words successfully placed in the puzzle. All words are uppercase.

**Example:**
```python
print(f"Find these words: {', '.join(puzzle.word_bank)}")
# Output: Find these words: PYTHON, ALGORITHM, SEARCH, PATTERN
```

##### `size`
```python
size: int
```
Grid dimensions (both width and height).

---

#### Methods

##### `display()`
```python
display() -> None
```
Prints the puzzle to console in a human-readable format.

**Example:**
```python
puzzle.display()
```
**Output:**
```
P Y T H O N A L G
O L G O R I T H M
S E A R C H P A T
...
Word Bank:
PYTHON, ALGORITHM, SEARCH, PATTERN
```

##### `__str__()`
```python
__str__() -> str
```
Returns string representation of the puzzle (used by `display()` and `print()`).

**Example:**
```python
puzzle_string = str(puzzle)
print(puzzle_string)
```

---

## Usage Examples

### Basic Example

```python
from Wordsearch_Generator import WordsearchGenerator

# Create generator
generator = WordsearchGenerator()

# Generate puzzle
puzzle = generator.generate(size=10, min_word_length=4, max_word_length=8)

# Display to user
puzzle.display()
```

### Export to File

```python
# Generate puzzle
puzzle = generator.generate(size=12)

# Save to text file
with open('puzzle.txt', 'w') as f:
    f.write(str(puzzle))
```

### Generate Multiple Puzzles

```python
# Create 10 unique puzzles
puzzles = []
for i in range(10):
    puzzle = generator.generate(size=10, min_word_length=4, max_word_length=7)
    puzzles.append(puzzle)
    
# Save each with unique filename
for i, puzzle in enumerate(puzzles):
    with open(f'puzzle_{i+1}.txt', 'w') as f:
        f.write(str(puzzle))
```

### Access Puzzle Components

```python
puzzle = generator.generate(size=10)

# Get grid dimensions
print(f"Grid size: {puzzle.size}×{puzzle.size}")

# Count words
print(f"Number of words: {len(puzzle.word_bank)}")

# List words by length
for word in sorted(puzzle.word_bank, key=len):
    print(f"{word} ({len(word)} letters)")

# Convert grid to different format
import numpy as np
grid_array = np.array(puzzle.grid)
```

### Custom Word List

```python
# Create custom word file (e.g., 'science_terms.txt')
science_words = [
    'NEURON',
    'SYNAPSE', 
    'COGNITION',
    'MEMORY',
    'ATTENTION',
    'PERCEPTION'
]

with open('science_terms.txt', 'w') as f:
    f.write('\n'.join(science_words))

# Use custom list
generator = WordsearchGenerator(word_file='science_terms.txt')
puzzle = generator.generate(size=12)
```

### Integrate with GUI or Web App

```python
def create_puzzle_json(size, min_len, max_len):
    """Create puzzle and return as JSON for web app."""
    import json
    
    generator = WordsearchGenerator()
    puzzle = generator.generate(size, min_len, max_len)
    
    return json.dumps({
        'grid': puzzle.grid,
        'words': puzzle.word_bank,
        'size': puzzle.size
    })

# Use in web framework
puzzle_data = create_puzzle_json(10, 4, 8)
```

---

## Advanced Features

### Substring Filtering

The generator automatically removes words that are substrings of other selected words.

**Example:**
If the word list contains both "CATCH" and "CAT", only "CATCH" will be included in the puzzle, preventing redundancy.

**Why?** If "CAT" is placed as a separate word, it's unlikely to overlap perfectly with "CATCH" due to random placement, making it effectively hidden inside the longer word anyway.

### Overlapping Words

Words can overlap when they share the same letter at an intersection point.

**Example:**
```
  C A T
  O
  N
  G
  O
```
"CAT" (horizontal) and "CONGO" (vertical) overlap at "C".

### Letter Frequency Distribution

Empty cells are filled using weighted random sampling based on English letter frequency:
- Common letters (E, T, A, O, I, N, S) appear more frequently
- Rare letters (Q, X, Z) appear less frequently
- Makes puzzles more natural and challenging

### Automatic Word Count Scaling

The number of words scales with grid size:
```python
# Formula (approximate)
min_words = max(3, size // 2)
max_words = max(5, size * 0.8)
actual_words = random.randint(min_words, max_words)
```

**Examples:**
- 8×8 grid: 4-6 words
- 10×10 grid: 5-8 words
- 15×15 grid: 7-12 words
- 20×20 grid: 10-16 words

---

## Algorithm Details

### Word Placement Algorithm

1. **Initialize** empty grid (size × size)
2. **Filter** words based on length constraints
3. **Select** random subset of words from corpus
4. **Remove** substring duplicates (keeps longer words)
5. **Place** each word:
   - Try random positions and directions (up to 100 attempts)
   - Check if word fits and doesn't conflict with existing letters
   - Allow overlaps only when letters match
6. **Fill** remaining empty cells with frequency-weighted random letters

### Collision Detection

A word can be placed if:
- It fits within grid boundaries
- Each cell is either:
  - Empty, OR
  - Contains the same letter the word needs

### Performance Characteristics

- **Time Complexity**: O(w × a × l) where:
  - w = number of words
  - a = max attempts per word (default: 100)
  - l = average word length
  
- **Space Complexity**: O(size²) for grid storage

- **Success Rate**: High for reasonable parameters
  - Small grids (<8) with long words may fail to place all words
  - Large grids (>15) can accommodate many words easily

### Randomization

All puzzles are truly random:
- Word selection uses `random.sample()`
- Placement uses `random.randint()` and `random.choice()`
- Filler letters use `random.choices()` with weights
- Set `random.seed()` before generation for reproducible puzzles

**Example:**
```python
import random

# Ensure reproducibility
random.seed(42)
puzzle1 = generator.generate(size=10)

random.seed(42)
puzzle2 = generator.generate(size=10)

# puzzle1 and puzzle2 will be identical
```

---

## Tips and Best Practices

### For Human Puzzles
- Use sizes 10-15 for moderate difficulty
- Set min_word_length=4 to avoid tiny words
- Set max_word_length=8 to avoid excessively long words

### For Research Studies
- Use consistent size and word length across conditions
- Set random seed for reproducible stimuli
- Generate multiple variants to avoid practice effects
- Consider word frequency when selecting custom word lists

### For Educational Use
- Smaller grids (8-10) for children
- Themed word lists (science, history, vocabulary)
- Vary difficulty by grid size, not word length

### Troubleshooting
- **Too few words placed**: Increase grid size or reduce word length constraints
- **No words fit**: Check that max_word_length <= size
- **Want more words**: Increase grid size (word count scales automatically)

---

## Word Corpus

The default word list (`google-10000-english-usa-no-swears-medium.txt`) contains:
- ~3,000 common English words
- Medium length (typically 4-10 letters)
- No profanity or offensive terms
- US English spelling

### Creating Custom Word Lists

Format: Plain text file, one word per line
```
apple
banana
cherry
```

Tips:
- Use uppercase or lowercase (will be normalized)
- One word per line
- No special characters or punctuation
- Mix of word lengths works best

---

## License

Part of the cognitive science word search research project. See main LICENSE file for details.