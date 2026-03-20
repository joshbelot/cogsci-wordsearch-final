# Cognitive Science Word Search Project

A cognitive science research project exploring memory, pattern recognition, and visual search behavior through word search puzzles. This project generates customizable word search puzzles and includes tools for analyzing participant performance.

## 🎯 Project Overview

This project investigates how humans find and recognize words in visual search tasks. Word search puzzles provide an ideal environment to study:
- **Visual scanning strategies**
- **Pattern recognition**
- **Working memory capacity**
- **Attention mechanisms**
- **Learning effects over time**

## 📁 Project Structure

```
cogsci-wordsearch-final/
├── README.md                          # Main project documentation
├── run_experiments.py                 # Main script to run experiments
├── Wordsearch_Generator/              # Word search generation module
│   ├── README.md                      # Generator-specific documentation
│   ├── Wordsearch.py                  # Core classes
│   ├── __init__.py                    # Package initialization
│   └── google-10000-english-usa-no-swears-medium.txt  # Default word corpus
├── strategies/                        # Solving strategy implementations
│   ├── brute_force.py                 # Exhaustive search strategy
│   ├── ordered_search.py              # Gestalt-based ordered strategy
│   ├── uncommon_letter_search.py      # Rare letter prioritization
│   ├── random_sample.py               # Monte Carlo sampling
│   ├── patch_search.py                # Local region search
│   └── random_to_ordered.py           # Hybrid strategy
├── experiments/                       # Experimentation framework
│   ├── README.md                      # Experiments documentation
│   ├── experiment_config.py           # Configuration classes
│   ├── puzzle_generator.py            # Puzzle suite generation
│   ├── metrics_collector.py           # Performance metrics
│   ├── experiment_runner.py           # Main orchestrator
│   ├── results_analyzer.py            # Statistical analysis
│   ├── data/                          # Generated puzzle suites
│   ├── results/                       # Experiment outputs
│   └── plots/                         # Visualizations
├── solver.py                          # Strategy execution wrapper
├── Strategy.py                        # Base strategy interface
├── testing_nb.ipynb                   # Testing and experimentation notebook
└── Cog_Sci_Term_Project_Pitch.pdf    # Project proposal
```

## 🚀 Quick Start

### Installation

1. Clone the repository:
```bash
git clone https://github.com/joshbelot/cogsci-wordsearch-final.git
cd cogsci-wordsearch-final
```

2. Install Python 3.7 or higher

3. Install dependencies (for experiments framework):
```bash
pip install -r requirements.txt
```

> **Note**: The word search generator has no dependencies and uses only Python standard library. The experiments framework requires `pandas` and `numpy` for data analysis.

### Basic Usage

```python
from Wordsearch_Generator import WordsearchGenerator

# Create a generator with the default word list
generator = WordsearchGenerator()

# Generate a 10x10 puzzle with 4-8 letter words
puzzle = generator.generate(size=10, min_word_length=4, max_word_length=8)

# Display the puzzle
puzzle.display()

# Access puzzle components
print(f"Grid: {puzzle.grid}")
print(f"Words to find: {puzzle.word_bank}")
print(f"Size: {puzzle.size}")
```

## 🎲 Features

### Word Search Generator
- **Flexible sizing**: Generate puzzles from small (5×5) to large (50×50+)
- **Custom word lists**: Use default corpus or provide your own word file
- **Length constraints**: Filter words by minimum and maximum length
- **8-directional placement**: Words can be horizontal, vertical, diagonal, and backwards
- **Intelligent overlapping**: Words can overlap when they share common letters
- **Frequency-based filling**: Empty cells filled using English letter frequency distribution
- **Substring filtering**: Automatically removes words that are substrings of other selected words

### Smart Features
- **Natural letter distribution**: Filler letters chosen based on English language frequency (E appears ~12.7%, Z appears ~0.07%)
- **Automatic word count**: Scales intelligently with puzzle size
- **Collision handling**: Allows overlapping words with matching letters
- **Random selection**: Each puzzle is unique with randomly selected words from the corpus

## 🧬 Solving Strategies

This project implements 6 cognitive-inspired strategies for solving word search puzzles:

1. **Brute Force** - Systematic exhaustive search (baseline)
2. **Ordered Search** - Gestalt-based top-to-bottom, left-to-right scanning
3. **Uncommon Letter Search** - Prioritizes rare letters (Q, Z, X, J) as anchors
4. **Random Sample** - Monte Carlo sampling approach
5. **Patch Search** - Local region-based searching
6. **Random to Ordered** - Hybrid random/systematic strategy

Each strategy models different aspects of human visual search behavior and cognitive processing.

## 🔬 Experiments Framework

### Quick Start with Experiments

Run a quick test to compare all strategies:
```bash
python run_experiments.py quick
```

Run the full standard experiment (~2-4 hours):
```bash
python run_experiments.py standard
```

Analyze results:
```bash
python run_experiments.py analyze
```

### What Gets Measured

The experiments framework provides ML-style rigorous evaluation:

- **Fixed puzzle sets** - All strategies tested on identical puzzles
- **Multiple trials** - 30+ trials per configuration for statistical power
- **Comprehensive metrics** - Time, efficiency, success rate, memory usage
- **Systematic variation** - Tests across grid sizes, word lengths, densities
- **Statistical analysis** - Automated reporting with comparisons

**Default experiment**: 1,800 puzzles × 6 strategies = 10,800 trials

### Key Features

✅ **Reproducible** - Seeded random generation  
✅ **Checkpoint/Resume** - Auto-saves progress every 50 puzzles  
✅ **Comprehensive metrics** - Beyond just execution time  
✅ **Statistical rigor** - Multiple trials, paired comparisons  
✅ **Automated analysis** - Generate reports and visualizations  

For complete documentation, see [Experiments Documentation](experiments/README.md)

## 📚 Documentation

For detailed API documentation and advanced usage, see:
- [Word Search Generator Documentation](Wordsearch_Generator/README.md)
- [Experiments Framework Documentation](experiments/README.md)

## 🧪 Research Applications

This tool can be used for cognitive science research in several ways:
1. **Difficulty manipulation**: Control puzzle complexity via size and word length
2. **Stimulus generation**: Create consistent, reproducible stimuli for experiments
3. **Individual differences**: Study how different populations approach visual search tasks
4. **Training studies**: Generate multiple puzzles to study learning effects
5. **Eye-tracking studies**: Analyze visual search patterns and strategies

## 📖 Example Use Cases

### Generate Multiple Difficulty Levels
```python
generator = WordsearchGenerator()

# Easy: Small grid, short words
easy_puzzle = generator.generate(size=8, min_word_length=3, max_word_length=5)

# Medium: Standard grid
medium_puzzle = generator.generate(size=12, min_word_length=4, max_word_length=8)

# Hard: Large grid, longer words
hard_puzzle = generator.generate(size=15, min_word_length=6, max_word_length=12)
```

### Use Custom Word List
```python
# Create a themed word search (e.g., psychology terms)
generator = WordsearchGenerator(word_file='psychology_terms.txt')
puzzle = generator.generate(size=10)
```

## 🤝 Contributing

This is a research project. For questions or collaborations, please open an issue or contact the repository owner.

## 📄 License

See [LICENSE](LICENSE) file for details.

## 👥 Authors

- Josh Belot - Georgia Tech Cognitive Science

## 🙏 Acknowledgments

- Word corpus derived from Google's 10,000 most common English words
- Letter frequency statistics based on English language analysis