#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


SUPPORTED = {".pdf", ".docx", ".pptx", ".xlsx", ".xls"}


def parse_args() -> argparse.Namespace:
    root = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="Convert documents to Markdown.")
    parser.add_argument("--source-dir", type=Path, default=root / "sources")
    parser.add_argument("--output-dir", type=Path, default=root / "markdown")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    converter = Path(__file__).resolve().parent / ".venv" / "bin" / "markitdown"
    if not converter.exists():
        raise SystemExit("MarkItDown is not installed; run ./setup.sh first")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    sources = sorted(
        path for path in args.source_dir.iterdir()
        if path.is_file() and not path.name.startswith(".") and path.suffix.lower() in SUPPORTED
    )
    if not sources:
        raise SystemExit(f"No supported files found in {args.source_dir}")

    for source in sources:
        output = args.output_dir / f"{source.stem}.md"
        result = subprocess.run(
            [str(converter), str(source)],
            check=True,
            capture_output=True,
            text=True,
        )
        output.write_text(result.stdout, encoding="utf-8")
        print(f"{source.name} -> {output.name}")


if __name__ == "__main__":
    main()
