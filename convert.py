#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import tempfile
from pathlib import Path


SUPPORTED = {".pdf", ".docx", ".pptx", ".xlsx", ".xls"}


def parse_args() -> argparse.Namespace:
    root = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="Convert documents to Markdown.")
    parser.add_argument("--source-dir", type=Path, default=root / "sources")
    parser.add_argument("--output-dir", type=Path, default=root / "markdown")
    return parser.parse_args()


def markitdown_path() -> Path:
    root = Path(__file__).resolve().parent
    path = root / ".venv" / "bin" / "markitdown"
    if not path.exists():
        raise SystemExit(f"MarkItDown is not installed; run {root / 'setup.sh'} first")
    return path


def looks_broken(text: str) -> bool:
    if not text.strip():
        return True
    cid_count = len(re.findall(r"\(cid:\d+\)", text))
    replacement_count = text.count("�")
    control_count = sum(
        1 for character in text
        if ord(character) < 32 and character not in "\n\r\t\f"
    )
    return cid_count >= 5 or replacement_count >= 5 or control_count >= 50


def convert_with_markitdown(converter: Path, source: Path) -> str:
    result = subprocess.run(
        [str(converter), str(source)],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def convert_pdf_with_layout(source: Path) -> str:
    result = subprocess.run(
        ["pdftotext", "-layout", str(source), "-"],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    pages = [page.strip() for page in text.split("\f")]
    if len(pages) == 1:
        return pages[0].strip() + "\n"
    return "\n\n".join(
        f"<!-- page {number} -->\n\n{page}"
        for number, page in enumerate(pages, start=1)
        if page
    ) + "\n"


def convert_pdf_with_ocr(source: Path, ocr_binary: Path) -> str:
    if shutil.which("pdftoppm") is None:
        raise SystemExit("pdftoppm is required for OCR fallback but was not found")

    with tempfile.TemporaryDirectory(prefix="document-to-markdown-") as temporary:
        render_dir = Path(temporary) / "pages"
        render_dir.mkdir()
        subprocess.run(
            ["pdftoppm", "-png", "-r", "200", str(source), str(render_dir / "page")],
            check=True,
            stdout=subprocess.DEVNULL,
        )
        pages = sorted(render_dir.glob("page-*.png"))
        if not pages:
            raise RuntimeError(f"no rendered pages produced for {source.name}")

        parts = [
            f"# {source.stem}\n",
            "_extracted with local macOS Vision OCR because normal PDF text extraction was unreliable._\n",
        ]
        for page_number, page in enumerate(pages, start=1):
            result = subprocess.run(
                [str(ocr_binary), str(page)],
                check=True,
                capture_output=True,
                text=True,
            )
            parts.append(f"\n<!-- page {page_number} -->\n\n{result.stdout.strip()}\n")
        return "".join(parts)


def main() -> None:
    args = parse_args()
    converter = markitdown_path()
    ocr_binary = Path(__file__).resolve().parent / "bin" / "ocr-page"
    args.output_dir.mkdir(parents=True, exist_ok=True)
    sources = sorted(
        path for path in args.source_dir.iterdir()
        if path.is_file() and not path.name.startswith(".") and path.suffix.lower() in SUPPORTED
    )
    if not sources:
        raise SystemExit(f"No supported files found in {args.source_dir}")

    for source in sources:
        output = args.output_dir / f"{source.stem}.md"
        try:
            if source.suffix.lower() == ".pdf":
                try:
                    text = convert_pdf_with_layout(source)
                    method = "pdf-layout"
                except (FileNotFoundError, subprocess.CalledProcessError):
                    text = convert_with_markitdown(converter, source)
                    method = "markitdown"
            else:
                text = convert_with_markitdown(converter, source)
                method = "markitdown"

            if source.suffix.lower() == ".pdf" and looks_broken(text):
                if not ocr_binary.exists():
                    raise SystemExit(f"OCR fallback required for {source.name}. Run: {Path(__file__).resolve().parent / 'scripts' / 'build_ocr.sh'}")
                text = convert_pdf_with_ocr(source, ocr_binary)
                method = "vision-ocr"
            output.write_text(normalize_text(text), encoding="utf-8")
            print(f"{method:10} {source.name} -> {output.name}")
        except subprocess.CalledProcessError as error:
            print(f"failed      {source.name}: {error}")


if __name__ == "__main__":
    main()
