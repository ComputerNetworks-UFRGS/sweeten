#!/usr/bin/env python
import docker
import requests
import bs4
from operator import itemgetter


def get_enriched_description(imageName):
    queryText = imageName
    url = "https://google.com/search?q=define+" + queryText
    requestResult = requests.get(url)
    enrichedDescription = bs4.BeautifulSoup(requestResult.text, "html.parser").find("div", class_='BNeawe').text
    return enrichedDescription


def get_container_info_from_docker(imageName):
    client = docker.from_env()
    client.images.pull(imageName)
    dockerImage = client.images.get(imageName)
    imageTagsReadDict = dockerImage.tags
    try:
        imageDescription = dockerImage.labels["description"]
        # print("Image default description: " + imageDescription)
    except:
        imageDescription = ""
        # print("No default image description available")
    return dockerImage, imageTagsReadDict, imageDescription


def addTagsToContainerImage(imageName):
    dockerImage, imageDefaultTags, imageDefaultDescription = get_container_info_from_docker(imageName)
    enrichedDescription = get_enriched_description(imageName)

    with open('input/descriptions.txt') as f:
        docs = f.readlines()

    for i, doc in enumerate(docs[:-1]):
        docs[i] = doc[:-1]

    current_doc = get_enriched_description(imageName)
    docs.append(current_doc)

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
    dct.doc2bow([x for x in current_doc])
    top_topic = max(ldamodel.get_document_topics(dct.doc2bow([x for x in current_doc])), key=itemgetter(1))
    return top_topic
    # print(ldamodel.print_topics())
    # print(ldamodel.get_document_topics(dct.doc2bow([x for x in current_doc])))
    # print(ldamodel.print_topics()[top_topic[0]])
    # print(ldamodel.print_topics()[top_topic[0]][1])
