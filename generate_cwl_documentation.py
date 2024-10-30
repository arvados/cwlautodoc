import argparse
import os
from cwl_utils.parser.cwl_v1_2 import load_document, CommandLineTool, Workflow
import json


def serialize_cwl_object(obj):
    if isinstance(obj, dict):
        return {k: serialize_cwl_object(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [serialize_cwl_object(i) for i in obj]
    elif hasattr(obj, "__dict__"):
        return {k: str(v) for k, v in obj.__dict__.items() if not k.startswith("_")}
    else:
        return str(obj)


def extract_cwl_type(cwl_input):
    if hasattr(cwl_input, "type"):
        cwl_type = cwl_input.type
        if isinstance(cwl_type, str):
            return cwl_type
        elif isinstance(cwl_type, dict):
            return cwl_type.get("type", "N/A")
        elif isinstance(cwl_type, list):
            return ", ".join([extract_cwl_type(t) for t in cwl_type])
    return "N/A"

def get_all_attributes(obj):
    # Use vars() if obj has a __dict__ attribute
    if hasattr(obj, '__dict__'):
        attributes = vars(obj)
    else:
        # Otherwise, use dir() and get the attribute values using getattr()
        attributes = {attr: getattr(obj, attr) for attr in dir(obj) if not attr.startswith('__')}
    
    return attributes

# Function to clean up the main keys and interior field keys
def clean_schema_dict(data):
    cleaned_data = {}
    
    for key, value in data.items():
        # Rename the main key using the last part of the URL
        new_key = key.rsplit('/', 1)[-1]
        
        # Process nested dictionary or list values to remove "schema" prefixes in field names
        if isinstance(value, list):
            cleaned_value = [
                {sub_key.split(':', 1)[-1]: sub_value for sub_key, sub_value in item.items()}
                if isinstance(item, dict) else item
                for item in value
            ]
        elif isinstance(value, dict):
            cleaned_value = {sub_key.split(':', 1)[-1]: sub_value for sub_key, sub_value in value.items()}
        else:
            cleaned_value = value

        # Assign the cleaned key and value to the new dictionary
        cleaned_data[new_key] = cleaned_value

    return cleaned_data


# Generate document structure from CWL file
def generate_document_structure(cwl_doc):

    extension_fields = (clean_schema_dict(cwl_doc.extension_fields))

    if isinstance(cwl_doc, Workflow):
        doc_structure = {
            "id": cwl_doc.id,
            "label": getattr(cwl_doc, "label", None),
            "doc": getattr(cwl_doc, "doc", None),
            "cwlversion": getattr(cwl_doc, "cwlVersion", None),
            "authors": (
                [author["s:name"] for author in cwl_doc["s:author"]]
                if hasattr(cwl_doc, "s:author")
                else []
            ),
            "formats": ["s:format"] if hasattr(cwl_doc, "s:format") else [],
            "base_command": (
                cwl_doc.baseCommand
                if isinstance(cwl_doc, CommandLineTool)
                and hasattr(cwl_doc, "baseCommand")
                else None
            ),
            "inputs": [
                {
                    "id": input.id,
                    "type": getattr(input, "type_"),
                    "description": getattr(input, "doc", "No description provided."),
                }
                for input in cwl_doc.inputs or []
            ],
            "outputs": [
                {
                    "id": output.id,
                    "type": getattr(output, "type_"),
                    "description": getattr(output, "doc", "No description provided."),
                }
                for output in cwl_doc.outputs or []
            ],
            "steps": (
                [step for step in cwl_doc.steps or []]
                if isinstance(cwl_doc, Workflow)
                else []
            ),
            "requirements": [dir(req) for req in cwl_doc.requirements or []],
            "hints": [serialize_cwl_object(hint) for hint in cwl_doc.hints or []],
        }

    return doc_structure


# Convert document structure to Markdown
def convert_to_markdown(doc_structure: dict) -> str:
    doc_str = f"# Documentation for {doc_structure['id']}\n\n"
    if doc_structure["label"]:
        doc_str += f"**Label**: {doc_structure['label']}\n\n"
    doc_str += f"## Description\n{doc_structure['doc']}\n\n"

    if doc_structure["authors"]:
        doc_str += f"## Authors\n**Authors**: {', '.join(doc_structure['authors'])}\n\n"

    if doc_structure["formats"]:
        doc_str += f"**Formats**: {', '.join(doc_structure['formats'])}\n\n"

    if doc_structure["base_command"]:
        doc_str += f"## Base Command\n`{doc_structure['base_command']}`\n\n"

    doc_str += "## Inputs\n"
    for input in doc_structure["inputs"]:
        doc_str += f"- **{input['id']}** (`{input['type']}`): {input['description']}\n"
    doc_str += "\n"

    doc_str += "## Outputs\n"
    for output in doc_structure["outputs"]:
        doc_str += (
            f"- **{output['id']}** (`{output['type']}`): {output['description']}\n"
        )
    doc_str += "\n"

    if doc_structure["steps"]:
        doc_str += "## Workflow Steps\n"
        for step in doc_structure["steps"]:
            doc_str += f"- **{step['id']}**: Runs `{step['run']}` with inputs {step['inputs']}\n"
            doc_str += f"  Outputs: {step['outputs']}\n"
        doc_str += "\n"

    if doc_structure["requirements"]:
        doc_str += "## Requirements\n"
        for req in doc_structure["requirements"]:
            doc_str += f"- **{req['class']}**: {json.dumps(req, indent=2)}\n"
        doc_str += "\n"

    if doc_structure["hints"]:
        doc_str += "## Hints\n"
        for hint in doc_structure["hints"]:
            doc_str += f"- **{hint['class']}**: {json.dumps(hint, indent=2)}\n"
        doc_str += "\n"

    return doc_str


# Main function for command-line interaction
def main():
    parser = argparse.ArgumentParser(
        description="Generate CWL documentation in Markdown or HTML format."
    )
    parser.add_argument("cwl_file", type=str, help="Path to the CWL file.")
    parser.add_argument(
        "--format",
        type=str,
        choices=["markdown", "html"],
        default="markdown",
        help="Output format (markdown or html).",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="docs",
        help="Directory to save the generated documentation.",
    )

    args = parser.parse_args()

    # Create the output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Generate the documentation structure
    cwl_obj = load_document(args.cwl_file)
    doc_structure = generate_document_structure(cwl_obj)


    print(doc_structure)

# Convert to the requested format
# if args.format == "markdown":
#    output_content = convert_to_markdown(doc_structure)
#    output_file = os.path.join(args.output_dir, "cwl-documentation.md")
# else:
#    output_content = convert_to_html(doc_structure)
#    output_file = os.path.join(args.output_dir, "cwl-documentation.html")

# Write the content to the file
# with open(output_file, "w") as f:
#    f.write(output_content)

# print(f"Documentation generated and saved to {output_file}")

if __name__ == "__main__":
    main()
