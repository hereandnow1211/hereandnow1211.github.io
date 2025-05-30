# PDF Library

A simple PDF library hosted on GitHub Pages that allows users to browse and read PDF files.

## How to Use

1. Visit [https://hereandnow1211.github.io](https://hereandnow1211.github.io) to view the PDF library
2. Click on any PDF to read it
3. Use the refresh button to update the library contents

## Adding New PDFs

To add new PDFs to the library:

1. Add your PDF files to the `pdfs` directory
2. Run the metadata generator:
   ```bash
   pip install PyPDF2
   python generate_pdf_metadata.py
   ```
3. Commit and push the changes:
   ```bash
   git add .
   git commit -m "Add new PDFs"
   git push origin main
   ```

The library will automatically update with the new PDFs.

## Structure

- `index.html` - The main webpage
- `generate_pdf_metadata.py` - Script to generate PDF metadata
- `pdfs.json` - Generated metadata file (do not edit manually)
- `pdfs/` - Directory containing all PDF files 