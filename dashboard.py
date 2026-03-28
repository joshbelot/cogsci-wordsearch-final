"""
Wordsearch Strategy Explorer — Streamlit Dashboard

Run with:
    streamlit run dashboard.py
"""

import io
import tempfile
import time
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

from wordsearch.generator import WordsearchGenerator
from wordsearch.strategies import (
    BruteForceStrategy,
    OrderedSearchStrategy,
    UncommonLetterSearchStrategy,
    RandomSampleStrategy,
    PatchSearchStrategy,
    RandomToOrderedStrategy,
)

# ── constants ────────────────────────────────────────────────────────────────

STRATEGY_MAP = {
    "Brute Force":              lambda: BruteForceStrategy(),
    "Ordered Search":           lambda: OrderedSearchStrategy(),
    "Uncommon Letter Search":   lambda: UncommonLetterSearchStrategy(),
    "Random Sample":            lambda: RandomSampleStrategy(max_attempts=5000),
    "Patch Search":             lambda: PatchSearchStrategy(),
    "Random to Ordered":        lambda: RandomToOrderedStrategy(),
}

DEFAULT_SIZES = [10, 15, 20]

# ── helpers ───────────────────────────────────────────────────────────────────

def run_experiment(
    generator: WordsearchGenerator,
    sizes: list[int],
    puzzles_per_size: int,
    strategy_names: list[str],
    min_word_len: int,
    max_word_len_mode: str,
    progress_bar,
    status_text,
) -> pd.DataFrame:
    """Generate puzzles and run selected strategies; return results DataFrame."""
    rows = []
    strategies = [STRATEGY_MAP[n]() for n in strategy_names]

    total_steps = len(sizes) * puzzles_per_size
    step = 0

    for size in sizes:
        max_word_len = size if max_word_len_mode == "Scale with grid (up to size)" else min(10, size)
        failed = 0

        for i in range(puzzles_per_size):
            step += 1
            progress_bar.progress(step / total_steps)
            status_text.text(f"Generating {size}×{size} puzzle {i+1}/{puzzles_per_size}…")

            try:
                puzzle = generator.generate(
                    size=size,
                    min_word_length=min_word_len,
                    max_word_length=max(min_word_len + 1, max_word_len),
                )
            except Exception:
                failed += 1
                continue

            puzzle_id = f"{size}x{size}_{i:04d}"
            word_lengths = [len(w) for w in puzzle.word_bank]
            avg_word_length = sum(word_lengths) / len(word_lengths) if word_lengths else 0

            for strategy in strategies:
                try:
                    result = strategy.solve(puzzle)
                    rows.append({
                        "puzzle_id":        puzzle_id,
                        "strategy":         result.strategy_name,
                        "size":             size,
                        "word_count":       result.total_words,
                        "avg_word_length":  avg_word_length,
                        "cells_examined":   result.cells_examined,
                        "execution_time":   result.execution_time,
                        "words_found":      result.words_found_count,
                        "total_words":      result.total_words,
                        "success_rate":     result.success_rate,
                    })
                except Exception:
                    pass

    status_text.text("Done!")
    progress_bar.progress(1.0)
    return pd.DataFrame(rows)


def fig_to_bytes(fig) -> bytes:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=150)
    buf.seek(0)
    return buf.getvalue()


# ── plots ─────────────────────────────────────────────────────────────────────

def plot_time_vs_size(df: pd.DataFrame):
    mean_time = df.groupby(["strategy", "size"])["execution_time"].mean().reset_index()
    fig, ax = plt.subplots(figsize=(10, 5))
    for strategy, group in mean_time.groupby("strategy"):
        ax.plot(group["size"], group["execution_time"], marker="o", markersize=4, label=strategy)
    ax.set_xlabel("Grid Size (n×n)")
    ax.set_ylabel("Mean Execution Time (s)")
    ax.set_title("Mean Execution Time vs Puzzle Size")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig


