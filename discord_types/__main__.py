import argparse
import itertools
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from . import md


@dataclass(frozen=True)
class Endpoint:
    name: str
    method: str
    route: str
    parameters: Dict[str, Optional[str]]


def discover_files(docs: Path) -> List[Path]:
    if not docs.exists():
        raise RuntimeError(
            f"discord-api-docs repository not found, path does not exist: {docs.absolute()!s}"
        )
    return list(
        itertools.chain.from_iterable(
            (docs / dir).rglob("*.md") for dir in ("interactions", "resources", "topics")
        )
    )


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "output_path",
        help="output directory for json files",
        nargs="?",
        default="./output",
    )
    parser.add_argument(
        "repo_path",
        help="path to cloned discord-api-docs repository",
        nargs="?",
        default="./discord-api-docs",
    )
    args = parser.parse_args()

    repo = Path(args.repo_path) / "docs"
    files = discover_files(repo)

    output = Path(args.output_path)
    for file in files:
        ast = md.parser.ast(file.read_text(encoding="utf-8"))
        print(f"Parsed {len(ast)} elements from {file!s}")
        result = md.processor.read_ast(ast)

        if result:
            out_path = output / file.relative_to(repo)
            out_path = out_path.with_suffix(".json")
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(result.json(indent=4), encoding="utf-8")
            print(f"Wrote data to {out_path!s}")


if __name__ == "__main__":
    main()
