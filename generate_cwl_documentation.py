import argparse
import os
from cwl_utils.parser.cwl_v1_2 import load_document, CommandLineTool, Workflow
import json

def serialize_cwl_object(obj):
    if isinstance(obj, dict):
        return {k: serialize_cwl_object(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [serialize_cwl_object(i) for i in obj]
    elif hasattr(obj, '__dict__'):
        return {k: str(v) for k, v in obj.__dict__.items() if not k.startswith('_')}
    else:
        return str(obj)

def extract_cwl_type(cwl_input):
    if hasattr(cwl_input, 'type'):
        cwl_type = cwl_input.type
        if isinstance(cwl_type, str):
            return cwl_type
        elif isinstance(cwl_type, dict):
            return cwl_type.get('type', 'N/A')
        elif isinstance(cwl_type, list):
            return ', '.join([extract_cwl_type(t) for t in cwl_type])
    return 'N/A'

# Generate document structure from CWL file
def generate_document_structure(cwl_file_path: str) -> dict:
    cwl_doc = load_document(cwl_file_path)

    doc_structure = {
        "id": cwl_doc.id,
        "label": getattr(cwl_doc, 'label', None),
        "description": getattr(cwl_doc, 'doc', "No description provided."),
        "authors": [author['s:name'] for author in cwl_doc['s:author']] if hasattr(cwl_doc, 's:author') else [],
        "formats": cwl_doc['s:format'] if hasattr(cwl_doc, 's:format') else [],
        "base_command": cwl_doc.baseCommand if isinstance(cwl_doc, CommandLineTool) and hasattr(cwl_doc, 'baseCommand') else None,
        "inputs": [{"id": input.id, "type": extract_cwl_type(input), "description": getattr(input, 'doc', 'No description provided.')} for input in cwl_doc.inputs or []],
        "outputs": [{"id": output.id, "type": extract_cwl_type(output), "description": getattr(output, 'doc', 'No description provided.')} for output in cwl_doc.outputs or []],
        "steps": [{"id": step.id, "run": step.run, "inputs": [input.id for input in step.in_], "outputs": step.out} for step in cwl_doc.steps or []] if isinstance(cwl_doc, Workflow) else [],
        "requirements": [serialize_cwl_object(req) for req in cwl_doc.requirements or []],
        "hints": [serialize_cwl_object(hint) for hint in cwl_doc.hints or []]
    }

    return doc_structure

# Convert document structure to Markdown
def convert_to_markdown(doc_structure: dict) -> str:
    doc_str = f"# Documentation for {doc_structure['id']}\n\n"
    if doc_structure['label']:
        doc_str += f"**Label**: {doc_structure['label']}\n\n"
    doc_str += f"## Description\n{doc_structure['description']}\n\n"

    if doc_structure['authors']:
        doc_str += f"## Authors\n**Authors**: {', '.join(doc_structure['authors'])}\n\n"

    if doc_structure['formats']:
        doc_str += f"**Formats**: {', '.join(doc_structure['formats'])}\n\n"

    if doc_structure['base_command']:
        doc_str += f"## Base Command\n`{doc_structure['base_command']}`\n\n"

    doc_str += "## Inputs\n"
    for input in doc_structure['inputs']:
        doc_str += f"- **{input['id']}** (`{input['type']}`): {input['description']}\n"
    doc_str += "\n"

    doc_str += "## Outputs\n"
    for output in doc_structure['outputs']:
        doc_str += f"- **{output['id']}** (`{output['type']}`): {output['description']}\n"
    doc_str += "\n"

    if doc_structure['steps']:
        doc_str += "## Workflow Steps\n"
        for step in doc_structure['steps']:
            doc_str += f"- **{step['id']}**: Runs `{step['run']}` with inputs {step['inputs']}\n"
            doc_str += f"  Outputs: {step['outputs']}\n"
        doc_str += "\n"

    if doc_structure['requirements']:
        doc_str += "## Requirements\n"
        for req in doc_structure['requirements']:
            doc_str += f"- **{req['class']}**: {json.dumps(req, indent=2)}\n"
        doc_str += "\n"

    if doc_structure['hints']:
        doc_str += "## Hints\n"
        for hint in doc_structure['hints']:
            doc_str += f"- **{hint['class']}**: {json.dumps(hint, indent=2)}\n"
        doc_str += "\n"

    return doc_str

# Convert document structure to HTML
def convert_to_html(doc_structure: dict) -> str:
    doc_str = f"<h1>Documentation for {doc_structure['id']}</h1>\n\n"
    if doc_structure['label']:
        doc_str += f"<strong>Label</strong>: {doc_structure['label']}<br>\n\n"
    doc_str += f"<h2>Description</h2>\n<p>{doc_structure['description']}</p>\n\n"

    if doc_structure['authors']:
        doc_str += f"<h2>Authors</h2>\n<strong>Authors</strong>: {', '.join(doc_structure['authors'])}<br>\n\n"

    if doc_structure['formats']:
        doc_str += f"<strong>Formats</strong>: {', '.join(doc_structure['formats'])}<br>\n\n"

    if doc_structure['base_command']:
        doc_str += f"<h2>Base Command</h2>\n<code>{doc_structure['base_command']}</code>\n\n"

    doc_str += "<h2>Inputs</h2>\n"
    for input in doc_structure['inputs']:
        doc_str += f"<strong>{input['id']}</strong> (`{input['type']}`): {input['description']}<br>\n"
    doc_str += "\n"

    doc_str += "<h2>Outputs</h2>\n"
    for output in doc_structure['outputs']:
        doc_str += f"<strong>{output['id']}</strong> (`{output['type']}`): {output['description']}<br>\n"
    doc_str += "\n"

    if doc_structure['steps']:
        doc_str += "<h2>Workflow Steps</h2>\n"
        for step in doc_structure['steps']:
            doc_str += f"<strong>{step['id']}</strong>: Runs `{step['run']}` with inputs {step['inputs']}<br>\n"
            doc_str += f"  Outputs: {step['outputs']}<br>\n"
        doc_str += "\n"

    if doc_structure['requirements']:
        doc_str += "<h2>Requirements</h2>\n"
        for req in doc_structure['requirements']:
            doc_str += f"<strong>{req['class']}</strong>: <pre>{json.dumps(req, indent=2)}</pre>\n"
        doc_str += "\n"

    if doc_structure['hints']:
        doc_str += "<h2>Hints</h2>\n"
        for hint in doc_structure['hints']:
            doc_str += f"<strong>{hint['class']}</strong>: <pre>{json.dumps(hint, indent=2)}</pre>\n"
        doc_str += "\n"

    return doc_str

# Main function for command-line interaction
def main():
    parser = argparse.ArgumentParser(description="Generate CWL documentation in Markdown or HTML format.")
    parser.add_argument("cwl_file", type=str, help="Path to the CWL file.")
    parser.add_argument("--format", type=str, choices=["markdown", "html"], default="markdown", help="Output format (markdown or html).")
    parser.add_argument("--output_dir", type=str, default="docs", help="Directory to save the generated documentation.")
    
    args = parser.parse_args()

    # Create the output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Generate the documentation structure
    doc_structure = generate_document_structure(args.cwl_file)

    # Convert to the requested format
    if args.format == "markdown":
        output_content = convert_to_markdown(doc_structure)
        output_file = os.path.join(args.output_dir, "cwl-documentation.md")
    else:
        output_content = convert_to_html(doc_structure)
        output_file = os.path.join(args.output_dir, "cwl-documentation.html")

    # Write the content to the file
    with open(output_file, "w") as f:
        f.write(output_content)

    print(f"Documentation generated and saved to {output_file}")

if __name__ == "__main__":
    main()

