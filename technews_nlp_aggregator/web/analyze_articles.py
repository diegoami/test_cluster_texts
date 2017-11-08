from flask import  request, render_template, session
from technews_nlp_aggregator.nlp_model.spacy.utils import retrieve_entities

import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import traceback

from . import app
from .util import highlight_entities

#
DEFAULT_FILTER_CRITERIA = 'T_SCORE > 0.8 AND D_SCORE > 0.4 OR ( U_SCORE > 0.5 )'

@app.route('/filterduplicates', methods=['POST'])
def filterduplicates():
    if request.method == 'POST':
        form = request.form
        if form:
            filterCriteria = form["filterCriteria"]
            session['filterCriteria'] = request.form['filterCriteria']
    return duplicates(0)

@app.route('/duplicates/<int:page_id>')
def duplicates(page_id=0):
    _ = app.application
    filter_criteria = session.get('filterCriteria', DEFAULT_FILTER_CRITERIA )
    messages = []
    try:
        all_articles = _.similarArticlesRepo.list_similar_articles(filter_criteria=filter_criteria )
        start, end = page_id*100, (page_id+1)*100
        if (len(all_articles) > start):
            has_next = len(all_articles) > end
            dup_articles = all_articles[start:min(end,len(all_articles))]
        else:
            dup_articles = []
            return render_template('duplicates.html', messages=['No articles found with this query'],
                                   filter_criteria=filter_criteria)

        return render_template('duplicates.html', dup_articles=dup_articles, page_id=page_id, has_next=has_next, filter_criteria=filter_criteria)
    except:
        traceback.print_exc()
        return render_template('duplicates.html',  filter_criteria=filter_criteria, messages=['Could not execute query - filter criteria are not valid'])


@app.route('/examples')
def examples(page_id=0):
    _ = app.application
    yes_articles = _.similarArticlesRepo.list_similar_articles(filter_criteria=" U_SCORE > 0.9 ")
    almost_articles = _.similarArticlesRepo.list_similar_articles(filter_criteria=" U_SCORE > 0.3 AND U_SCORE < 0.7 ")
    return render_template('examples.html', yes_examples=yes_articles[:8], almost_examples=almost_articles[:8] )



@app.route('/compare/<int:id1>/<int:id2>')
def compare(id1, id2):
    _ = app.application
    article1, article2 = _.articleDatasetRepo.load_articles_with_text(id1, id2)
    article1["ATX_TEXT"], article2["ATX_TEXT"] = _.tokenizer.clean_text(article1["ATX_TEXT"]), _.tokenizer.clean_text(article2["ATX_TEXT"])
    article1["ORGANIZATIONS"], article1["PERSONS"], article1["NOUNS"] = retrieve_entities(article1["ATX_TEXT"])
    article2["ORGANIZATIONS"], article2["PERSONS"], article2["NOUNS"] = retrieve_entities(article2["ATX_TEXT"])
    highlight_entities(article1, article1["ORGANIZATIONS"], article1["PERSONS"], article1["NOUNS"])
    highlight_entities(article2, article2["ORGANIZATIONS"], article2["PERSONS"], article2["NOUNS"])

    return render_template('to_compare.html', A1=article1, A2=article2)

@app.route('/summary/<int:article_id>')
def summary(article_id):
    _ = app.application
    id =  _.articleLoader.articlesDF[_.articleLoader.articlesDF['article_id'] == article_id].index[0]
    article = _.articleDatasetRepo.load_article_with_text( article_id )
    summary_sentences = _.summaryFacade.summarize(article["AIN_TITLE"], article["ATX_TEXT"], id)
    result = ""
    for entry in summary_sentences:
        if entry["highlighted"]:
            result = result + " <B> " + entry["sentence"] +"</B>"
        else:
            result =  result + " " + entry["sentence"]
    return result, {'Content-Type': 'text/html'}

@app.route('/randomrelated')
def randomrelated():
    _ = app.application
    id1, id2 = _.similarArticlesRepo.retrieve_random_related()

    return compare(id1, id2)

def save_user_association(id1,id2, similarity):
    _ = app.application
    _.similarArticlesRepo.persist_user_association(id1, id2, similarity, request.environ['REMOTE_ADDR'])
    return randomrelated()

def save_user_association_xhr(id1,id2, similarity):
    _ = app.application
    _.similarArticlesRepo.persist_user_association(id1, id2, similarity, request.environ['REMOTE_ADDR'])
    return str(similarity), {'Content-Type': 'text/html'}

@app.route('/samestory/<int:id1>/<int:id2>')
def samestory(id1, id2):
    return save_user_association(id1,id2, 1.0)

@app.route('/related/<int:id1>/<int:id2>')
def related(id1, id2):
    return save_user_association(id1, id2, 0.5)

@app.route('/unrelated/<int:id1>/<int:id2>')
def unrelated(id1, id2):
    return save_user_association(id1, id2, 0.0)


@app.route('/samestory_xhr/<int:id1>/<int:id2>')
def samestory_xhr(id1, id2):
    return save_user_association_xhr(id1, id2, 1.0)

@app.route('/related_xhr/<int:id1>/<int:id2>')
def related_xhr(id1, id2):
    return save_user_association_xhr(id1, id2, 0.5)

@app.route('/unrelated_xhr/<int:id1>/<int:id2>')
def unrelated_xhr(id1, id2):
    return save_user_association_xhr(id1, id2, 0.0)


