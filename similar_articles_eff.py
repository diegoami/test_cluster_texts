

import yaml
import traceback
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)

from technews_nlp_aggregator import Application


def process_for_insertion(id, ids, scores, threshold, articleFilterDF):

    for other_id, score in zip(ids, scores):
        if score >= threshold and score < 0.995:
            article_id, article_other_id = articleFilterDF.iloc[id]['article_id'], articleFilterDF.iloc[other_id]['article_id']
            logging.debug("Yielding {}, {}, {}".format(article_id, article_other_id, score))
            yield (article_id, article_other_id, score)



def eff_similar_articles(application):
    _ = application
    articleFilterDF = _.articleLoader.articlesDF[:_.tfidfFacade.docs_in_model()]
    articlesToProcessDF =  articleFilterDF [_.articleLoader.articlesDF['processed'].isnull()]

    for id, row in articlesToProcessDF.iterrows():
        article_id = row['article_id']
        article_date = row['date_p']
        logging.debug("Processing article : {}".format(article_id))

        tfd_ids, tdf_scores = _.tfidfFacade.get_related_articles_for_id(2, id, article_date)
        doc2vec_ids, doc2vec_scores = _.doc2VecFacade.get_related_articles_for_id(2, id, article_date)
        con = _.similarArticlesRepo.get_connection()
        try:
            con.begin()
            for article1, article2, score in process_for_insertion(id, tfd_ids, tdf_scores, 0.6, articleFilterDF):
                _.similarArticlesRepo.persist_association(con, article1, article2,  _.tfidfFacade.name, score)

            for article1, article2, score in process_for_insertion(id,  doc2vec_ids, doc2vec_scores, 0.26,  articleFilterDF):
                _.similarArticlesRepo.persist_association(con, article1, article2, _.doc2VecFacade.name, score)

            _.similarArticlesRepo.update_to_processed(article_id, con)
            con.commit()
        except:
            traceback.print_exc()
            con.rollback()




if __name__ == '__main__':

    config = yaml.safe_load(open('config.yml'))
    application = Application(config, True)
    eff_similar_articles(application)
