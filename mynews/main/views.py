import json
from django.shortcuts import render
from modules.scraper import Scraper_GIGAZINE
from modules.scraper import Scraper_Publicky
import modules.db_mediator as db_mediator
import modules.vector_model as vector_model
import MeCab

# 拡張辞書mecab-ipadic-neologdを-dで指定
# 'mecabrc -d /usr/lib/mecab/dic/mecab-ipadic-neologd'
mecab = MeCab.Tagger()
# wikiで形態素解析しようとしている
# wv = KeyedVectors.load_word2vec_format('./wiki.vec.pt', binary=True)
# ディレクトリパス
dir_path = '../data/'

# ディレクトリパス
dir_path = '../data/'

def admin(request):
    return render(request, 'main/')
    
def index(request):
    return render(request, 'main/index.html', {})

# //////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////
# 新しい記事取得
# //////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////
def get_articles(request):
    # すべてのサイトの記事を集約
    infos = []
    infos.extend(gigazine_beautifulSoup())
    infos.extend(publicky_beautifulSoup())
    # 今回抽出したデータをDBに登録
    db_mediator.register_new_datas(infos)
    # LIKEされているデータだけをDBに登録
    db_mediator.register_liked_data()
    # DBから、今回抽出したデータだけを取得
    this_infos = []
    for info in infos:
        this_infos.extend(list(db_mediator.get_data_contains_string(info[1])))
    return render(request, 'main/articles.html', {'infos': this_infos})
    
def gigazine_beautifulSoup():
    url = r'https://gigazine.net/'
    scraper = Scraper_GIGAZINE()
    infos = scraper.get_infos(url)
    return infos

def publicky_beautifulSoup():
    url = r'https://www.publickey1.jp/'
    scraper = Scraper_Publicky()
    infos = scraper.get_infos(url)
    return infos

# //////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////
# 全記事取得
# //////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////
def get_articles_all(request):
    infos = db_mediator.get_all_datas()
    db_mediator.register_liked_data()
    return render(request, 'main/articles_all.html', {'infos': infos})

# trainデータの作成
# def create_trained_data():
#     liked_datas = db_mediator.get_all_favorites()
#     csv_med.write(dir_path + 'contents.csv', liked_datas)

# 分析
# def analyze(request):
#     sim_calc.test()
#     texts = ['私は機械学習が大好きです', '飛行機の音ではなかった。耳の後ろ側を飛んでいた虫の羽音だった。']
#     result = sim_calc.analyze_test(texts)
#     return render(request, 'main/analysis.html', {'result': result})

# //////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////
# モデルのテスト
# //////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////
def create_model_test(request):
    # if request.method == "POST":
    #     if "create_model" in request.POST:
    #         vector_model.create()
    db_mediator.register_liked_data()
    res = vector_model.create()
    return render(request, 'main/model.html', {'model': res})

# //////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////
# favモデルからモデルを作成（favモデルの単語ファイルも作成）
# //////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////
def create_model(request):
    db_mediator.register_liked_data()
    vector_model.create()
    return render(request, 'main/index.html')

# //////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////
# おすすめ
# //////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////
def recommendation(request):
    # 1. favモデルの単語をすべて取得
    fav_words = vector_model.get_fav_words()
    # 2. データベースからすべての記事を取得
    articles = db_mediator.get_all_datas()
    dict_similarity = {}
    num = 1
    for article in articles:
    # for article in articles[:5]:
        # 3. 記事ごとに単語の類似の平均を取得
        # ///////////////////////////////
        # ///////////////////////////////
        # ///////////////////////////////
        # if (article.title == "「影」が光速を超えることはあるのか？"): 
        # if (article.title == "OpenAIの元研究者がセキュリティ上の懸念を取締役会に訴えたため解雇されたことを明らかに"): 
        #     article.title == "「世界最大の発光器官」を持つ珍しい深海イカに襲われるド迫力ムービーが公開される" or 
        #     article.title == "Amazonプライムビデオで映画「十二人の怒れる男」のサムネイルがAI生成画像になっていて「19人いる」と指摘あり"):
        # ///////////////////////////////
        # ///////////////////////////////
        # ///////////////////////////////
        similarity = get_similarity_of_an_article(fav_words, article, article.title)
        # 4. 記事とその記事の類似度dictionaryとして保存
        dict_similarity[article] = similarity
        print(str(num) + '. 類似度計算完了...　' + article.title + '：' + str(similarity))
        num += 1
    
    # お気に入りの記事があったら除外
    fav_datas = db_mediator.get_all_favorites()
    fav_titles = [data.article.title for data in fav_datas]
    keys_to_remove = [obj for obj in dict_similarity if obj.title in fav_titles]
    for key in keys_to_remove:
        del dict_similarity[key]
    
    # 5. 辞書を、similarityを基準でソートし、上位10の記事を取得
    # sorted_articles = sorted(dict_similarity.items(), key=lambda x: x[1])
    top_10_articles = (sorted(dict_similarity.items(), key = lambda x : x[1], reverse=True)[:20])
    # articleだけのリストを作成
    top_10_articles_keys = [article[0] for article in top_10_articles]

    # 6. 上位10の記事を持たせて画面に表示
    return render(request, 'main/recommendation.html', {'articles': top_10_articles_keys})

# 評価対象のタイトルの全単語・favモデルの単語すべての類似度を取得し、平均を取得
def get_similarity_of_an_article(fav_words, article, title):
    words = split_title(article.title)
    sum_similarity = 0
    # similarity_dict = {}
    
    for word in words:
        for fav_word in fav_words:
            similarity = vector_model.get_similarity(word, fav_word)
            sum_similarity += similarity
            # similarity_dict['タイトルの単語：' + word + '　お気に入り単語：' + fav_word] = similarity

    # sorted_similarity_dict = dict(sorted(similarity_dict.items(), key=lambda item: item[1], reverse=True))
    # file_path = "C:/Users/nakahira/Git/mynews/data/test_openAI.txt"
    # with open(file_path, 'w') as f:
    #     f.writelines("\n".join(str(k)+","+str(v) for k,v in sorted_similarity_dict.items()))

    average_similarity = 0
    if len(words) > 0:
        len_sum = len(words) * len(fav_words)
        average_similarity = sum_similarity / len_sum
    return average_similarity

# タイトルを単語に分割
def split_title(title):
    node = mecab.parseToNode(title)
    words = []
    while node:
        # 単語
        word = node.surface
        # 品詞
        pos = node.feature.split(',')[0]
        # 名詞だけ抽出
        if pos == '名詞':
            words.append(word)
        # 次のnode
        node = node.next
    return words

# //////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////
# 形態素解析
# //////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////
# 形態素解析の結果をcsvファイルに出力
path_morphological_analysis = "C:/Users/nakahira/Git/mynews/data/morphological_analysis2.csv"
def morphological_analysis(request):
    if request.method == 'POST':
        url = request.POST.get('input_text')
        text = Scraper_GIGAZINE.get_text(url)
        f = open(path_morphological_analysis, 'a')
        # f.write(text)
        f.write(mecab.parse(text))
        f.close()
    
    return render(request, 'main/index.html')