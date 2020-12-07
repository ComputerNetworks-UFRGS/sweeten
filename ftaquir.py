#!/usr/bin/env python

import yaml

#Start by parsing the compose file with user's deployments/services/etc, and aquire desired management features annotations

def aquire_features(inputYaml):
    featuresMapping = {} # maps what features are required, and by what deployments/docs (by name)
    featuresOptions = {} # maps options requested by each service, for each feature (this all could use a dif data structure, mb a tree)
    featuresTargets = [] # targets/docs that have features required (mgmt tags already removed)
    partialOutputYaml = [] # input that does not require management features (copied to output, thus)

    with open(inputYaml) as f:    
        docs = yaml.load_all(f, Loader=yaml.FullLoader)
        for doc in docs:
            if (doc is not None):
                if ("management" in doc["metadata"]):
#                    print "THIS IS A DOC THAT REQUESTS MANAGEMENT FEATURE(S):"
                    for featureRequest in doc["metadata"]["management"]:
                        for discipline in ["administration", "monitoring", "security"]:
                            if discipline in featureRequest:
                                if discipline not in featuresMapping:
                                    featuresMapping[discipline] = {}
                                    featuresOptions[discipline] = {}
                                if featureRequest[discipline] not in featuresMapping[discipline]:
                                    featuresMapping[discipline][featureRequest[discipline]] = []
                                    featuresOptions[discipline][featureRequest[discipline]] = []
                                featuresMapping[discipline][featureRequest[discipline]].append(doc["metadata"]["name"])

                                temp = featureRequest[discipline]
                                del featureRequest[discipline]
                                featuresOptions[discipline][temp].append(featureRequest)

                    #create target list for the docs minus the management annotations
                    del doc["metadata"]["management"]
                    featuresTargets.append(doc)
                else:
#                    print "THIS IS A DOC THAT DOES NOT(!) REQUEST ANY MANAGEMENT FEATURE (i.e., is copied directly to output yaml):"
                    partialOutputYaml.append(doc)
#                print doc
#                print "!+_+!#_+!_#+!_#+!_#+!_#+!_#+!_"

    return featuresMapping, featuresOptions, featuresTargets, partialOutputYaml
