import logging
import pickle
import os

from datetime import datetime
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import yaml
from technews_nlp_aggregator.persistence import ArticleDatasetRepo
from technews_nlp_aggregator.nlp_model.common import ArticleLoader, defaultTokenizer
import argparse
import sys

def create_pickle( config , articleLoader, tokenizer, limit=None):

    logging.info("Articles loaded : {} ".format(len(articleLoader.articlesDF)))
    articleFilterDF = articleLoader.articlesDF[:limit] if limit else articleLoader.articlesDF
    texts_df = tokenizer.tokenize_ddf(articleFilterDF )
    texts = texts_df.tolist()
    if (not limit):
        save_picke_file(config, texts)


def save_picke_file(config, texts):
    core_name = 'texts_'
    pickle_file = config["pickle_dir"] + core_name + datetime.now().isoformat() + '.p'

    logging.info("Articles saved in pickle file : {} ".format(len(texts)))
    with open(pickle_file, 'wb') as f:
        pickle.dump(texts, f)
    if os.path.islink(config["text_pickle_file"]):
        os.unlink(config["text_pickle_file"])
    os.symlink(pickle_file, config["text_pickle_file"])


def update_pickle(config, articleLoader, tokenizer):

    pickle_file = config["text_pickle_file"]
    with open(pickle_file, 'rb') as f:
        texts = pickle.load(f)
        logging.info("Loaded {} texts".format(len(texts)))
        logging.info("Articles loaded : {} ".format(len(articleLoader.articlesDF)))
        logging.info("Articles loaded : {} ".format(len(articleLoader.articlesDF)))

        articlesNewDF = articleLoader.articlesDF.iloc[len(texts):]
        new_texts =  tokenizer.tokenize_ddf(articlesNewDF )
        texts = texts + new_texts
        save_picke_file(config, texts)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--action', help='action can be create or append')
    args = parser.parse_args()


    config = yaml.safe_load(open('config.yml'))
    db_config = yaml.safe_load(open(config["key_file"]))
    db_url = db_config["db_url"]
    articleDatasetRepo = ArticleDatasetRepo(db_config.get("db_url"), db_config.get("limit"))
    articleLoader = ArticleLoader(articleDatasetRepo)
    articleLoader.load_all_articles(True)
    if (args.action == 'append'):
        update_pickle(config, articleLoader, defaultTokenizer)
    elif (args.action == 'create'):
        create_pickle(config , articleLoader, defaultTokenizer)
    else:
        print("Please choose create or append")
        sys.exit(1)




