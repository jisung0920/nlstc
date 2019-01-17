from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO


class LinkMiner:
    search_engine = "https://www.google.com/search"
    query = ''
    hdr = {'User-Agent': 'Mozilla/5.0'}

    def __init__(self, engine, query):
        self.search_engine = engine
        self.query = query

    """
        getLink(str, str) : list
        검색url 링크와 검색어를 입력 받는다.
        검색결과에서 모든 link를 찾는다.
    """

    def req_value(self):
        values = {'q': self.query,
                  'oq': self.query,
                  'aqs': 'chrome..69i57.35694j0j7',
                  'sourceid': 'chrome',
                  'ie': 'UTF-8', }
        return values

    def get_links(self):

        # 검색을 위한 request 생성
        query_string = urllib.urlencode(req_value())
        url_link = self.search_engine + '?' + query_string
        req = urllib2.Request(url_link, headers=hdr)
        context = ssl._create_unverified_context()

        # URL open 과 html respone 처리
        res = urllib2.urlopen(req, context=context).read()
        html_data = BS(res, 'html.parser')

        # html 파싱 : link 찾기
        get_details = html_data.find_all("div", attrs={"class": "g"})
        links = []
        for details in get_details:
            link = details.find_all("h3")
            for mdetails in link:
                links = mdetails.find_all("a")
                lmk = ""
                for lnk in links:
                    lmk = lnk.get("href")[7:].split("&")
                    result.append(str(lmk[0]))

        return links


def url_filter(url_list):
    links = []
    for link in url_list:
        if 'www.youtube.com' in link:
            continue
        if 'https://' not in link:
            continue
        links.append(link)
    return links


class Crawler:
    tokens = []

    def __init__(self, tokens):
        self.tokens = tokens

    def html_crawler(base_url, tokens, tag='div'):
        req = requests.get(base_url)
        html = req.text
        html_data = BS(html, 'html.parser')

        html_content = html_data.find_all(tag)

        search_sentences = []

        for contents in html_content:
            sentences = nltk.tokenize.sent_tokenize(contents.text)
            for sentence in sentences:
                for token in tokens:
                    if token.lower() in sentence.lower():
                        search_sentences.append(sentence)

        search_sentences = list(set(search_sentences))

        return search_sentences

    def pdf_crawler(url):
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)

        scrape = urllib2.urlopen(url).read()
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

        for contents in pdf_contents:
            sentences = nltk.tokenize.sent_tokenize(contents.text)
            for sentence in sentences:
                for token in tokens:
                    if token.lower() in sentence.lower():
                        search_sentences.append(sentence)

        search_sentences = list(set(search_sentences))

        return search_sentences
