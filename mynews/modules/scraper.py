import requests
from bs4 import BeautifulSoup
import newspaper
from newspaper import Article
import nltk
import time
import abc
import time
# region Interface
class IScraper(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_infos(self, soup):
        pass
# endregion

# region IScraperを実装した、各サイト専用のBeautifulSoupを使ったスクレイピング
class Scraper_GIGAZINE(IScraper):
    def get_infos(self, url):
        infos = []
        soup = get_soup(url)
        articles = soup.body.find_all('section')
        for article in articles:
            current_infos = []
            # URL / https://gigazine.net/news/20230731-minibrains-grown-international-space-station/
            url = article.find('a').attrs['href']
            if url is not None:
                current_infos.append(url)
            # タイトル / ヒトの「ミニ脳」が国際宇宙ステーションで作られる予定
            title = article.find('span').contents[0]
            if title is not None:
                current_infos.append(title)
            # 発行日 / 2023-07-31T14:00:00+09:00
            date = article.find('time').attrs['datetime']
            if date is not None:
                date_formatted = date[0:10]
                current_infos.append(date_formatted)
            # サイト / GIGAZINE
            current_infos.append('GIGAZINE')
            
            infos.append(current_infos)
        return infos
    
    def get_text(url):
        text = ''
        soup = get_soup(url)
        body = soup.find('body')
        tag_cntimage = body.find('div', attrs={'cntimage'})
        tag_prefaces = tag_cntimage.find_all('p', attrs={'preface'})
        text += tag_cntimage.get_text()
        # リンクのない、べた書きの本文
        # if tag_prefaces:
        #     for tag_preface in tag_prefaces:
        #         if tag_preface:
        #             for tag_preface_text in tag_preface.contents:
        #                 if tag_preface_text:
        #                     text += tag_preface_text
        # リンクのある本文
        # tag_a = tag_text.find_all("a")
        # if tag_a:
        #     for a in tag_a:
        #         text += a.string
        # text = tag_text.string
        return text

class Scraper_Publicky(IScraper):
    def get_infos(self, url):
        infos = []
        soup = get_soup(url)
        articles = soup.body.find_all('li')
        for article in articles:
            current_infos = []
            a = article.find('a')
            if a is not None:
                this_url = a.attrs['href']
                current_infos.append(this_url)
            else:
                continue
            a = article.find('a')
            if a is not None:
                if len(a.contents) > 1:
                    title = a.contents[2]
                else:
                    title = a.contents[0]
                current_infos.append(title)
            else:
                continue
            # 発行日 / 2023-9-1
            span = article.find('span')
            if span is not None:
                date = span.contents[0]
                current_infos.append(date)
            else:
                continue
            # サイト / Publicky
            current_infos.append('Publicky')
            
            infos.append(current_infos)
        return infos

    def get_text(url):
        text = ''
        soup = get_soup(url)
        div_contents = soup.find('div', class_='entrybody clearfix')
        for p_content in [p.get_text() for p in div_contents.find_all('p')]:
            text += p_content
        for a_content in [a.get_text() for a in div_contents.find_all('a')]:
            text += a_content
        return text
# endregion

# region 汎用的なメソッド
def get_soup(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    return soup
# endregion
    
# region newspaper3kを用いたスクレイピング
    # サイト上のすべてのhtmlデータを取得
    def get_all_articles_newspaper3k(self, url):
        website = newspaper.build(url, memorize_articles=False)
        return website
    # 5個のhtmlデータを取得
    def get_5_articles_newspaper3k(self, url):
        articles_5 = []
        website = self.get_all_articles_newspaper3k(url)
        website_count = len(website.articles)
        if website_count > 0:
            for i in range(5):
                article = website.articles[i]
                article.download()
                article.parse()
                articles_5.append(article)
                time.sleep(2)
        return articles_5
    # 記事のURLから記事を抽出
    def setup_newspaper3k(self, url):
        # urlからarticle作成と分析
        article = Article(url)
        article.download()
        article.parse()
        # 自然言語処理
        nltk.download('punkt')
        article.nlp()
        return article
    # 以下、記事の各要素のみを返す
    def get_info_newspaper3k(self, url):
        article = self.setup_newspaper3k(url)
        return [article.url, article.title, article.text, article.publish_date]
    def get_title_newspaper3k(self, url):
        article = self.setup_newspaper3k(url)
        return  article.title
    def get_url_newspaper3k(self, url):
        article = self.setup_newspaper3k(url)
        return article.url
    def get_publish_date_newspaper3k(self, url):
        article = self.setup_newspaper3k(url)
        return article.publish_date
    def get_authors_newspaper3k(self, url):
        article = self.setup_newspaper3k(url)
        return article.authors
    def get_text_newspaper3k(self, url):
        article = self.setup_newspaper3k(url)
        return article.text
    def get_meta_data_newspaper3k(self, url):
        article = self.setup_newspaper3k(url)
        return article.meta_data
    def get_keywords_newspaper3k(self, url):
        article = self.setup_newspaper3k(url)
        return article.keywords
    def get_summary_newspaper3k(self, url):
        article = self.setup_newspaper3k(url)
        return article.summary
# endregion
        