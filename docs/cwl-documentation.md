# Documentation for file:///home/swz/autodoc/cwlautodoc/cwl_exp/testworkflow.cwl#testworkflow

**Label**: Example Workflow

## Description
A simple example workflow to demonstrate multi-step processes.

## Inputs
- **file:///home/swz/autodoc/cwlautodoc/cwl_exp/testworkflow.cwl#testworkflow/input_file** (`File`): An input file to process.

## Outputs
- **file:///home/swz/autodoc/cwlautodoc/cwl_exp/testworkflow.cwl#testworkflow/final_output** (`File`): None

## Workflow Steps
- **file:///home/swz/autodoc/cwlautodoc/cwl_exp/testworkflow.cwl#testworkflow/step1**: Runs `file:///home/swz/autodoc/cwlautodoc/cwl_exp/tools/count_lines.cwl` with inputs ['file:///home/swz/autodoc/cwlautodoc/cwl_exp/testworkflow.cwl#testworkflow/step1/input_file']
  Outputs: ['file:///home/swz/autodoc/cwlautodoc/cwl_exp/testworkflow.cwl#testworkflow/step1/line_count']
- **file:///home/swz/autodoc/cwlautodoc/cwl_exp/testworkflow.cwl#testworkflow/step2**: Runs `file:///home/swz/autodoc/cwlautodoc/cwl_exp/tools/uppercase.cwl` with inputs ['file:///home/swz/autodoc/cwlautodoc/cwl_exp/testworkflow.cwl#testworkflow/step2/input_file']
  Outputs: ['file:///home/swz/autodoc/cwlautodoc/cwl_exp/testworkflow.cwl#testworkflow/step2/output_file']

