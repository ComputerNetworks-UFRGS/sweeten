#!/usr/bin/env python

# Optional (and alpha!) module to add tags to deployments based on information extracted from a container image description
# Requires docker package for container image processing
# Requires nltk for text processing and tag generation (TODO)

import docker

#imageName = "sflow/prometheus"
#imageName = "alpine"
imageName = "eclipse-mosquitto"

client = docker.from_env()

dockerImage = client.images.get(imageName)

imageTagsReadDict = dockerImage.tags

print(dockerImage)
print(imageTagsReadDict)
try:
        imageDescription = dockerImage.labels["description"]
        print(imageDescription)
except:
        imageDescription = ""
        print("No description available")
