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
            # Ensure URL uses forward slashes and is relative to pdfs directory
            url_path = str(rel_path).replace('\\', '/')
            return {
                'name': pdf_path.name,
                'type': 'file',
                'size': f"{pdf_path.stat().st_size / (1024*1024):.1f} MB",
                'pages': len(pdf.pages),
                'path': str(rel_path.parent).replace('\\', '/') if str(rel_path.parent) != '.' else '',
                'url': url_path  # URL will be relative to pdfs directory
            }
    except Exception as e:
        print(f"Error reading {pdf_path}: {str(e)}")
        return None

def get_directory_info(dir_path, base_dir):
    """Get information about a directory."""
    rel_path = dir_path.relative_to(base_dir)
    # Ensure path uses forward slashes
    path_str = str(rel_path).replace('\\', '/')
    return {
        'name': dir_path.name,
        'type': 'directory',
        'path': path_str if path_str != '.' else ''
    }

def scan_directory(directory, base_dir=None):
    """Scan directory recursively for PDFs and subdirectories."""
    if base_dir is None:
        base_dir = Path(directory)
    base_dir = Path(base_dir)
    current_dir = Path(directory)
    contents = []
    
    # First add directories
    for item in sorted(current_dir.iterdir()):
        if item.is_dir():
            contents.append(get_directory_info(item, base_dir))
            # Recursively scan subdirectories, always passing the original base_dir
            subdir_contents = scan_directory(item, base_dir)
            contents.extend(subdir_contents)
    
    # Then add PDF files in current directory
    for item in sorted(current_dir.iterdir()):
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
    contents = scan_directory(pdf_dir, pdf_dir)
    
    # Write metadata to JSON file
    with open('pdfs.json', 'w') as f:
        json.dump(contents, f, indent=2)
    
    print(f"Processed {len(contents)} items (files and directories)")

if __name__ == '__main__':
    main() 