MIN_FREQUENCY = 3
DICTIONARY_FILENAME   = 'dictionary'
CORPUS_FILENAME       = 'corpus'
LSI_FILENAME          = 'lsi'
INDEX_FILENAME        = 'index'


from gensim import corpora, models, similarities
from gensim.corpora import MmCorpus

from .tfidf_matrix_wrapper import TfidfMatrixWrapper
import numpy as np
from . import ClfFacade
import logging



class TfidfFacade(ClfFacade):

    def __init__(self, model_dir, article_loader=None, gramFacade=None, tokenizer=None):
        self.model_dir = model_dir
        self.article_loader = article_loader
        self.name = 'TFIDF-V4-500'
        self.gramFacade = gramFacade
        self.tokenizer = tokenizer

    def load_models(self):
        self.dictionary = corpora.Dictionary.load(self.model_dir + '/'+DICTIONARY_FILENAME)  # store the dictionary, for future reference
        self.corpus = MmCorpus(self.model_dir + '/'+ CORPUS_FILENAME )
        self.lsi = models.LsiModel.load(self.model_dir + '/'+ LSI_FILENAME)
        self.matrix_wrapper = TfidfMatrixWrapper(similarities.MatrixSimilarity.load(self.model_dir + '/'+ INDEX_FILENAME))  # transform corpus to LSI space and index it

    def compare_docs_to_id(self,title, doc, id):
        vec_lsi = self.get_vec(title, doc)
        condition = self.article_loader.articlesDF.index == id
        scores = self.matrix_wrapper[(vec_lsi, condition )]
        return scores

    def compare_sentences_to_id(self, sentences, id):
        condition = self.article_loader.articlesDF.index == id
        vec_lsis = []
        for sentence in sentences:
            p_words = self.get_tokenized(sentence)
            vec_bow = self.dictionary.doc2bow(p_words)
            vec_lsi = self.lsi[vec_bow]  # convert the query to LSI space
            vec_lsis.append(vec_lsi)
        scores = self.matrix_wrapper.get_for_corpus(vec_lsis, id)
        return scores


    def get_vec(self, title, doc):
        vec_bow = self.get_doc_bow(doc, title)
        vec_lsi = self.lsi[vec_bow]  # convert the query to LSI space
        return vec_lsi

    def get_doc_bow(self, title, doc):
        p_words = self.get_tokenized(doc, title)
        vec_bow = self.dictionary.doc2bow(p_words)
        return vec_bow

    def get_tokenized(self, doc, title=''):
        words = self.tokenizer.tokenize_doc(title, doc)
        p_words = self.gramFacade.phrase(words)
        return p_words

    def get_vec_docid(self, id):

        vec_bow = self.corpus[id]
        vec_lsi = self.lsi[vec_bow]  # convert the query to LSI space
        return vec_lsi

    def docs_in_model(self):
        return self.corpus.num_docs

    def get_related_articles_and_score_doc(self, doc, start=None, end=None, title=''):
        articlesModelDF = self.article_loader.articlesDF.iloc[:self.corpus.num_docs]
        vec_lsi = self.get_vec(title, doc)
        if (start and end):
            interval_condition = (articlesModelDF ['date_p'] >= start) & (articlesModelDF ['date_p'] <= end)
            scores = self.matrix_wrapper[(vec_lsi, interval_condition) ]
            articlesFilteredDF = articlesModelDF [interval_condition ]
        else:
            scores = self.matrix_wrapper[(vec_lsi,None)]
            articlesFilteredDF = articlesModelDF
        args_scores = np.argsort(-scores)
        return articlesFilteredDF.iloc[args_scores].index, scores[args_scores]




    def get_related_articles_and_score_url(self,  url, d_days = 30   ):
        articlesModelDF= self.article_loader.articlesDF.iloc[:self.corpus.num_docs]
        url_condition = articlesModelDF['url'] == url
        docrow = articlesModelDF[url_condition]
        if (len(docrow) > 0):
            docid = docrow.index[0]
            url_date = docrow.iloc[0]['date_p']
            interval_condition = abs((articlesModelDF['date_p'] - url_date).dt.days) <= d_days

            articlesFilteredDF = articlesModelDF[interval_condition]

            vec_lsi = self.get_vec_docid(docid)
            scores = self.matrix_wrapper[(vec_lsi,interval_condition)]
            args_scores = np.argsort(-scores)
            return articlesFilteredDF.iloc[args_scores].index, scores[args_scores]
        else:
            return None, None

    def compare_articles_from_dates(self,  start, end, thresholds):
        articles_and_sim = {}
        interval_condition = (self.article_loader.articlesDF['date_p'] >= start) & (self.article_loader.articlesDF['date_p'] <= end)
        articlesFilteredDF = self.article_loader.articlesDF[interval_condition]
        dindex = articlesFilteredDF.index
        for id in dindex:
            vec_lsi = self.get_vec_docid(id)
            scores = self.matrix_wrapper[(vec_lsi,interval_condition)]
            scores_in_threshold_condition = (scores >= thresholds[0]) &  (scores <= thresholds[1])
            scores_in_threshold = scores[scores_in_threshold_condition]
            id_in_threshold = articlesFilteredDF.index[scores_in_threshold_condition]

            articles_and_sim[id] = zip(id_in_threshold, scores_in_threshold)
        return articles_and_sim




