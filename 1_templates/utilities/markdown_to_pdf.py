import os
import argparse
import markdown
from weasyprint import HTML

def convert_markdown_to_pdf(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith('.md'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, os.path.splitext(filename)[0] + '.pdf')
            
            try:
                with open(input_path, 'r', encoding='utf-8') as f:
                    markdown_content = f.read()
                html_content = markdown.markdown(markdown_content)
                HTML(string=html_content).write_pdf(output_path)
                print(f"Converted {filename} to PDF")
            except Exception as e:
                print(f"Error converting {filename}: {e}")