def plot_speedup(df: pd.DataFrame):
    mean_time = df.groupby(["strategy", "size"])["execution_time"].mean().reset_index()
    brute = mean_time[mean_time["strategy"].str.contains("Brute", case=False)][
        ["size", "execution_time"]
    ].rename(columns={"execution_time": "bf_time"})
    if brute.empty:
        return None
    rel = mean_time.merge(brute, on="size")
    rel["speedup"] = rel["bf_time"] / rel["execution_time"].replace(0, np.nan)
    non_bf = rel[~rel["strategy"].str.contains("Brute", case=False)]

    fig, ax = plt.subplots(figsize=(10, 5))
    for strategy, group in non_bf.groupby("strategy"):
        ax.plot(group["size"], group["speedup"], marker="o", markersize=4, label=strategy)
    ax.axhline(1, color="gray", linestyle="--", label="Brute Force baseline")
    ax.set_xlabel("Grid Size (n×n)")
    ax.set_ylabel("Speedup vs Brute Force (×)")
    ax.set_title("Speedup Relative to Brute Force")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig


def plot_cells_examined(df: pd.DataFrame):
    mean_cells = df.groupby(["strategy", "size"])["cells_examined"].mean().reset_index()
    mean_cells["grid_cells"] = mean_cells["size"] ** 2
    mean_cells["fraction"] = mean_cells["cells_examined"] / mean_cells["grid_cells"]

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    for strategy, group in mean_cells.groupby("strategy"):
        axes[0].plot(group["size"], group["cells_examined"], marker="o", markersize=3, label=strategy)
    axes[0].set_xlabel("Grid Size (n×n)")
    axes[0].set_ylabel("Mean Cells Examined")
    axes[0].set_title("Cells Examined vs Puzzle Size")
    axes[0].legend(fontsize=8)
    axes[0].grid(True, alpha=0.3)

    for strategy, group in mean_cells.groupby("strategy"):
        axes[1].plot(group["size"], group["fraction"], marker="o", markersize=3, label=strategy)
    axes[1].set_xlabel("Grid Size (n×n)")
    axes[1].set_ylabel("Fraction of Grid Scanned")
    axes[1].set_title("Fraction of Grid Scanned vs Puzzle Size")
    axes[1].legend(fontsize=8)
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    return fig


def plot_success_rate(df: pd.DataFrame):
    sr = df.groupby(["strategy", "size"])["success_rate"].mean().reset_index()
    fig, ax = plt.subplots(figsize=(10, 5))
    for strategy, group in sr.groupby("strategy"):
        ax.plot(group["size"], group["success_rate"] * 100, marker="o", markersize=4, label=strategy)
    ax.set_xlabel("Grid Size (n×n)")
    ax.set_ylabel("Mean Success Rate (%)")
    ax.set_ylim(0, 105)
    ax.axhline(100, color="gray", linestyle="--", alpha=0.5)
    ax.set_title("Mean Success Rate vs Puzzle Size")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig


def plot_strategy_summary_bars(df: pd.DataFrame):
    summary = df.groupby("strategy").agg(
        mean_time=("execution_time", "mean"),
        mean_cells=("cells_examined", "mean"),
        mean_success=("success_rate", "mean"),
    ).reset_index().sort_values("mean_time")

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    colors = plt.cm.tab10.colors

    strats = summary["strategy"].tolist()
    x = range(len(strats))

    for ax, col, title, ylabel in [
        (axes[0], "mean_time",    "Mean Execution Time",  "Time (s)"),
        (axes[1], "mean_cells",   "Mean Cells Examined",  "Cells"),
        (axes[2], "mean_success", "Mean Success Rate",    "Rate (0–1)"),
    ]:
        bars = ax.bar(x, summary[col], color=colors[: len(strats)])
        ax.set_xticks(x)
        ax.set_xticklabels(strats, rotation=30, ha="right", fontsize=8)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.grid(True, alpha=0.3, axis="y")

    plt.tight_layout()
    return fig


