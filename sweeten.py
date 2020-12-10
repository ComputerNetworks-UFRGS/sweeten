#!/usr/bin/env python

import logging, sys
from components.ftaquir import aquire_features
from components.toolmapper import map_tools
from components.templatemapper import map_templates
from components.deployer import deploy

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

#SWEETEN main
#1. Take user input
inputYaml = sys.argv[1]

#2. Acquire features requested from input
featuresMapping, featuresOptions, featuresTargets, partialOutputYaml = aquire_features(inputYaml)
logging.info("Management features required:")
logging.info(featuresMapping)
logging.info("Management options required for each feature/service:")
logging.info(featuresOptions)
logging.info("Docs targeted for the features:")
logging.info(featuresTargets)
logging.info("Partial output:")
logging.info(partialOutputYaml)

#3. Map features into tools (and options, possibly), and get tools architectures (used for templates later)
toolsMapping, toolsArchs, toolsOptions = map_tools(featuresMapping, featuresOptions)
logging.info("Tools mapping:")
logging.info(toolsMapping)
logging.info("Tools architectures:")
logging.info(toolsArchs)
logging.info("Tools options:")
logging.info(toolsOptions)

#4. Map tools using templates to generate a deployable specification for all the mgmt tools (and managed user services)
augmentedOutputYaml, outputs = map_templates(toolsMapping, toolsArchs, toolsOptions, featuresTargets)
logging.info("Augmented output (managed services and mgmt tools):")
logging.info(augmentedOutputYaml)
logging.info("API/Dashboard outputs:")
logging.info(outputs)

#5. Deploy the complete solution (user app + net management)
deploy(partialOutputYaml, augmentedOutputYaml, outputs)
