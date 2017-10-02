import json


from gensim import corpora, models, similarities

import os

from gensim.corpora import MmCorpus

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import string

from os import listdir
from os.path import isfile, join
from gensim.models.doc2vec import TaggedDocument
from datetime import datetime
import json
from gensim.models import Doc2Vec



MIN_FREQUENCY = 3
MODEL_FILENAME   = 'doc2vec'


import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class LabeledLineSentence(object):
    def __init__(self, doc_list, labels_list):
        self.labels_list = labels_list
        self.doc_list = doc_list

    def __iter__(self):
        for idx, doc in enumerate(self.doc_list):
            wtok = [i for i in word_tokenize(doc.lower())]
            tags = [self.labels_list[idx]]

            yield TaggedDocument(words=wtok, tags=tags)

class Doc2VecGenerator:


    def __init__(self, article_map, model_output_dir):
        self.article_map = article_map
        self.model_output_dir = model_output_dir


    def create_model(self):
        urls  = [self.article_map[article]["url"] for article in self.article_map]

        texts = [self.article_map[article]["text"] for article in self.article_map]

        it = LabeledLineSentence(texts, urls)

        self.model = Doc2Vec(size=300, window=10, min_count=MIN_FREQUENCY, workers=11, alpha=0.025, min_alpha=0.025,
                             iter=10)  # use fixed learning rate
        self.model.build_vocab(it)

        logging.info("Starting to train......")

        # for epoch in range(10):
        #    logging.info("On epoch "+str(epoch))
        # model.train(it)
        # model.alpha -= 0.002 # decrease the learning rate
        # model.min_alpha = model.alpha # fix the learning rate, no deca
        self.model.train(it, total_examples=self.model.corpus_count, epochs=self.model.iter)
        #   logging.info("Finished training epoch " + str(epoch))

        logging.info("Training completed, saving to  " + self.model_output_dir)
        self.model.save(self.model_output_dir+MODEL_FILENAME )





