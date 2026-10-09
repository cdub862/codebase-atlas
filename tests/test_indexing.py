from pathlib import Path

from codebase_atlas.indexing import FunctionEntry, index_python_functions

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "sample_repo"


def get_expected_source(entry: FunctionEntry):
    file_path = FIXTURE_PATH / entry.file
    lines = file_path.read_text(encoding="utf-8").splitlines()
    return "\n".join(lines[entry.start_line - 1 : entry.end_line]).strip()


def test_index_python_functions():
    entries = index_python_functions(FIXTURE_PATH)

    functions: dict[str, FunctionEntry] = {}

    for entry in entries:
        functions[entry.symbol] = entry

        assert 1 <= entry.start_line <= entry.end_line
        assert entry.source.lstrip().startswith(
            (f"def {entry.symbol}(", f"async def {entry.symbol}(")
        )

    assert len(entries) == 3
    # api / get_profile
    assert "get_profile" in functions
    assert functions["get_profile"].file == "api.py"
    assert functions["get_profile"].source.strip() == get_expected_source(
        functions["get_profile"]
    )

    # auth / validate_token
    assert "validate_token" in functions
    assert functions["validate_token"].file == "auth.py"
    assert functions["validate_token"].source.strip() == get_expected_source(
        functions["validate_token"]
    )

    # database / find_user
    assert "find_user" in functions
    assert functions["find_user"].file == "database.py"
    assert functions["find_user"].source.strip() == get_expected_source(
        functions["find_user"]
    )
