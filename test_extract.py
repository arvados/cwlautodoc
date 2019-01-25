#!/usr/bin/env python3
import sys
import cwl_utils.parser_v1_0 as cwl
import inspect
import os

def main():
    top = cwl.load_document(sys.argv[1])
    traverse(top)

def extract_software_packages(process: cwl.Process):
    for req in extract_software_reqs(process):
        print(process.id)
        process_software_requirement(req)

def extract_labels(process: cwl.Process):
    if process.label:
       print('#### '+ process.label+ '\n')
    if process.doc:
       print('#### ' + process.doc + '\n')

def extract_software_reqs(process: cwl.Process):
    if process.requirements:
        for req in process.requirements:
            if isinstance(req, cwl.SoftwareRequirement):
                yield req
    if process.hints:
        for req in process.hints:
            if req['class'] == "SoftwareRequirement":
                yield cwl.load_field(req, cwl.SoftwareRequirementLoader,
                                     process.id, process.loadingOptions)


def process_software_requirement(req: cwl.SoftwareRequirement):
    for package in req.packages:
        print("Package: {}, version: {}, specs: {}".format(
            package.package, package.version, package.specs))


def traverse(process: cwl.Process):
    extract_software_packages(process)
    if isinstance(process, cwl.Workflow):
        traverse_workflow(process)


def get_process_from_step(step: cwl.WorkflowStep):
    if isinstance(step.run, str):
        return cwl.load_document(step.run)
    return step.run


def traverse_workflow(workflow: cwl.Workflow):
#    print('Workflow: \n')
    workflowname = os.path.basename(workflow.id)
    print('# Workflow: ' + workflowname + '\n')
#    print(vars(workflow))
    extract_labels(workflow)
    print('## Steps: \n')
    for step in workflow.steps:
#         print(vars(step))
         stepname = step.id.split('#')[-1]
         print('### Step: ' + stepname + '\n')
         extract_labels(step)
#        extract_software_packages(step)
#        traverse(get_process_from_step(step))


if __name__ == "__main__":
    sys.exit(main())
