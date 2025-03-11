#!/usr/bin/env python3
"""
Script to generate both newsletters and memos from markdown files
using the AfricaCare templates.
"""

import os
import sys
import argparse
import subprocess

# Define base directory and make it the current directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

def generate_newsletter(markdown_file, output_name=None):
    """
    Generate a newsletter from a markdown file using the generate_newsletters.py script.
    """
    try:
        cmd = ['python', 'generate_newsletters.py', markdown_file]
        if output_name:
            cmd.extend(['--output', output_name])
        
        print(f"Generating newsletter from {markdown_file}...")
        subprocess.run(cmd, check=True)
        print("Newsletter generation completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error generating newsletter: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error in newsletter generation: {e}")
        return False

def generate_memo(markdown_file, date=None, from_field=None, to_field=None, subject=None):
    """
    Generate a memo from a markdown file using the generate_memos.py script.
    """
    try:
        cmd = ['python', 'generate_memos.py', markdown_file]
        if date:
            cmd.extend(['--date', date])
        if from_field:
            cmd.extend(['--from', from_field])
        if to_field:
            cmd.extend(['--to', to_field])
        if subject:
            cmd.extend(['--subject', subject])
        
        print(f"Generating memo from {markdown_file}...")
        subprocess.run(cmd, check=True)
        print("Memo generation completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error generating memo: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error in memo generation: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Generate AfricaCare documents (newsletters or memos) from markdown files.')
    parser.add_argument('markdown_file', help='Path to the markdown file to convert')
    parser.add_argument('--type', choices=['newsletter', 'memo'], default='memo', 
                      help='Type of document to generate (default: memo)')
    parser.add_argument('--output', help='Output name for the newsletter (without extension)')
    parser.add_argument('--date', help='Date for the memo (default: today)')
    parser.add_argument('--from', dest='from_field', help='From field for the memo (default: África Care)')
    parser.add_argument('--to', help='To field for the memo (default: Grupo Castel Angola)')
    parser.add_argument('--subject', help='Subject field for the memo (default: extracted from title)')
    
    args = parser.parse_args()
    
    if not os.path.isfile(args.markdown_file):
        print(f"Error: File {args.markdown_file} not found")
        sys.exit(1)
    
    if args.type == 'newsletter':
        success = generate_newsletter(args.markdown_file, args.output)
    else:  # memo
        success = generate_memo(args.markdown_file, args.date, args.from_field, args.to, args.subject)
    
    if success:
        print(f"{args.type.capitalize()} generated successfully!")
    else:
        print(f"Failed to generate {args.type}.")
        sys.exit(1)

if __name__ == "__main__":
    main() 
