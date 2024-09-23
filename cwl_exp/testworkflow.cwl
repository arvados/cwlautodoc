cwlVersion: v1.2
class: Workflow
id: testworkflow
label: Example Workflow
doc: A simple example workflow to demonstrate multi-step processes.

s:author:
  - s:name: "John Doe"
    s:email: "john.doe@example.com"

inputs:
  input_file:
    type: File
    doc: "An input file to process."

outputs:
  final_output:
    type: File
    outputSource: step2/output_file

steps:
  step1:
    run: tools/count_lines.cwl
    in:
      input_file: input_file
    out: [line_count]

  step2:
    run: tools/uppercase.cwl
    in:
      input_file: step1/line_count
    out: [output_file]

$namespaces:
  s: https://schema.org/
  edam: http://edamontology.org/
