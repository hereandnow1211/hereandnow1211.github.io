import os
import json
from PyPDF2 import PdfReader
from pathlib import Path

def get_pdf_info(pdf_path, base_dir):
    """Get information about a PDF file."""
    try:
        with open(pdf_path, 'rb') as file:
            pdf = PdfReader(file)
            # Get relative path from base directory
            rel_path = pdf_path.relative_to(base_dir)
            return {
                'name': pdf_path.name,
                'type': 'file',
                'size': f"{pdf_path.stat().st_size / (1024*1024):.1f} MB",
                'pages': len(pdf.pages),
                'path': str(rel_path.parent) if str(rel_path.parent) != '.' else '',
                'url': str(rel_path)  # Use relative path for URL
            }
    except Exception as e:
        print(f"Error reading {pdf_path}: {str(e)}")
        return None

def get_directory_info(dir_path, base_dir):
    """Get information about a directory."""
    rel_path = dir_path.relative_to(base_dir)
    return {
        'name': dir_path.name,
        'type': 'directory',
        'path': str(rel_path) if str(rel_path) != '.' else ''
    }

def scan_directory(directory):
    """Scan directory recursively for PDFs and subdirectories."""
    base_dir = Path(directory)
    contents = []
    
    # First add directories
    for item in sorted(base_dir.iterdir()):
        if item.is_dir():
            contents.append(get_directory_info(item, base_dir))
    
    # Then add PDF files
    for item in sorted(base_dir.iterdir()):
        if item.is_file() and item.suffix.lower() == '.pdf':
            info = get_pdf_info(item, base_dir)
            if info:
                contents.append(info)
    
    return contents

def main():
    # Get all PDF files from the pdfs directory
    pdf_dir = Path('pdfs')
    if not pdf_dir.exists():
        print("Creating pdfs directory...")
        pdf_dir.mkdir()
    
    # Scan the directory recursively
    contents = scan_directory(pdf_dir)
    
    # Write metadata to JSON file
    with open('pdfs.json', 'w') as f:
        json.dump(contents, f, indent=2)
    
    print(f"Processed {len(contents)} items (files and directories)")

if __name__ == '__main__':
    main() 