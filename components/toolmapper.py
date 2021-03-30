#!/usr/bin/env python

import yaml
# import itertools

def map_tools(featuresMapping, featuresOptions, featuresTags):
    toolsMapping = {}
    toolsArchs = {}
    toolsOptions = {} #for now, options from features are simply copied as options for the tools themselves
    toolsCatalogue = load_tools_catalogue()
    for discipline in featuresMapping:
        for feature in featuresMapping[discipline]:
            ftOpts = featuresOptions[discipline][feature]
            ftTags = featuresTags[discipline][feature]
            tool = feature_to_tool(discipline, feature, ftOpts, ftTags, toolsCatalogue)
            if tool["tool"] not in toolsMapping:
                toolsMapping[tool["tool"]] = []
                toolsOptions[tool["tool"]] = []
                toolsArchs[tool["tool"]] = tool["architecture"]
            for target, options in zip(featuresMapping[discipline][feature], featuresOptions[discipline][feature]):
                toolsMapping[tool["tool"]].append(target)
                toolsOptions[tool["tool"]].append(options)
    return toolsMapping, toolsArchs, toolsOptions


#For now, this simply returns the first tool corresponding to the feature requested. Should consider other parameters (user options, other deployment specs maybe) to produce a more fit tool
def feature_to_tool(discipline, feature, featureOptions, featureTags, toolsCatalogue):
    for tag in featureTags[0:5]:
        for tool in toolsCatalogue[discipline][feature]:
            if tool[1] in tag:
                return tool[0]

def load_tools_catalogue():
    with open("tools_catalogue.yaml", 'r') as stream:
        try:
            toolsCatalogue = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print("Error loading the Tools Catalogue")
            print(exc)
        return toolsCatalogue
