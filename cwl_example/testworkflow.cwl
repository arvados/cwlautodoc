cwlVersion: v1.1
class: Workflow
id: testworkflow
label: Example Workflow
doc: A simple example workflow to demonstrate autodocumentation.

s:author:
  - class: s:Person
    s:name: "John Doe"
    s:email: "john.doe@example.com"

s:citation: https://dx.doi.org/
s:dateCreated: "2023-10-02"
s:license: https://spdx.org/licenses/Apache-2.0

inputs:
  input_file:
    type: File
    format: edam:format_1964
    label: "An input file to process."

outputs:
  outputwc:
    type: string
    outputSource: step1/line_count
    label: "String containing line count of input file" 

  outputcap:
    type: File
    format: edam:format_1964
    outputSource: step2/output_file
    label: "Output file with all capital letters"
   
steps:
  step1:
    run: tools/count_lines.cwl
    in:
      input_file: input_file
    out: [line_count]

  step2:
    run: tools/uppercase.cwl
    in:
      input_file: input_file 
    out: [output_file]

$namespaces:
  s: https://schema.org/
  edam: http://edamontology.org/

$schemas:
  - https://schema.org/version/latest/schemaorg-current-https.rdf
  - http://edamontology.org/EDAM_1.18.owl
