# -*- coding: utf-8 -*-
import nltk
import urllib, urllib2
import requests
import re
from bs4 import BeautifulSoup as BS
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

"""
LinkMiner is created and execute url parsing function at the same time.
function - request_creator() / link_searching() / url_filter() 
It can use one query(file type) per object
"""
class LinkMiner:

    search_engine = "https://www.google.com/search" #default : google
    query = ''
    request = ''
    url_list = []

    def __init__(self, engine, query):
        self.search_engine = engine
        self.query = query
        self.request = self.request_creator()
        self.url_list = self.link_searching()
        self.url_list = self.url_filter()

    #create web request using query(variable) 
    def request_creator(self):

        values = {'q': self.query,
                  'oq': self.query,
                  'aqs': 'chrome..69i57.35694j0j7',
                  'sourceid': 'chrome',
                  'ie': 'UTF-8', }

        hdr = {'User-Agent': 'Mozilla/5.0'}

        query_string = urllib.urlencode(values)
        url_link = self.search_engine + '?' + query_string
        req = urllib2.Request(url_link, headers=hdr)

        return req

    
    #Get html data and parse url
    
    def link_searching(self):
        # get html data
        res = urllib2.urlopen(self.request).read()
        html_data = BS(res, 'html.parser')
        
        # parse url
        get_details = html_data.find_all("div", attrs={"class": "g"})
        result = []

        for details in get_details:
            link = details.find_all("h3")
            for mdetails in link:
                links = mdetails.find_all("a")
                # lmk = ""
                for lnk in links:
                    lmk = lnk.get("href")[7:].split("&")
                    result.append(str(lmk[0]))

        return result

    def url_filter(self):
        links = []
        for link in self.url_list:
            if 'www.youtube.com' in link:
                continue
            if 'https://' not in link:
                continue
            links.append(link)
        return links

"""
SentenceCrawler find sentence in links
can find from html and pdf file
"""
class SentenceCrawler:

    tokens = []

    def __init__(self, search_tokens):
        self.tokens = search_tokens

    # use nltk API
    def html_crawler(self, link, tag='div'):

        try :
            req = requests.get(link)
        except :
            return []

        html = req.text
        html_data = BS(html, 'html.parser')

        html_content = html_data.find_all(tag)

        search_sentences = []

        for contents in html_content:
            try :
                sentences = nltk.tokenize.sent_tokenize(contents.text)
                for sentence in sentences:
                    for token in self.tokens:
                        if self.sentence_filter(sentence) and (token.lower() in sentence.lower()):
                            search_sentences.append(sentence)
                            break
            except : continue
        search_sentences = list(set(search_sentences))

        return search_sentences

    # use pdfminer API
    def pdf_crawler(self,link):

        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
        try :
            scrape = urllib2.urlopen(link).read()
        except :
             return []
        fp = StringIO(scrape)

        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos = set()
        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching,
                                      check_extractable=True):
            interpreter.process_page(page)

        fp.close()
        device.close()
        pdf_contents = retstr.getvalue()
        retstr.close()

        search_sentences = []

        for contents in pdf_contents:
            try :
                sentences = nltk.tokenize.sent_tokenize(contents.text)
                for sentence in sentences:
                    for token in self.tokens:
                        if self.sentence_filter(sentence) and ( token.lower() in sentence.lower() ):
                            search_sentences.append(sentence)
                            break
            except : continue
        search_sentences = list(set(search_sentences))

        return search_sentences

    def sentence_filter(self, sentence) :

        if len(sentence)>100 :
            return False
        if "  " in sentence  :
            return False
        if '.' not in sentence :
            return False
        pattern = '[^.a-zA-Z0-9\[\]]'
        if bool(re.match(pattern,sentence)):
            return False

        return True

def sentence_crawling(search_tokens,link_chunk,link_dic,file_types) :

    crawler = SentenceCrawler(search_tokens)
    sentences = []

    for i in range(len(file_types)):
        if file_types[i] is "html":
            for link in link_chunk[i]:
                html_sents = crawler.html_crawler(link)
                for sent in html_sents :
                    link_dic[sent] = link
                sentences = sentences + html_sents
        if file_types[i] is "pdf" :
            for link in link_chunk[i]:
                pdf_sents = crawler.pdf_crawler(link)
                for sent in pdf_sents :
                    link_dic[sent] = link
                sentences = sentences + pdf_sents
    return sentences

#create txt file to use at sentence compare
def learningFormatting(input_sentence, sentences,file_path):
    file = open(file_path,"w")
    for entry in sentences :
        sentence = '0\t' +input_sentence+'\t'+entry+'\n'
        file.write(sentence.encode('utf8'))

    file.close()
    return file_path