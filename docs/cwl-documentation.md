# Documentation for file:///home/swz/autodoc/cwlautodoc/cwl_example/testworkflow.cwl#testworkflow

**Label**: Example Workflow

## Description
A simple example workflow to demonstrate autodocumentation.

## Inputs
- **file:///home/swz/autodoc/cwlautodoc/cwl_example/testworkflow.cwl#testworkflow/input_file** (`File`): None

## Outputs
- **file:///home/swz/autodoc/cwlautodoc/cwl_example/testworkflow.cwl#testworkflow/outputcap** (`File`): None
- **file:///home/swz/autodoc/cwlautodoc/cwl_example/testworkflow.cwl#testworkflow/outputwc** (`string`): None

## Workflow Steps
- **file:///home/swz/autodoc/cwlautodoc/cwl_example/testworkflow.cwl#testworkflow/step1**: Runs `file:///home/swz/autodoc/cwlautodoc/cwl_example/tools/count_lines.cwl` with inputs ['file:///home/swz/autodoc/cwlautodoc/cwl_example/testworkflow.cwl#testworkflow/step1/input_file']
  Outputs: ['file:///home/swz/autodoc/cwlautodoc/cwl_example/testworkflow.cwl#testworkflow/step1/line_count']
- **file:///home/swz/autodoc/cwlautodoc/cwl_example/testworkflow.cwl#testworkflow/step2**: Runs `file:///home/swz/autodoc/cwlautodoc/cwl_example/tools/uppercase.cwl` with inputs ['file:///home/swz/autodoc/cwlautodoc/cwl_example/testworkflow.cwl#testworkflow/step2/input_file']
  Outputs: ['file:///home/swz/autodoc/cwlautodoc/cwl_example/testworkflow.cwl#testworkflow/step2/output_file']

