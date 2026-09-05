# app/benchmark/humaneval.py
import json


def load_problems(path: str = "data/humaneval_10.json") -> list:
    """Load benchmark problems from JSON file."""
    with open(path, "r") as f:
        return json.load(f)