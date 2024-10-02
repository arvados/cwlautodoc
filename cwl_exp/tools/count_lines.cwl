cwlVersion: v1.1
class: CommandLineTool
baseCommand: wc
requirements:
  - class: DockerRequirement
    dockerPull: "python:3.7-slim"
inputs:
  input_file:
    type: File
    inputBinding:
      position: 1
outputs:
  line_count:
    type: File
    outputBinding:
      glob: output.txt

