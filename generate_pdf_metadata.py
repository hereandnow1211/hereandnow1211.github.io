import os
import json
from PyPDF2 import PdfReader
from pathlib import Path

def get_pdf_info(pdf_path):
    """Get information about a PDF file."""
    try:
        with open(pdf_path, 'rb') as file:
            pdf = PdfReader(file)
            return {
                'name': pdf_path.name,
                'type': 'file',
                'size': f"{pdf_path.stat().st_size / (1024*1024):.1f} MB",
                'pages': len(pdf.pages),
                'url': f"pdfs/{pdf_path.name}"  # Use relative path for GitHub Pages
            }
    except Exception as e:
        print(f"Error reading {pdf_path}: {str(e)}")
        return None

def main():
    # Get all PDF files from the pdfs directory
    pdf_dir = Path('pdfs')
    if not pdf_dir.exists():
        print("Creating pdfs directory...")
        pdf_dir.mkdir()
    
    pdf_files = [f for f in os.listdir(pdf_dir) if f.lower().endswith('.pdf')]
    
    # Generate metadata for each PDF
    pdf_info = []
    for pdf_file in pdf_files:
        info = get_pdf_info(pdf_dir / pdf_file)
        if info:
            pdf_info.append(info)
    
    # Write metadata to JSON file
    with open('pdfs.json', 'w') as f:
        json.dump(pdf_info, f, indent=2)
    
    print(f"Processed {len(pdf_info)} PDF files")

if __name__ == '__main__':
    main() 