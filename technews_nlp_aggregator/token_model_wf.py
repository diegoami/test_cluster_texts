import logging
import pickle
import os
import sys
from datetime import datetime
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import yaml
from technews_nlp_aggregator.application import Application

def create_pickle(application, config ):
    _ = application


    logging.info("Articles loaded : {} ".format(len(_.articleLoader.articlesDF)))

    texts = _.tokenizer.tokenize_ddf(_.articleLoader.articlesDF)
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


def update_pickle(application, config):
    _ = application
    pickle_file = config["text_pickle_file"]
    with open(pickle_file, 'rb') as f:
        texts = pickle.load(f)
        logging.info("Loaded {} texts".format(len(texts)))
        logging.info("Articles loaded : {} ".format(len(_.articleLoader.articlesDF)))
        logging.info("Articles loaded : {} ".format(len(_.articleLoader.articlesDF)))

        articlesNewDF = _.articleLoader.articlesDF.iloc[len(texts):]
        new_texts =  _.tokenizer.tokenize_ddf(articlesNewDF )
        texts = texts + new_texts
        save_picke_file(config, texts)


if __name__ == '__main__':
    import sys
    sys.path.append('..')
    config = yaml.safe_load(open('../config.yml'))
    application = Application(config, True)

    #create_pickle(application, config )
    update_pickle(application, config)




