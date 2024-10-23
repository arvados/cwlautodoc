cwlVersion: v1.1
class: CommandLineTool

arguments:
  - cat
  - $(inputs.input_file)
  - {shellQuote: false, valueFrom: "|"}
  - tr
  - 'a-z'
  - 'A-Z'

requirements:
  - class: DockerRequirement
    dockerPull: "python:3.7-slim"
  - class: ShellCommandRequirement

inputs:
  input_file:
    type: File

outputs:
  output_file:
    type: File
    outputBinding:
      glob: output.txt

stdout: output.txt
