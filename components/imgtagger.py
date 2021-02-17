#!/usr/bin/env python
import docker
import requests
import bs4
from operator import itemgetter

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


with open('../input/descriptions.txt') as f:
        docs = f.readlines()

for i, doc in enumerate(docs[:-1]):
        docs[i] = doc[:-1]

imageName = "eclipse-mosquitto"
doc_a = enrichedDescriptionFromGoogle(imageName)
docs.append(doc_a)

from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
import re

tokenizer = RegexpTokenizer(r'\w+')

# create English stop words list
en_stop = get_stop_words('en')

# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()

# create sample documents
# doc_b = "Constrained Application Protocol (CoAP) is a specialized Internet Application Protocol for constrained devices, as defined in RFC 7252. It enables those constrained devices called 'nodes' to communicate with the wider Internet using similar protocols. CoAP is designed for use between devices on the same constrained network (e.g., low-power, lossy networks), between devices and general nodes on the Internet, and between devices on different constrained networks both joined by an internet. CoAP is also being used via other mechanisms, such as SMS on mobile communication networks. CoAP is a service layer protocol that is intended for use in resource-constrained internet devices, such as wireless sensor network nodes. CoAP is designed to easily translate to HTTP for simplified integration with the web, while also meeting specialized requirements such as multicast support, very low overhead, and simplicity.[1][2] Multicast, low overhead, and simplicity are extremely important for Internet of Things (IoT) and Machine-to-Machine (M2M) devices, which tend to be deeply embedded and have much less memory and power supply than traditional internet devices have. Therefore, efficiency is very important. CoAP can run on most devices that support UDP or a UDP analogue. The Internet Engineering Task Force (IETF) Constrained RESTful Environments Working Group (CoRE) has done the major standardization work for this protocol. In order to make the protocol suitable to IoT and M2M applications, various new functions have been added. The core of the protocol is specified in RFC 7252; important extensions are in various stages of the standardization process."
# doc_c = "Small. Simple. Secure. Alpine Linux is a security-oriented, lightweight Linux distribution based on musl libc and busybox. Alpine Linux is a Linux distribution based on musl and BusyBox, designed for security, simplicity, and resource efficiency. It uses OpenRC for its init system and compiles all user-space binaries as position-independent executables with stack-smashing protection.It allows very small Linux containers, around 8 MB in size, while a minimal installation to disk might be around 130 MB. "
# doc_d = "Elasticsearch is a search engine based on the Lucene library. It provides a distributed, multitenant-capable full-text search engine with an HTTP web interface and schema-free JSON documents. Elasticsearch is developed in Java. Parts of the software were licensed under various open-source licenses (mostly the Apache License), with future development dual-licensed under the source-available Server Side Public License and the Elastic license starting in 2021,[2] while other parts[3] fall under the proprietary (source-available) Elastic License. Official clients are available in Java, .NET (C#), PHP, Python, Apache Groovy, Ruby and many other languages.[4] According to the DB-Engines ranking, Elasticsearch is the most popular enterprise search engine followed by Apache Solr, also based on Lucene. Elasticsearch is a distributed, free and open search and analytics engine for all types of data, including textual, numerical, geospatial, structured, and unstructured. Elasticsearch is built on Apache Lucene and was first released in 2010 by Elasticsearch N.V. (now known as Elastic). Known for its simple REST APIs, distributed nature, speed, and scalability, Elasticsearch is the central component of the Elastic Stack, a set of free and open tools for data ingestion, enrichment, storage, analysis, and visualization. Commonly referred to as the ELK Stack (after Elasticsearch, Logstash, and Kibana), the Elastic Stack now includes a rich collection of lightweight shipping agents known as Beats for sending data to Elasticsearch."
# doc_e = "Kubernetes is a portable, extensible, open-source platform for managing containerized workloads and services, that facilitates both declarative configuration and automation. It has a large, rapidly growing ecosystem. Kubernetes services, support, and tools are widely available. The name Kubernetes originates from Greek, meaning helmsman or pilot. Google open-sourced the Kubernetes project in 2014. Kubernetes combines over 15 years of Google's experience running production workloads at scale with best-of-breed ideas and practices from the community. It aims to provide a platform for automating deployment, scaling, and operations of application containers across clusters of hosts. It works with a range of container tools and runs containers in a cluster, often with images built using Docker. Kubernetes originally interfaced with the Docker runtime through a Dockershim; however, the shim has since been deprecated in favor of directly interfacing with containerd or another CRI-compliant runtime. Many cloud services offer a Kubernetes-based platform or infrastructure as a service (PaaS or IaaS) on which Kubernetes can be deployed as a platform-providing service. Many vendors also provide their own branded Kubernetes distributions."
# doc_f = 'The Internet of things (IoT) describes the network of physical objects—“things”—that are embedded with sensors, software, and other technologies for the purpose of connecting and exchanging data with other devices and systems over the Internet. Things have evolved due to the convergence of multiple technologies, real-time analytics, machine learning, commodity sensors, and embedded systems.[1] Traditional fields of embedded systems, wireless sensor networks, control systems, automation (including home and building automation), and others all contribute to enabling the Internet of things. In the consumer market, IoT technology is most synonymous with products pertaining to the concept of the "smart home", including devices and appliances (such as lighting fixtures, thermostats, home security systems and cameras, and other home appliances) that support one or more common ecosystems, and can be controlled via devices associated with that ecosystem, such as smartphones and smart speakers. IoT can also be used in healthcare systems. There are a number of serious concerns about dangers in the growth of IoT, especially in the areas of privacy and security, and consequently industry and governmental moves to address these concerns have begun including the development of international standards.'
# doc_g = "Enhanced mobile broadband (eMBB) is, in simple terms, an extension of services first enabled by 4G LTE networks that allows for a high data rate across a wide coverage area. eMBB will provide the greater capacity necessary to support peak data rates both for large crowds and for end users who are on the move. For data-hungry consumers and enterprises, this is the key to a faster, more reliably connected experience across many applications. Depending on the use case, eMBB will need to adapt to difference scenarios. Where there are many users who are not moving quickly, like fans at a sporting event, the network will need a high traffic capacity but a lower mobility requirement. However, for passengers on a commuter train, for example, there will be a greater demand for mobility but at a lower capacity. Either way, seamless coverage is the ultimate goal: users can get connected and stay connected as they move anywhere within the eMBB service range."
# doc_h = "In computing, lightweight software also called lightweight program and lightweight application, is a computer program that is designed to have a small memory footprint (RAM usage) and low CPU usage, overall a low usage of system resources. To achieve this, the software should avoid software bloat and code bloat and try to find the best algorithm efficiency. "
doc_b = "Constrained Application Protocol (CoAP) is a specialized Internet Application Protocol for constrained devices, as defined in RFC 7252. It enables those constrained devices called 'nodes' to communicate with the wider Internet using similar protocols. CoAP is designed for use between devices on the same constrained network (e.g., low-power, lossy networks), between devices and general nodes on the Internet, and between devices on different constrained networks both joined by an internet. CoAP is also being used via other mechanisms, such as SMS on mobile communication networks. CoAP is a service layer protocol that is intended for use in resource-constrained internet devices, such as wireless sensor network nodes. CoAP is designed to easily translate to HTTP for simplified integration with the web, while also meeting specialized requirements such as multicast support, very low overhead, and simplicity.[1][2] Multicast, low overhead, and simplicity are extremely important for Internet of Things (IoT) and Machine-to-Machine (M2M) devices, which tend to be deeply embedded and have much less memory and power supply than traditional internet devices have. Therefore, efficiency is very important. CoAP can run on most devices that support UDP or a UDP analogue. The Internet Engineering Task Force (IETF) Constrained RESTful Environments Working Group (CoRE) has done the major standardization work for this protocol. In order to make the protocol suitable to IoT and M2M applications, various new functions have been added. The core of the protocol is specified in RFC 7252; important extensions are in various stages of the standardization process."
doc_c = "Small. Simple. Secure. Alpine Linux is a security-oriented, lightweight Linux distribution based on musl libc and busybox. Alpine Linux is a Linux distribution based on musl and BusyBox, designed for security, simplicity, and resource efficiency. It uses OpenRC for its init system and compiles all user-space binaries as position-independent executables with stack-smashing protection.It allows very small Linux containers, around 8 MB in size, while a minimal installation to disk might be around 130 MB. "
#doc_d = "Elasticsearch is a search engine based on the Lucene library. It provides a distributed, multitenant-capable full-text search engine with an HTTP web interface and schema-free JSON documents. Elasticsearch is developed in Java. Parts of the software were licensed under various open-source licenses (mostly the Apache License), with future development dual-licensed under the source-available Server Side Public License and the Elastic license starting in 2021,[2] while other parts[3] fall under the proprietary (source-available) Elastic License. Official clients are available in Java, .NET (C#), PHP, Python, Apache Groovy, Ruby and many other languages.[4] According to the DB-Engines ranking, Elasticsearch is the most popular enterprise search engine followed by Apache Solr, also based on Lucene. Elasticsearch is a distributed, free and open search and analytics engine for all types of data, including textual, numerical, geospatial, structured, and unstructured. Elasticsearch is built on Apache Lucene and was first released in 2010 by Elasticsearch N.V. (now known as Elastic). Known for its simple REST APIs, distributed nature, speed, and scalability, Elasticsearch is the central component of the Elastic Stack, a set of free and open tools for data ingestion, enrichment, storage, analysis, and visualization. Commonly referred to as the ELK Stack (after Elasticsearch, Logstash, and Kibana), the Elastic Stack now includes a rich collection of lightweight shipping agents known as Beats for sending data to Elasticsearch."
doc_e = "Kubernetes is a portable, extensible, open-source platform for managing containerized workloads and services, that facilitates both declarative configuration and automation. It has a large, rapidly growing ecosystem. Kubernetes services, support, and tools are widely available. The name Kubernetes originates from Greek, meaning helmsman or pilot. Google open-sourced the Kubernetes project in 2014. Kubernetes combines over 15 years of Google's experience running production workloads at scale with best-of-breed ideas and practices from the community. It aims to provide a platform for automating deployment, scaling, and operations of application containers across clusters of hosts. It works with a range of container tools and runs containers in a cluster, often with images built using Docker. Kubernetes originally interfaced with the Docker runtime through a Dockershim; however, the shim has since been deprecated in favor of directly interfacing with containerd or another CRI-compliant runtime. Many cloud services offer a Kubernetes-based platform or infrastructure as a service (PaaS or IaaS) on which Kubernetes can be deployed as a platform-providing service. Many vendors also provide their own branded Kubernetes distributions."
doc_f = 'The Internet of things (IoT) describes the network of physical objects—“things”—that are embedded with sensors, software, and other technologies for the purpose of connecting and exchanging data with other devices and systems over the Internet. Things have evolved due to the convergence of multiple technologies, real-time analytics, machine learning, commodity sensors, and embedded systems.[1] Traditional fields of embedded systems, wireless sensor networks, control systems, automation (including home and building automation), and others all contribute to enabling the Internet of things. In the consumer market, IoT technology is most synonymous with products pertaining to the concept of the "smart home", including devices and appliances (such as lighting fixtures, thermostats, home security systems and cameras, and other home appliances) that support one or more common ecosystems, and can be controlled via devices associated with that ecosystem, such as smartphones and smart speakers. IoT can also be used in healthcare systems. There are a number of serious concerns about dangers in the growth of IoT, especially in the areas of privacy and security, and consequently industry and governmental moves to address these concerns have begun including the development of international standards.'
doc_g = "Enhanced mobile broadband (eMBB) is, in simple terms, an extension of services first enabled by 4G LTE networks that allows for a high data rate across a wide coverage area. eMBB will provide the greater capacity necessary to support peak data rates both for large crowds and for end users who are on the move. For data-hungry consumers and enterprises, this is the key to a faster, more reliably connected experience across many applications. Depending on the use case, eMBB will need to adapt to difference scenarios. Where there are many users who are not moving quickly, like fans at a sporting event, the network will need a high traffic capacity but a lower mobility requirement. However, for passengers on a commuter train, for example, there will be a greater demand for mobility but at a lower capacity. Either way, seamless coverage is the ultimate goal: users can get connected and stay connected as they move anywhere within the eMBB service range."
doc_h = "In computing, lightweight software also called lightweight program and lightweight application, is a computer program that is designed to have a small memory footprint (RAM usage) and low CPU usage, overall a low usage of system resources. To achieve this, the software should avoid software bloat and code bloat and try to find the best algorithm efficiency. "
doc_i = "6LoWPAN is an acronym of IPv6 over Low -Power Wireless Personal Area Networks.[1] 6LoWPAN is the name of a concluded working group in the Internet area of the IETF.[2] The 6LoWPAN concept originated from the idea that 'the Internet Protocol could and should be applied even to the smallest devices,'[3] and that low-power devices with limited processing capabilities should be able to participate in the Internet of Things.[4] The 6LoWPAN group has defined encapsulation and header compression mechanisms that allow IPv6 packets to be sent and received over IEEE 802.15.4 based networks. IPv4 and IPv6 are the work horses for data delivery for local-area networks, metropolitan area networks, and wide-area networks such as the Internet. Likewise, IEEE 802.15.4 devices provide sensing communication-ability in the wireless domain. The inherent natures of the two networks though, are different."
doc_j = "LoRa (short for long range) is a spread spectrum modulation technique derived from chirp spread spectrum (CSS) technology. Semtech’s LoRa devices and wireless radio frequency technology is a long range, low power wireless platform that has become the de facto technology for Internet of Things (IoT) networks worldwide. LoRa devices and the open LoRaWAN® protocol enable smart IoT applications that solve some of the biggest challenges facing our planet: energy management, natural resource reduction, pollution control, infrastructure efficiency, disaster prevention, and more. Semtech’s LoRa devices and the LoRaWAN protocol have amassed several hundred known uses cases for smart cities, smart homes and buildings, smart agriculture, smart metering, smart supply chain and logistics, and more. With over 167 million devices connected to networks in 99 countries and growing, LoRa devices are creating a Smarter Planet."

