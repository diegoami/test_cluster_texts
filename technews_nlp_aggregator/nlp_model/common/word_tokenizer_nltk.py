
from nltk.tokenize import sent_tokenize, word_tokenize

chars_to_remove = ['“', '”']


class NltkWordTokenizer:



    def tokenize_sentence(self, all_sentences):
        tokenized_sentences = []
        for sentence in all_sentences:
            tokenized_sentences.append([word for word in word_tokenize(sentence.lower())])
        return tokenized_sentences