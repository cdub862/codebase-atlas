import json
from pathlib import Path

from codebase_atlas.indexing import index_python_functions
from codebase_atlas.retrieval import search_functions


def main():
    root = Path(__file__).resolve().parent.parent

    fixture = root / "tests" / "fixtures" / "sample_repo"
    dataset = root / "tests" / "evaluation" / "navigation_cases.json"

    entries = index_python_functions(fixture)
    cases = json.loads(dataset.read_text(encoding="utf-8"))

    correct_count = 0

    for case in cases:
        results = search_functions(case["query"], entries, limit=1)
        predicted = results[0].entry if results else None

        correct = (
            predicted is not None
            and predicted.file == case["expected_file"]
            and predicted.symbol == case["expected_symbol"]
        )

        correct_count += int(correct)

        print(
            f"{case['id']}: "
            f"predicted={predicted.symbol if predicted else 'None'} "
            f"expected={case['expected_symbol']} "
            f"correct={correct}"
        )

    accuracy = correct_count / len(cases) if cases else 0
    print(f"\nTop-1 accuracy: {accuracy:.1%} ({correct_count}/{len(cases)})")


if __name__ == "__main__":
    main()
