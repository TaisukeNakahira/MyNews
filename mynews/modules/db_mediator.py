import time
from main.models import Articles, Favorites
from datetime import datetime
from modules.scraper import Scraper_GIGAZINE
from modules.scraper import Scraper_Publicky

# DBのすべてのデータを取得
def get_all_datas():
    datas = Articles.objects.all()
    return datas

# ArticlesDBに新しいデータを追加
def register_new_datas(infos):
    for info in infos:
        if not is_article_existed(info):
            if isinstance(info[1], str):
                Articles.objects.create(url=info[0], title=info[1], publish_date=convert_datetime(info[2]), site=info[3])

# タイトルが特定の文字列を含むデータを取得
def get_data_contains_string(strValue):
    if not isinstance(strValue, str):
        return []
    datas = Articles.objects.filter(title__contains=strValue)
    return datas

# 日にちの形式を整える
def convert_datetime(str):
    dt = datetime.strptime(str, '%Y-%m-%d')
    return dt

# Articlesに記事がすでに登録されているかどうか
def is_article_existed(info):
    try:
        article = Articles.objects.filter(url=info[0], title=info[1], publish_date=convert_datetime(info[2]), site=info[3])
        if article:
            return True
        else: 
            return False
    except Exception as e:
        return False

# LIKEされているすべてのデータを取得
def register_liked_data():
    # LIKEされているデータを登録
    infos = Articles.objects.filter(like=True)
    if infos:
        register_new_datas_favorites(infos)
    # LIKEが外れているデータを削除する
    delete_unliked_data()

# FavoritesDBに新しいデータを追加
def register_new_datas_favorites(infos):
    for info in infos:
        # タイトルが同じデータ = すでにあるデータは省く
        article = Favorites.objects.filter(article__title=info.title)
        if len(article) == 0:
            if info.site == 'GIGAZINE':
                time.sleep(2)
                txt = Scraper_GIGAZINE.get_text(info.url)
            elif info.site == 'Publicky':
                time.sleep(2)
                txt = Scraper_Publicky.get_text(info.url)
            else:
                txt = ''
            Favorites.objects.create(article=info, text=txt)

# FavoritesDBで、LIKEが外れているものを削除する
def delete_unliked_data():
    Favorites.objects.filter(article__like=False).delete()

def get_all_favorites():
    datas = Favorites.objects.all()
    return datas
