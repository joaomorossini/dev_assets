#!/usr/bin/env python3
"""
Script to convert markdown files to HTML memos and PDFs using the AfricaCare memo template.
"""

import os
import re
import sys
import base64
import markdown
import datetime
from pathlib import Path
import subprocess
import argparse

# Define base directory and template paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEMO_TEMPLATE_PATH = os.path.join(BASE_DIR, "memo_template.html")
LOGO_PATH = os.path.join(BASE_DIR, "..", "logo.png")
OUTPUT_DIR = os.path.join(BASE_DIR, "memos")

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_metadata(markdown_content):
    """Extract title and other metadata from markdown content"""
    metadata = {
        "title": "Memorando",
        "date": datetime.datetime.now().strftime("%d/%m/%Y"),
        "from": "África Care",
        "to": "Grupo Castel Angola",
        "subject": "Informação Interna"
    }
    
    # Extract title from the first heading
    title_match = re.search(r'^#\s+(.+)$', markdown_content, re.MULTILINE)
    if title_match:
        metadata["title"] = title_match.group(1).strip()
        metadata["subject"] = metadata["title"]
    
    # Look for metadata in the format <!-- key: value --> or [//]: # (key: value)
    meta_patterns = [
        r'<!--\s*(\w+)\s*:\s*(.+?)\s*-->',
        r'\[//\]:\s*#\s*\((\w+)\s*:\s*(.+?)\s*\)'
    ]
    
    for pattern in meta_patterns:
        for match in re.finditer(pattern, markdown_content, re.MULTILINE):
            key, value = match.groups()
            key = key.lower()
            if key in ["title", "date", "from", "to", "subject"]:
                metadata[key] = value.strip()
    
    return metadata

def convert_markdown_to_html(markdown_content):
    """Convert markdown content to HTML"""
    # Configure the markdown extensions
    extensions = [
        'markdown.extensions.tables',
        'markdown.extensions.fenced_code',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
        'markdown.extensions.nl2br'  # Convert newlines to <br>
    ]
    
    # Convert markdown to HTML
    html_content = markdown.markdown(markdown_content, extensions=extensions)
    return html_content

