import logging
import os

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from technews_nlp_aggregator.nlp_model.common import ArticleLoader
from technews_nlp_aggregator.nlp_model.generation import TfidfGenerator
from technews_nlp_aggregator.persistence.article_dataset_repo import ArticleDatasetRepo
from technews_nlp_aggregator.nlp_model.common import ArticleLoader, DefaultTokenizer, TechArticlesSentenceTokenizer, TechArticlesTokenExcluder
from technews_nlp_aggregator.persistence.article_dataset_repo import ArticleDatasetRepo
import yaml

from datetime import datetime
import yaml

config = yaml.safe_load(open('../config.yml'))
db_config = yaml.safe_load(open(config["db_key_file"]))

articleDatasetRepo = ArticleDatasetRepo(db_config["db_url"])
articleLoader = ArticleLoader(articleDatasetRepo)
articlesDF = articleLoader.load_all_articles(load_text=True)
tokenizer = DefaultTokenizer(sentence_tokenizer=TechArticlesSentenceTokenizer(), token_excluder=TechArticlesTokenExcluder())
models_dir = config["lsi_models_dir_base"] + datetime.now().isoformat()+'/'

os.mkdir(models_dir)

tfidfGenerator = TfidfGenerator(articlesDF, models_dir, tokenizer)
tfidfGenerator.create_model()


if os.path.islink(config["lsi_models_dir_link"]):
    os.unlink(config["lsi_models_dir_link"])

os.symlink(models_dir,config["lsi_models_dir_link"])
