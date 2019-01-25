cwlVersion: v1.0
class: Workflow
label: Calculates an md5sum
doc: Longer label to describe how what this workflow does

inputs:
  input_file: File

outputs:
  output_file:
    type: File
    outputSource: md5sum/output_file

steps:
  md5sum:
    label: Main workhorse to calculate the md5sum
    doc:  Longer doc statement on what the step does
    run: /home/sarah/cwldoc/cwl-utils/testdata/dockstore-tool-md5sum.cwl
    in:
      input_file: input_file
    out: [output_file]

