import pickle
import json
import os
import random
from pathlib import Path
from .generator import WordsearchGenerator, Wordsearch

def generate_a_puzzles():
    random.seed(42)
    generator = WordsearchGenerator()
    
    SIZES_A = list(range(10, 101, 5))  # [10, 15, 20, ..., 100]
    PUZZLES_PER_SIZE = 500

    part_a_puzzles = {}   # { size: [Wordsearch, ...] }
    part_a_metadata = {}  # { size: [{ puzzle_id, word_count, avg_word_length, ... }, ...] }

    for size in SIZES_A:
        puzzles = []
        metas = []
        failed = 0

        for i in range(PUZZLES_PER_SIZE):
            try:
                p = generator.generate(
                    size=size,
                    min_word_length=3,
                    max_word_length=size  # scales with grid — intentional for Part A
                )
                puzzles.append(p)
                word_lengths = [len(w) for w in p.word_bank]
                metas.append({
                    "puzzle_id": f"A_{size}x{size}_{i:04d}",
                    "size": size,
                    "word_count": len(p.word_bank),
                    "avg_word_length": sum(word_lengths) / len(word_lengths),
                    "min_word_length": min(word_lengths),
                    "max_word_length": max(word_lengths),
                })
            except Exception as e:
                failed += 1

        part_a_puzzles[size] = puzzles
        part_a_metadata[size] = metas
        print(f"Size {size:3d}x{size}: {len(puzzles)} generated, {failed} failed")

    print(f"\nPart A total: {sum(len(v) for v in part_a_puzzles.values())} puzzles")
    with open("data/part_a/puzzles.pkl", "wb") as f:
        pickle.dump(part_a_puzzles, f)

    with open("data/part_a/metadata.json", "w") as f:
        json.dump(part_a_metadata, f, indent=2)

    print("Part A saved.")
    
    
def generate_b_puzzles():
    random.seed(42)
    generator = WordsearchGenerator()
    
    # Fixed grid size — held constant so word length is the only IV
    SIZE_B = 30
    PUZZLES_PER_CONDITION = 200

    # Corpus contains only 5–8 character words; conditions are non-overlapping
    # and fully contained within the corpus range.
    WORD_LENGTH_CONDITIONS = {
        "short":  (5, 5),   # length 5 only       (1,367 words available)
        "medium": (6, 7),   # length 6–7           (2,935 words available)
        "long":   (8, 8),   # length 8 only        (1,157 words available)
    }

    part_b_puzzles = {}   # { condition_label: [Wordsearch, ...] }
    part_b_metadata = {}  # { condition_label: [{ ... }, ...] }

    for label, (min_len, max_len) in WORD_LENGTH_CONDITIONS.items():
        puzzles = []
        metas = []
        failed = 0

        for i in range(PUZZLES_PER_CONDITION):
            try:
                p = generator.generate(
                    size=SIZE_B,
                    min_word_length=min_len,
                    max_word_length=max_len
                )
                puzzles.append(p)
                word_lengths = [len(w) for w in p.word_bank]
                metas.append({
                    "puzzle_id": f"B_{label}_{i:04d}",
                    "size": SIZE_B,
                    "condition": label,
                    "min_word_length_constraint": min_len,
                    "max_word_length_constraint": max_len,
                    "word_count": len(p.word_bank),
                    "avg_word_length": sum(word_lengths) / len(word_lengths),
                    "min_word_length": min(word_lengths),
                    "max_word_length": max(word_lengths),
                })
            except Exception as e:
                failed += 1

        part_b_puzzles[label] = puzzles
        part_b_metadata[label] = metas
        print(f"Condition '{label}' ({min_len}-{max_len} letters): {len(puzzles)} generated, {failed} failed")

    print(f"\nPart B total: {sum(len(v) for v in part_b_puzzles.values())} puzzles")

    # Ensure the directory exists before writing
    import os
    os.makedirs("data/part_b", exist_ok=True)
    with open("data/part_b/puzzles.pkl", "wb") as f:
        pickle.dump(part_b_puzzles, f)

    with open("data/part_b/metadata.json", "w") as f:
        json.dump(part_b_metadata, f, indent=2)

    print("Part B saved.")
    
    

def get_part_a(force_regenerate=False):
    """Load Part A puzzles from disk, generating them first if needed."""
    path = "data/part_a/puzzles.pkl"
    if not os.path.exists(path) or force_regenerate:
        generate_a_puzzles()
    with open(path, "rb") as f:
        return pickle.load(f)
    
    
def get_part_b(force_regenerate=False):
    """Load Part B puzzles from disk, generating them first if needed."""
    path = "data/part_b/puzzles.pkl"
    if not os.path.exists(path) or force_regenerate:
        generate_b_puzzles()
    with open(path, "rb") as f:
        return pickle.load(f)    