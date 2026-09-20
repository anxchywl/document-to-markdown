# document-to-markdown

Local converter for PDFs, Word, Excel, and PowerPoint files.

It uses Microsoft's [MarkItDown](https://github.com/microsoft/markitdown) for Office files, `pdftotext -layout` for readable PDFs, and local macOS Vision OCR when a PDF has broken font encoding. Files stay on the computer.

## why it exists

Markdown is easier to search, edit, compare, and reuse than office files. It also works well with scripts and language models, which can reduce the amount of data and cost needed for AI processing. This project keeps conversion local and uses OCR when normal PDF extraction fails.

## setup and use

1. Open Terminal.

2. Download the project:

```bash
git clone https://github.com/anxchywl/document-to-markdown.git
```

3. Enter the project folder:

```bash
cd document-to-markdown
```

4. Install the required dependencies:

```bash
./setup.sh
```

5. Put the files you want to convert into the `sources/` folder.

6. Start the converter:

```bash
./convert.py
```

The converted Markdown files will appear in the `markdown/` folder.

OCR recovers text but not the original visual layout. Keep the source files for visual review.
