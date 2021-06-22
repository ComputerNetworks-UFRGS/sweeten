#!/usr/bin/env python

import yaml
import io
import subprocess
import shutil

#Container catalogue is abstracted since default dockerhub repository is used for all (user's and management's) images

def deploy(partialOutputYaml, augmentedOutputYaml, outputs):
    # Write YAML file for unchanged input docs
    with open("solution/partialOutput.yaml", "w") as stream:
        yaml.dump_all(partialOutputYaml, stream, default_flow_style=False)

    # Write YAML file for augmented docs
    with open("solution/augmentedOutput.yaml", "w") as stream:
        yaml.dump_all(augmentedOutputYaml, stream, default_flow_style=False)

    # Copy YAML kustomization file to trigger the deployment from both YAML files
    shutil.copy2('templates/kustomization.yaml', 'solution/')

    return 0
    #Launch kubectl to deploy solution
    bashCommand = "kubectl apply -k solution/"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE, cwd='./')
    output, error = process.communicate()

    #mb optional? wait for deployment to be available
    bashCommand = "kubectl wait deployment --all --for condition=available --timeout=400s"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE, cwd='./')
    output, error = process.communicate()

    #(for minikube and sflow example!) Get dashboard url
    #print "URL for dashboard:"
    #bashCommand = "minikube service sflow-rt-rest --url"
    #process = subprocess.Popen(bashCommand.split(), cwd='./')
    #output, error = process.communicate()
    print("Output:")
    for svcOutput in outputs:
        bashCommand = "minikube service $svc --url".replace("$svc", svcOutput["svcName"])
        bashOutput = subprocess.check_output(bashCommand, shell=True)
        
        print(svcOutput["outputKind"] + " for " + svcOutput["metric"] + ": " + bashOutput.rstrip() + svcOutput["path"])
