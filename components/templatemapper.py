#!/usr/bin/env python
import yaml
import io
#import itertools
import copy

def map_templates(toolsMapping, toolsArchs, toolsOptions, featuresTargets):
    augmentedOutputYaml = []
    outputs = []
    for tool in toolsMapping:
        #The following is the logic for implementing each tool based on the provided architecture (and their templates). This could mb be replaced by HELM or some other similar tools
        #Toplevel "pod" tag on the template doc determines whether it is a new doc to be added to output (default behaviour), if pod=new, or if it should be included in the user doc specification (i.e., a new container sharing the same pod/deployment), if pod=share
        #featuresTargets is incrementally augmented with management containers as needed, and added to the output before returning it

        with open("templates/" + tool + ".yml") as f:
            docs = yaml.load_all(f, Loader=yaml.FullLoader)
            for doc in docs:
                if (doc is not None):
                    podSharing = doc.pop("pod", "new")
                    podRole = doc.pop("role", "None")

                    if (doc["kind"] == "Service" and "output" in doc["metadata"]):
                        svcOutputs = doc["metadata"].pop("output", "None")
                        for output in svcOutputs:
                            outputs.append(output_from_service(doc, output, toolsOptions[tool]))

                    if toolsArchs[tool] == "agents-collector":
                        if podRole == "collector":
                            print("Collector for " + tool + " unchanged...") #collector won't be changed as is

                        elif podRole == "agent":
                            for featRequester, optionsRequested in zip(toolsMapping[tool],toolsOptions[tool]):
                                for target in featuresTargets:
                                    if target["metadata"]["name"] == featRequester:
                                        if podSharing == "share":
                                            target = add_from_tag("containers", target, copy.deepcopy(doc), optionsRequested)
                                            target = add_from_tag("volumes", target, copy.deepcopy(doc), optionsRequested)

                    #TODO
                    elif toolsArchs[tool] == "client-server":
                        print("#TODO")
                    #TODO
                    elif toolsArchs[tool] == "standalone":
                        print("#TODO")

                    else:
                        print(toolsArchs[tool])
                        print("Error mapping " + tool + "'s architecture!")

                    if podSharing == "new":
                        augmentedOutputYaml.append(doc)

    for target in featuresTargets:
        augmentedOutputYaml.append(target)
    return augmentedOutputYaml, outputs

def output_from_service(svcdoc, output, toolOptions):
    result = {}
    result["svcName"] = svcdoc["metadata"]["name"]
    result["outputKind"] = output["kind"]
    result["metric"] = output["metric"] #default from template
    for option in toolOptions:
        if "metric" in option:
            result["metric"] = option["metric"]
    result["path"] = output["path"].replace("$metric", result["metric"])
    return result

def add_from_tag(tag, original, increment, options):
    if tag not in original["spec"]["template"]["spec"]:
        original["spec"]["template"]["spec"][tag] = []
    if tag == "containers":
        for key in options:
            exists = False
            for origkey in increment["spec"]["template"]["spec"][tag][0]["env"]:
                if origkey["name"] == key:
                    origkey["value"] = options[key]
                    exists = True
            if not exists:
                increment["spec"]["template"]["spec"][tag][0]["env"].extend([{"name": key, "value": options[key]}])

    original["spec"]["template"]["spec"][tag].extend(increment["spec"]["template"]["spec"][tag])
    return original

# TODO recursive function to augment the original doc with the template/tool specification
def augment_doc(original, increment, options):
    for tag, value in increment.items():
        if tag not in original:
            original[tag] = increment[tag]
      
        if isinstance(increment[tag], dict):
            augment_doc(original[tag], increment[tag], options)

        elif isinstance(increment[tag], list):
            print("is a list")
            if tag not in original:
                print("a new one")
 #               original[tag] = increment[tag]
            else:
                print("not a new one")
                original[tag].extend(increment[tag])

        else:       
            print("Error augmenting...")
