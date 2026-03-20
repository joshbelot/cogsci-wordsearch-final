# Quick Reference Guide

## Installation & Setup
```bash
# Clone repository
git clone https://github.com/joshbelot/cogsci-wordsearch-final.git
cd cogsci-wordsearch-final

# Install dependencies
pip install -r requirements.txt
```

## Running Experiments

### Quick Test (1-2 minutes)
```bash
python run_experiments.py quick
```

### Standard Experiment (2-4 hours)
```bash
python run_experiments.py standard
```

### Generate Puzzles Only
```bash
python run_experiments.py generate --config default
```

### Analyze Existing Results
```bash
python run_experiments.py analyze
```

## File Locations

### Generated Files
- Puzzles: `experiments/data/puzzle_suite.pkl`
- Results: `experiments/results/experiment_results.csv`
- Metadata: `experiments/results/puzzle_metadata.json`
- Statistics: `experiments/results/summary_statistics.csv`
- Report: `experiments/results/analysis_report.txt`
- Checkpoint: `experiments/data/checkpoint.pkl`

## Python API Examples

### Generate Puzzle
```python
from Wordsearch_Generator import WordsearchGenerator

generator = WordsearchGenerator()
puzzle = generator.generate(size=10, min_word_length=4, max_word_length=8)
puzzle.display()
```

### Test Single Strategy
```python
from solver import Solver
from strategies import BruteForceStrategy

solver = Solver(puzzle, BruteForceStrategy())
result = solver.run_and_display()
```

### Compare Strategies
```python
from solver import compare_strategies
from strategies import BruteForceStrategy, OrderedSearchStrategy

strategies = [BruteForceStrategy(), OrderedSearchStrategy()]
results = compare_strategies(puzzle, strategies)
```

### Custom Experiment
```python
from experiments import ExperimentConfig, ExperimentRunner
from strategies import BruteForceStrategy, OrderedSearchStrategy

config = ExperimentConfig(
    grid_sizes=[10, 15],
    trials_per_config=10
)

runner = ExperimentRunner(config, [BruteForceStrategy(), OrderedSearchStrategy()])
runner.generate_or_load_puzzles()
results = runner.run_experiment()
```

### Analyze Results
```python
from experiments import ResultsAnalyzer

analyzer = ResultsAnalyzer.from_csv("experiments/results/experiment_results.csv")

# Compare strategies
print(analyzer.compare_strategies('execution_time'))
print(analyzer.compare_strategies('success_rate'))

# Performance by grid size
print(analyzer.strategy_performance_by_grid_size('execution_time'))

# Generate report
analyzer.generate_report("my_report.txt")
```

## Experiment Configurations

### QUICK_TEST_CONFIG
- 2 grid sizes × 2 word ranges × 2 densities × 5 trials = 40 puzzles
- 40 puzzles × 6 strategies = 240 trials
- Time: ~1-2 minutes

### DEFAULT_CONFIG
- 5 grid sizes × 4 word ranges × 3 densities × 30 trials = 1,800 puzzles
- 1,800 puzzles × 6 strategies = 10,800 trials
- Time: ~2-4 hours

### COMPREHENSIVE_CONFIG
- 6 grid sizes × 4 word ranges × 3 densities × 50 trials = 3,600 puzzles
- 3,600 puzzles × 6 strategies = 21,600 trials
- Time: ~6-12 hours

## Strategies

1. **BruteForceStrategy** - Baseline exhaustive search
2. **OrderedSearchStrategy** - Gestalt-based top→bottom, left→right
3. **UncommonLetterSearchStrategy** - Prioritizes rare letters (Q, Z, X, J)
4. **RandomSampleStrategy** - Monte Carlo sampling
5. **PatchSearchStrategy** - Local region search
6. **RandomToOrderedStrategy** - Hybrid strategy

## Metrics Collected

### Primary
- `execution_time` - Time in seconds
- `cells_examined` - Number of cells checked
- `words_found` - Number of words found
- `success_rate` - Percentage (0-1)

### Derived
- `efficiency_ratio` - words_found / cells_examined
- `time_per_word` - execution_time / words_found
- `cells_per_second` - Throughput
- `found_all_words` - Boolean completeness

### Additional
- `memory_usage_mb` - Peak memory
- `timed_out` - Exceeded timeout
- `error_occurred` - Had an error

## Troubleshooting

### Import errors (pandas/numpy)
```bash
pip install pandas numpy
```

### Experiment too slow
- Use quick mode: `python run_experiments.py quick`
- Reduce trials: Modify config `trials_per_config = 10`
- Disable memory tracking: `config.enable_memory_tracking = False`

### Resume from interruption
Just run the same command again:
```bash
python run_experiments.py standard  # Automatically resumes
```

### Clear checkpoint
```bash
rm experiments/data/checkpoint.pkl
```

## Directory Structure
```
cogsci-wordsearch-final/
├── run_experiments.py          # Main entry point
├── solver.py                   # Strategy runner
├── Strategy.py                 # Base strategy class
├── strategies/                 # Strategy implementations
├── experiments/                # Experiments framework
│   ├── experiment_config.py
│   ├── puzzle_generator.py
│   ├── metrics_collector.py
│   ├── experiment_runner.py
│   ├── results_analyzer.py
│   ├── data/                   # Generated puzzles
│   ├── results/                # Experiment outputs
│   └── plots/                  # Visualizations
└── Wordsearch_Generator/       # Puzzle generation
```

## Key Features

✅ Fixed puzzle sets (same puzzles for all strategies)  
✅ Multiple trials for statistical power  
✅ Checkpoint/resume support  
✅ Comprehensive metrics beyond time  
✅ Automated statistical analysis  
✅ Reproducible (seeded random generation)  

## For More Details

- [Main README](README.md)
- [Experiments Documentation](experiments/README.md)
- [Generator Documentation](Wordsearch_Generator/README.md)
