cwlVersion: v1.1
class: CommandLineTool
requirements:
  - class: DockerRequirement
    dockerPull: "python:3.7-slim"
  - class: ShellCommandRequirement

inputs:
  input_file:
    type: File

arguments:
  - cat
  - $(inputs.input_file)
  - {shellQuote: false, valueFrom: "|"}
  - wc 
  - "-l"

outputs:
  line_count:
    type: string 
    outputBinding:
      glob: stdout.txt
      loadContents: true
      outputEval: $(self[0].contents)

stdout: stdout.txt
