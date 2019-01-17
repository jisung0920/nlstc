# -*- coding: utf-8 -*-
import json
from rake_nltk import Rake
from vocabulary.vocabulary import Vocabulary as vb

class WordParser:

    sentence = ""
    keywords = []
    key_tokens = []
    syn_words = []
    keyword_limit = 3
    synonym_limit = 2

    def __init__(self, sentence, keyword_limit=3, synonym_limit=2):

        self.sentence = sentence
        self.keyword_limit = keyword_limit
        self.synonym_limit = synonym_limit

        self.keywords = self.parse_keywords()
        self.key_tokens = self.parse_tokens(self.keywords)
        self.syn_words = self.parse_keyword_synonym(self.key_tokens)

    def parse_keywords(self):
        sentences = [self.sentence]
        r = Rake()
        r.extract_keywords_from_sentences(sentences)
        keywords = r.ranked_phrases
        return keywords[0:self.keyword_limit]

    def parse_tokens(self,keywords):
        tokens = []
        for keyword in keywords :
            raw_tokens = keyword.split(' ')
            for token in raw_tokens :
                if token.isdigit() :
                    continue
                tokens.append(token)
        return tokens

    def parse_keyword_synonym(self, tokens):
        synonyms = []
        # print vb.synonym("test")
        for token in tokens:
            # print token+": \n"
            # print json.loads(vb.synonym(token))
            # vb.
            try :
                data =  json.loads(vb.synonym(token))[0:self.synonym_limit]
                for word_txt in data :
                    synonyms.append(word_txt["text"])
                # synonyms = synonyms + json.loads(vb.synonym(token))["text"]
                # [0:self.synonym_limit]
            except:
                continue
        return synonyms

    def query_generator(self, file_types):
        querys = []
        words_txt = '~' + " or ~".join(self.key_tokens)
        for file_type in file_types :
            querys.append(words_txt + " filetype:" + file_type)
        return querys

    def searching_word_generator(self):
        return self.key_tokens + self.syn_words