def plot_box_execution_time(df: pd.DataFrame):
    strategies = sorted(df["strategy"].unique())
    data = [df[df["strategy"] == s]["execution_time"].values for s in strategies]
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.boxplot(data, labels=strategies, patch_artist=True)
    ax.set_ylabel("Execution Time (s)")
    ax.set_title("Execution Time Distribution per Strategy")
    plt.xticks(rotation=30, ha="right", fontsize=8)
    ax.grid(True, alpha=0.3, axis="y")
    plt.tight_layout()
    return fig


# ── app layout ────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Wordsearch Strategy Explorer",
    page_icon=None,
    layout="wide",
)

st.title("Wordsearch Strategy Explorer")
st.caption(
    "Generate word search puzzles, benchmark solving strategies, and analyze the results."
)

# ─── Sidebar: configuration ───────────────────────────────────────────────────
with st.sidebar:
    st.header("Experiment Setup")

    # 1. Optional word corpus upload
    st.subheader("1. Word Corpus")
    uploaded_corpus = st.file_uploader(
        "Upload a custom word list (.txt, one word per line)",
        type=["txt"],
        help="Leave empty to use the built-in English word list.",
    )

    # 2. Grid sizes
    st.subheader("2. Grid Sizes")
    size_mode = st.radio(
        "Size selection mode",
        ["Preset range", "Custom list"],
        horizontal=True,
    )
    if size_mode == "Preset range":
        size_min, size_max = st.slider(
            "Grid size range (n×n)",
            min_value=5,
            max_value=60,
            value=(10, 30),
            step=5,
        )
        size_step = st.number_input("Step", min_value=1, max_value=20, value=5)
        sizes = list(range(size_min, size_max + 1, size_step))
    else:
        raw = st.text_input(
            "Enter sizes (comma-separated)",
            value="10, 15, 20, 25",
        )
        try:
            sizes = sorted({int(s.strip()) for s in raw.split(",") if s.strip().isdigit()})
        except Exception:
            sizes = DEFAULT_SIZES
            st.warning("Could not parse sizes — using defaults.")

    st.caption(f"Selected sizes: {sizes}")

    puzzles_per_size = st.number_input(
        "Puzzles per size",
        min_value=1,
        max_value=500,
        value=10,
        help="More puzzles → more reliable statistics, but slower.",
    )

    # 3. Word length
    st.subheader("3. Word Length")
    min_word_len = st.slider("Minimum word length", 3, 10, 3)
    max_word_len_mode = st.selectbox(
        "Maximum word length",
        ["Scale with grid (up to size)", "Cap at 10 letters"],
    )

    # 4. Strategies
    st.subheader("4. Strategies")
    selected_strategies = st.multiselect(
        "Select strategies to benchmark",
        options=list(STRATEGY_MAP.keys()),
        default=list(STRATEGY_MAP.keys()),
    )

    # 5. Run button
    st.divider()
    run_button = st.button("Run Experiment", use_container_width=True, type="primary")

# ─── Main area ────────────────────────────────────────────────────────────────

if "results_df" not in st.session_state:
    st.session_state.results_df = None

# Run experiment
if run_button:
    if not selected_strategies:
        st.error("Please select at least one strategy.")
        st.stop()
    if not sizes:
        st.error("Please specify at least one grid size.")
        st.stop()

    # Build generator (with optional uploaded corpus)
    if uploaded_corpus is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="wb") as tmp:
            tmp.write(uploaded_corpus.read())
            tmp_path = tmp.name
        generator = WordsearchGenerator(word_file=tmp_path)
        st.sidebar.success(f"Using uploaded corpus ({uploaded_corpus.name})")
    else:
        generator = WordsearchGenerator()

    progress_bar = st.progress(0.0)
    status_text = st.empty()

    with st.spinner("Running experiment…"):
        df = run_experiment(
            generator=generator,
            sizes=sizes,
            puzzles_per_size=int(puzzles_per_size),
            strategy_names=selected_strategies,
            min_word_len=min_word_len,
            max_word_len_mode=max_word_len_mode,
            progress_bar=progress_bar,
            status_text=status_text,
        )

    progress_bar.empty()
    status_text.empty()
    st.session_state.results_df = df
    st.success(f"Experiment complete — {len(df):,} result rows collected.")

