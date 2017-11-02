import sys
sys.path.append('..')
import yaml

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from technews_nlp_aggregator.persistence.article_dataset_repo import ArticleDatasetRepo
from technews_nlp_aggregator.nlp_model.common import ArticleLoader, TechArticlesSentenceTokenizer, TechArticlesCleaner
from nltk.tokenize import sent_tokenize

config = yaml.safe_load(open('../config.yml'))
db_config = yaml.safe_load(open(config["key_file"]))
db_url    = db_config["db_url"]
articleDatasetRepo = ArticleDatasetRepo(db_url)
articleLoader = ArticleLoader(articleDatasetRepo)
articleLoader.load_all_articles(True)

sentence_tokenizer = TechArticlesSentenceTokenizer()
article_cleaner    = TechArticlesCleaner()

def cleaned_text(title, text):

    text = article_cleaner.do_clean(text)
    text = sentence_tokenizer.clean_sentences(text)
    return "\n".join(text)

articleFilteredDF = articleLoader.articlesDF
con = articleDatasetRepo.get_connection()
for index, row in articleFilteredDF.iterrows():

    articleDatasetRepo.update_article_text(row["article_id"], cleaned_text(row["text"]), con)
    if (index % 100 == 0):
        print("Processed {} rows".format(index))





