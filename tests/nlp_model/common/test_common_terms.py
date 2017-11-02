

from technews_nlp_aggregator.nlp_model.common import ArticleLoader, DefaultTokenizer, TechArticlesSentenceTokenizer, TechArticlesTokenExcluder
from technews_nlp_aggregator.persistence.article_dataset_repo import ArticleDatasetRepo
import yaml
from collections import Counter
import operator


config = yaml.safe_load(open('../../../config.yml'))
db_config = yaml.safe_load(open(config["key_file"]))
articleDatasetRepo = ArticleDatasetRepo(db_config["db_url"])
articleLoader = ArticleLoader(articleDatasetRepo)
articlesDF = articleLoader.load_all_articles(load_text=True,limit=300)
tokenizer = DefaultTokenizer(sentence_tokenizer=TechArticlesSentenceTokenizer(), token_excluder=TechArticlesTokenExcluder())
tokenized_docs = tokenizer.tokenize_ddf(articlesDF)
from collections import defaultdict

frequency = defaultdict(int)
for text in tokenized_docs:
    for token in text:
        frequency[token] += 1

sorted_freq = sorted(frequency .items(), key=operator.itemgetter(1), reverse=True)
sorted_keys = [x[0] for x in sorted_freq ]
print(sorted_keys[:100])

