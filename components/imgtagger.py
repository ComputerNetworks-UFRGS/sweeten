#!/usr/bin/env python

# Optional (and alpha!) module to add tags to deployments based on information extracted from a container image description
# Requires docker package for container image processing
# Requires nltk for text processing and tag generation (TODO)

import docker
import requests
import bs4

def enrichedDescriptionFromGoogle(imageName):
        queryText = imageName
        url = "https://google.com/search?q=define+" + queryText
        requestResult = requests.get(url)
        enrichedDescription = bs4.BeautifulSoup(requestResult.text,"html.parser").find("div", class_='BNeawe').text
        return enrichedDescription

def pullInfoFromDocker(imageName):
        client = docker.from_env()
        client.images.pull(imageName)
        dockerImage = client.images.get(imageName)
        imageTagsReadDict = dockerImage.tags
        try:
                imageDescription = dockerImage.labels["description"]
                #print("Image default description: " + imageDescription)
        except:
                imageDescription = ""
                #print("No default image description available")
        return dockerImage, imageTagsReadDict, imageDescription

def addTagsToContainerImage(imageName):
        dockerImage, imageDefaultTags, imageDefaultDescription = pullInfoFromDocker(imageName)
        enrichedDescription = enrichedDescriptionFromGoogle(imageName)

        print("Docker image name: " + imageName)
        print("Image original tags: ", end="")
        for tag in imageDefaultTags:
                print(tag)
        print("Image original description: " + imageDefaultDescription)
        print("Enriched description: " + enrichedDescription)


# imageName = "eclipse-mosquitto"
# addTagsToContainerImage(imageName)