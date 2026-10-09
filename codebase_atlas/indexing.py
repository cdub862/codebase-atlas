from dataclasses import dataclass
from pathlib import Path
import ast

@dataclass(frozen=True)
class FunctionEntry:
    file: str
    symbol: str
    start_line: int
    end_line: int
    source: str


def index_python_functions(repo_path: Path) -> list[FunctionEntry]:
    output = []

    for file in sorted(repo_path.rglob("*.py")):
        source = file.read_text(encoding="utf-8")
        tree = ast.parse(source)
        for smt in tree.body:
            if isinstance(smt, (ast.FunctionDef, ast.AsyncFunctionDef)):
                output.append(FunctionEntry(
                    file=file.relative_to(repo_path).as_posix(),
                    symbol=smt.name,
                    start_line=smt.lineno,
                    end_line=smt.end_lineno,
                    source=ast.get_source_segment(source, smt) or ""
                ))
    return output