# Results section
df = st.session_state.results_df

if df is not None and not df.empty:

    # ── Data preview & download ────────────────────────────────────────────────
    st.header("Results")

    col_left, col_right = st.columns([3, 1])
    with col_left:
        st.dataframe(df, use_container_width=True, height=260)
    with col_right:
        st.metric("Total rows", f"{len(df):,}")
        st.metric("Strategies", df["strategy"].nunique())
        st.metric("Grid sizes", df["size"].nunique())
        st.metric("Puzzles", df["puzzle_id"].nunique())

        csv_bytes = df.to_csv(index=False).encode()
        st.download_button(
            label="Download CSV",
            data=csv_bytes,
            file_name="wordsearch_results.csv",
            mime="text/csv",
            use_container_width=True,
        )

    # ── Summary statistics ─────────────────────────────────────────────────────
    with st.expander("Summary statistics", expanded=False):
        st.dataframe(
            df.groupby("strategy")
            .agg(
                mean_time=("execution_time", "mean"),
                median_time=("execution_time", "median"),
                mean_cells=("cells_examined", "mean"),
                mean_success_rate=("success_rate", "mean"),
                puzzles_run=("puzzle_id", "count"),
            )
            .round(5)
            .reset_index(),
            use_container_width=True,
        )

    # ── Plots ──────────────────────────────────────────────────────────────────
    st.header("Analysis Plots")

    tab_time, tab_speedup, tab_cells, tab_success, tab_bars, tab_box = st.tabs([
        "Time vs Size",
        "Speedup",
        "Cells Examined",
        "Success Rate",
        "Strategy Summary",
        "Time Distribution",
    ])

    with tab_time:
        fig = plot_time_vs_size(df)
        st.pyplot(fig)
        st.download_button(
            "Save plot",
            data=fig_to_bytes(fig),
            file_name="time_vs_size.png",
            mime="image/png",
        )
        plt.close(fig)

    with tab_speedup:
        fig = plot_speedup(df)
        if fig is None:
            st.info("Include Brute Force to see speedup comparisons.")
        else:
            st.pyplot(fig)
            st.download_button(
                "Save plot",
                data=fig_to_bytes(fig),
                file_name="speedup.png",
                mime="image/png",
            )
            plt.close(fig)

    with tab_cells:
        fig = plot_cells_examined(df)
        st.pyplot(fig)
        st.download_button(
            "Save plot",
            data=fig_to_bytes(fig),
            file_name="cells_examined.png",
            mime="image/png",
        )
        plt.close(fig)

    with tab_success:
        fig = plot_success_rate(df)
        st.pyplot(fig)
        st.download_button(
            "Save plot",
            data=fig_to_bytes(fig),
            file_name="success_rate.png",
            mime="image/png",
        )
        plt.close(fig)

    with tab_bars:
        fig = plot_strategy_summary_bars(df)
        st.pyplot(fig)
        st.download_button(
            "Save plot",
            data=fig_to_bytes(fig),
            file_name="strategy_summary.png",
            mime="image/png",
        )
        plt.close(fig)

    with tab_box:
        fig = plot_box_execution_time(df)
        st.pyplot(fig)
        st.download_button(
            "Save plot",
            data=fig_to_bytes(fig),
            file_name="time_distribution.png",
            mime="image/png",
        )
        plt.close(fig)

else:
    st.info(
        "Configure your experiment in the sidebar and click **Run Experiment** to get started."
    )