def create_memo(markdown_path, output_html_path=None, output_pdf_path=None):
    """Create memo HTML and PDF from markdown file"""
    with open(markdown_path, 'r', encoding='utf-8') as file:
        markdown_content = file.read()
    
    # Extract metadata from markdown
    metadata = extract_metadata(markdown_content)
    
    # Convert markdown to HTML
    html_content = convert_markdown_to_html(markdown_content)
    
    # Read template
    with open(MEMO_TEMPLATE_PATH, 'r', encoding='utf-8') as file:
        template = file.read()
    
    # Create a data URI for the logo to avoid path issues
    logo_data_uri = ""
    try:
        if os.path.isfile(LOGO_PATH):
            with open(LOGO_PATH, 'rb') as logo_file:
                logo_bytes = logo_file.read()
                logo_base64 = base64.b64encode(logo_bytes).decode('utf-8')
                logo_data_uri = f"data:image/png;base64,{logo_base64}"
        else:
            print(f"Logo file not found at {LOGO_PATH}")
            # Create a simple placeholder logo (orange rectangle)
            logo_data_uri = "data:image/png;base64,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"
    except Exception as e:
        print(f"Error creating data URI for logo: {e}")
        # Create a simple placeholder logo (orange rectangle)
        logo_data_uri = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAMgAAADICAYAAACtWK6eAAAAAXNSR0IArs4c6QAABClJREFUeF7t1DEBAAAIwzDAv+chx7YXWD8zZ4AACQQBD0gSRoDAOwQEYg0CtQICqcEIEBCIDUCgFhBIDUaAgEBsAAK1gEBqMAIEBGIDEKgFBFKDESAgEBuAQC0gkBqMAAGB2AAEagGB1GAECAjEBiBQCwikBiNAQCA2AIFaQCA1GAECArEBCNQCAqnBCBAQiA1AoBYQSA1GgIBAbAACCOyAQHbcBTwQEIgNQKAWEEgNRoCAQGwAArWAQGowAgQEYgMQqAUEUoMRICAQG4BALSCQGowAAYHYAARqAYHUYAQICMQGIFALCKQGI0BAIDYAgVpAIDUYAQICsQEI1AICqcEIEBCIDUCgFhBIDUaAgEBsAAK1gEBqMAIEBGIDEKgFBFKDESAgEBuAQC0gkBqMAAGB2AAEagGB1GAECAjEBiBQCwikBiNAQCA2AIFaQCA1GAECArEBCNQCAqnBCBAQiA1AoBYQSA1GgIBAbAACCOyAQHbcBTwQEIgNQKAWEEgNRoCAQGwAArWAQGowAgQEYgMQqAUEUoMRICAQG4BALSCQGowAAYHYAARqAYHUYAQICMQGIFALCKQGI0BAIDYAgVpAIDUYAQICsQEI1AICqcEIEBCIDUCgFhBIDUaAgEBsAAK1gEBqMAIEBGIDEKgFBFKDESAgEBuAQC0gkBqMAAGB2AAEagGB1GAECAjEBiBQCwikBiNAQCA2AIFaQCA1GAECArEBCNQCAqnBCBAQiA1AoBYQSA1GgIBAbAACCOyAQHbcBTwQEIgNQKAWEEgNRoCAQGwAArWAQGowAgQEYgMQqAUEUoMRICAQG4BALSCQGowAAYHYAARqAYHUYAQICMQGIFALCKQGI0BAIDYAgVpAIDUYAQICsQEI1AICqcEIEBCIDUCgFhBIDUaAgEBsAAK1gEBqMAIEBGIDEKgFBFKDESAgEBuAQC0gkBqMAAGB2AAEagGB1GAECAjEBiBQCwikBiNAQCA2AIFaQCA1GAECArEBCNQCAqnBCBAQiA1AoBYQSA1GgIBAbAACCOyAQHbcBTwQEIgNQKAWEEgNRoCAQGwAArWAQGowAgQEYgMQqAUEUoMRICAQG4BALSCQGowAAYHYAARqAYHUYAQICMQGIFALCKQGI0BAIDYAgVpAIDUYAQICsQEI1AICqcEIEBCIDUCgFhBIDUaAgEBsAAK1gEBqMAIEBGIDEKgFBFKDESAgEBuAQC0gkBqMAAGB2AAEagGB1GAECAjEBiBQCwikBiNAQCA2AIFaQCA1GAECArEBCNQCAqnBCBAQiA1AoBYQSA1GgIBAbAACCOyAQHbcBTwQEIgNQKAWEEgNRoCAQGwAArWAQGowAgQEYgMQqAUEUoMRICAQG4BALSCQGowAAYHYAARqAYHUYAQICMQGIFALCKQGI0BAIDYAgVpAIDUYAQICsQEI1AICqcEIEBCIDUCgFhBIDUaAgEBsAAK1gEBqMAIEBGIDEKgFBFKDESAgEBuAQC0gkBqMAAGB2AAEagGB1GAECAjEBiBQCwikBiNAQCA2AIFaQCA1GAECArEBCNQCAqnBCBAQiA1AAIEFOhCTRs3vUigAAAAASUVORK5CYII="
    
    # Replace placeholders in template
    memo_html = template
    memo_html = memo_html.replace("[LOGO_URL]", logo_data_uri)
    memo_html = memo_html.replace("[TITULO_MEMO]", metadata["title"])
    memo_html = memo_html.replace("[DATA_MEMO]", metadata["date"])
    memo_html = memo_html.replace("[DE_MEMO]", metadata["from"])
    memo_html = memo_html.replace("[PARA_MEMO]", metadata["to"])
    memo_html = memo_html.replace("[ASSUNTO_MEMO]", metadata["subject"])
    
    # Replace content placeholder with HTML content
    memo_html = memo_html.replace("[CONTEUDO_MEMO]", html_content)
    
    # Define output paths if not provided
    if output_html_path is None:
        filename = os.path.splitext(os.path.basename(markdown_path))[0]
        output_html_path = os.path.join(OUTPUT_DIR, f"memo_{filename}.html")
    
    if output_pdf_path is None:
        filename = os.path.splitext(os.path.basename(markdown_path))[0]
        output_pdf_path = os.path.join(OUTPUT_DIR, f"memo_{filename}.pdf")
    
    # Write HTML to file
    with open(output_html_path, 'w', encoding='utf-8') as file:
        file.write(memo_html)
    
    print(f"Memo HTML created: {output_html_path}")
    
    # Convert HTML to PDF using wkhtmltopdf
    try:
        print(f"Converting {output_html_path} to PDF...")
        cmd = ['wkhtmltopdf', '--enable-local-file-access', output_html_path, output_pdf_path]
        subprocess.run(cmd, check=True)
        print(f"PDF created: {output_pdf_path}")
        return output_html_path, output_pdf_path
    except subprocess.CalledProcessError as e:
        print(f"Error converting to PDF: {e}")
        return output_html_path, None
    except Exception as e:
        print(f"Unexpected error in PDF conversion: {e}")
        return output_html_path, None

def main():
    parser = argparse.ArgumentParser(description='Convert markdown files to AfricaCare memos in HTML and PDF format.')
    parser.add_argument('markdown_file', help='Path to the markdown file to convert')
    parser.add_argument('--date', help='Date for the memo (default: today)')
    parser.add_argument('--from', dest='from_field', help='From field (default: África Care)')
    parser.add_argument('--to', help='To field (default: Grupo Castel Angola)')
    parser.add_argument('--subject', help='Subject field (default: extracted from title)')
    
    args = parser.parse_args()
    
    if not os.path.isfile(args.markdown_file):
        print(f"Error: File {args.markdown_file} not found")
        sys.exit(1)
    
    # Create memo from markdown file
    try:
        html_path, pdf_path = create_memo(args.markdown_file)
        if pdf_path:
            print("Memo generation completed successfully!")
        else:
            print("Memo HTML generated, but PDF conversion failed.")
    except Exception as e:
        print(f"Error generating memo: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
