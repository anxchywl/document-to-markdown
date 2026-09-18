# document-to-markdown

A small local converter for PDFs, Word, Excel, and PowerPoint files.

It uses Microsoft's [MarkItDown](https://github.com/microsoft/markitdown) for Office files, `pdftotext -layout` for readable PDFs, and local macOS Vision OCR when a PDF has broken font encoding. Files stay on the computer.

## setup and use

```bash
cd /Users/anx/document-to-markdown
./setup.sh
./convert.py
```

Place files in `sources/`. Markdown output goes to `markdown/`.

OCR recovers text but not the original visual layout. Keep the source files for visual review.
