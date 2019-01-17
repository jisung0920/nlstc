# -*- coding: utf-8 -*-
from rake_nltk import Rake
from vocabulary.vocabulary import Vocabulary as vb


class WordParser:
    sentence = ''
    keyword_limit = 3
    synonym_limit = 2

    def __init__(self, sentence, keyword_limit=3, synonym_limit=2):
        self.sentence = sentence
        self.keyword_limit = keyword_limit
        self.synonym_limit = synonym_limit

    def get_keywords(self):
        r = Rake()
        r.extract_keywords_from_sentences(self.sentence)
        keywords = r.ranked_phrases
        return keywords[0:self.keyword_limit]

    def get_keyword_synonym(self, keywords):
        synonyms = []
        for keyword in keywords:
            synonyms = synonyms + json.loads(vb.synonym(keyword))[0:self.synonyms_limit]
        return synonyms

    @staticmethod
    def get_query(words, file_types):
        querys = []
        words_txt = '~' + " or ~".join(words)
        for file_type in file_types
            querys.add(words_txt + " filetype:" + file_type)
        return querys
