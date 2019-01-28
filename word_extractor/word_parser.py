# -*- coding: utf-8 -*-
import json
from rake_nltk import Rake
from vocabulary.vocabulary import Vocabulary as vb


"""
WordParser is created and execute parsing function at the same time.
function - parse_keywords / parse_tokens(keywords) / parse_keyword_synonym(token) 
It can use one sentence per object
"""
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

    """
    Find keyword from sentence
    use rake_nltk API
    rake API return scored list (all token)
    To improve search time, should limit the number
    return word list - len:keyword_limit
    """
    def parse_keywords(self):
        sentences = [self.sentence]
        r = Rake()
        r.extract_keywords_from_sentences(sentences)
        keywords = r.ranked_phrases
        return keywords[0:self.keyword_limit]

    """
    One keyword can be more than 2 words
    To use synonym API, should split this. 
    return keyword token list 
    """
    def parse_tokens(self,keywords):
        tokens = []
        for keyword in keywords :
            raw_tokens = keyword.split(' ')
            for token in raw_tokens :
                if token.isdigit() :
                    continue
                tokens.append(token)
        return tokens

    """
    Find synonyms of tokens
    use Vocabulary API
    To improve search time, should limit the number
    """
    def parse_keyword_synonym(self, tokens):
        synonyms = []
        for token in tokens:
            try :
                data =  json.loads(vb.synonym(token))[0:self.synonym_limit]
                for word_txt in data :
                    synonyms.append(word_txt["text"])
            except:
                continue
        return synonyms

    """
    Make qurey in google search form
    use key token(not synonym)
    ex) "~A or ~B or ~C filetype:html"
    return query list 
    """
    def query_generator(self, file_types):
        querys = []
        words_txt = '~' + " or ~".join(self.key_tokens)
        for file_type in file_types :
            querys.append(words_txt + " filetype:" + file_type)
        return querys

    """
    return tokens + synonyms in sentence
    """
    def searching_word_generator(self):
        return self.key_tokens + self.syn_words
