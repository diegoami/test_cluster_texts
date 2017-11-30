#!/bin/bash

[ $? -eq 0 ] &&  python scrape_site.py
[ $? -eq 0 ] &&  python scrape_urls.py
[ $? -eq 0 ] &&  python token_model_wf.py --action append
[ $? -eq 0 ] &&  python gram_model_wf.py
[ $? -eq 0 ] &&  python gram_export_wf.py
[ $? -eq 0 ] &&  python tfidf_dictionary_wf.py
[ $? -eq 0 ] &&  python tfidf_model_wf.py
[ $? -eq 0 ] &&  python tfidf_matrix_wf.py
[ $? -eq 0 ] &&  python doc2vec_model_wf.py
[ $? -eq 0 ] &&  python similar_articles_eff.py


