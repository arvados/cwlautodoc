cwlVersion: v1.2
class: CommandLineTool
baseCommand: ["bash", "-c"]
arguments: ["cat ${inputs.input_file} | tr a-z A-Z > output.txt"]
requirements:
  - class: DockerRequirement
    dockerPull: "python:3.7-slim"
inputs:
  input_file:
    type: File
    inputBinding:
      position: 1
outputs:
  output_file:
    type: File
    outputBinding:
      glob: output.txt

