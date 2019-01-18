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


class LinkMiner:

    search_engine = "https://www.google.com/search"
    query = ''
    request = ''
    url_list = []

    def __init__(self, engine, query):
        self.search_engine = engine
        self.query = query
        self.request = self.request_creator()
        self.url_list = self.link_searching()
        self.url_list = self.url_filter()

    def link_searching(self):
        res = urllib2.urlopen(self.request).read()
        html_data = BS(res, 'html.parser')

        # html 파싱 : link 찾기
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

    def url_filter(self):
        links = []
        for link in self.url_list:
            if 'www.youtube.com' in link:
                continue
            if 'https://' not in link:
                continue
            links.append(link)
        return links


class SentenceCrawler:

    tokens = []

    def __init__(self, search_tokens):
        self.tokens = search_tokens

    def html_crawler(self, link, tag='div'):

        req = requests.get(link)
        html = req.text
        html_data = BS(html, 'html.parser')

        html_content = html_data.find_all(tag)

        search_sentences = []

        for contents in html_content:
            sentences = nltk.tokenize.sent_tokenize(contents.text)
            for sentence in sentences:
                for token in self.tokens:
                    if self.sentence_filter(sentence) and (token.lower() in sentence.lower()):
                        search_sentences.append(sentence)

        search_sentences = list(set(search_sentences))

        return search_sentences

    def pdf_crawler(self,link):

        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)

        scrape = urllib2.urlopen(link).read()
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

def sentence_crawling(search_tokens,link_chunk,file_types) :

    crawler = SentenceCrawler(search_tokens)
    sentences = []

    for i in range(len(file_types)) :
        if file_types[i] is "html" :
            for link in link_chunk[i] :
                sentences = sentences + crawler.html_crawler(link)
        if file_types[i] is "pdf" :
            for link in link_chunk[i]:
                sentences = sentences + crawler.pdf_crawler(link)

    return sentences

def learningFormatting(inputSentence, sentenceList,filePath):
    file = open(filePath,"w")
    for entry in sentenceList :
        sentence = '0\t' +inputSentence+'\t'+entry+'\n'
        file.write(sentence.encode('utf8'))

    file.close()
    return filePath