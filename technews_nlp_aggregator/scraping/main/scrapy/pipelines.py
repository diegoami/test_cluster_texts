# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from technews_nlp_aggregator.persistence import ArticleDatasetRepo

class Pipeline(object):
    def process_item(self, item, spider):
        #print(item)
        #text = item['text']
        #sentences = sent_tokenize(text)
        #for sentence in sentences:
        #    print(sentence)

        if (len(item["title"]) >= 10) and (len(item["text"]) >= 600) and item["date"]:
            spider.article_repo.save_article( item["url"], item, item["text"])
        return item