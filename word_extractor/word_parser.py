# -*- coding: utf-8 -*-
import json
from rake_nltk import Rake
from vocabulary.vocabulary import Vocabulary as vb


def query_generator(sentence,key_num,syn_num,file_types) :

    parser = WordParser(sentence,key_num,syn_num)
    keywords = parser.get_keywords()
    key_tokens = parser.get_tokens(keywords)

    return parser.get_query(key_tokens,file_types)

def searching_word_generator(sentence,key_num,syn_num) :

    parser = WordParser(sentence,key_num,syn_num)
    keywords = parser.get_keywords()
    key_tokens = parser.get_tokens(keywords)
    syn_words = parser.get_keyword_synonym(key_tokens)
    search_word = key_tokens + syn_words

    return search_word

class WordParser:
    sentence = ""
    keyword_limit = 3
    synonym_limit = 2

    def __init__(self, sentence, keyword_limit=3, synonym_limit=2):
        self.sentence = sentence
        self.keyword_limit = keyword_limit
        self.synonym_limit = synonym_limit

    def get_keywords(self):
        sentences = [self.sentence]
        r = Rake()
        r.extract_keywords_from_sentences(sentences)
        keywords = r.ranked_phrases
        return keywords[0:self.keyword_limit]

    def get_tokens(self,keywords):
        tokens = []
        for keyword in keywords :
            raw_tokens = keyword.split(' ')
            for token in raw_tokens :
                if token.isdigit() :
                    continue
                tokens.append(token)
        return tokens

    def get_keyword_synonym(self, tokens):
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

    @staticmethod
    def get_query(words, file_types):
        querys = []
        words_txt = '~' + " or ~".join(words)
        for file_type in file_types :
            querys.append(words_txt + " filetype:" + file_type)
        return querys