# compile sample documents into a list
doc_set = [doc_a, doc_b, doc_c, doc_e, doc_f, doc_g, doc_h, doc_i, doc_j]

# list for tokenized documents in loop
texts = []

# loop through document list
for i in docs:
        # clean and tokenize document string
        raw = i.lower()
        raw = re.sub(r'[^a-z]+', ' ', raw)
        tokens = tokenizer.tokenize(raw)

        # remove stop words from tokens
        stopped_tokens = [i for i in tokens if not i in en_stop]

        # stem tokens
        stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]

        # add tokens to list
        texts.append(stemmed_tokens)

# turn our tokenized documents into a id <-> term dictionary
dictionary = corpora.Dictionary(texts)

# convert tokenized documents into a document-term matrix
corpus = [dictionary.doc2bow(text) for text in texts]

# generate LDA model
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=7, id2word=dictionary, passes=10, random_state=0)
dct = corpora.Dictionary(texts)
dct.doc2bow([x for x in doc_a])
print(ldamodel.print_topics())
print(ldamodel.get_document_topics(dct.doc2bow([x for x in doc_a])))
top_topic = max(ldamodel.get_document_topics(dct.doc2bow([x for x in doc_a])), key=itemgetter(1))
print(ldamodel.print_topics()[top_topic[0]])
print(ldamodel.print_topics()[top_topic[0]][1])