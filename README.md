Here is a `README.md` file that explains how to use the function and how to test it with the provided CWL file.

```markdown
# CWL Documentation Generator

This Python script generates documentation for CWL workflows or command-line tools in either Markdown or HTML format. It extracts metadata such as inputs, outputs, authors, and more from the CWL file and produces structured documentation.

## Requirements

1. Python 3.x
2. `cwl-utils` package for parsing CWL files.

Install the required Python package:

```bash
pip install cwl-utils

## How to run:

python3 generate_cwl_documentation.py path_to_cwl_file.cwl --format markdown

python3 generate_cwl_documentation.py path_to_cwl_file.cwl --format html --output_dir output/

