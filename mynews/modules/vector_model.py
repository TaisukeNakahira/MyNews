import csv
import os
from gensim.models import word2vec
import MeCab
import modules.db_mediator as db_mediator
 
# 拡張辞書mecab-ipadic-neologdを-dで指定
# 'mecabrc -d /usr/lib/mecab/dic/mecab-ipadic-neologd'
tagger = MeCab.Tagger()
tagger.parse('')

# モデルのパス
path_model = "C:/Users/nakahira/Git/mynews/data/word2vec_data_model.model"
# favモデル単語ファイルのパス
path_fav_words = "C:/Users/nakahira/Git/mynews/data/fav_words.csv"

# ベクトル生成時に、クライアントが呼ぶメソッド
def create():
    # 事前にモデルと単語ファイルを削除
    if os.path.exists(path_model):
        os.remove(path_model)
    if os.path.exists(path_fav_words):
        os.remove(path_fav_words)
    # 学習データの読み込み
    # 学習データ = Favoritesモデルのtext
    favDatas = db_mediator.get_all_favorites()
    favTexts = []
    for favData in favDatas:
        favTexts.append(favData.text)
    
    # コーパス作成
    favTextWords = []
    for text in favTexts:
        words = tokenize(text, 2, 10000, True)
        favTextWords.append(words)
    # np.savetxt("C:/Users/nakahira/Git/mynews/data/data_corpus.txt", favTextWords, fmt='%s', delimiter=',')
    
    # favモデルの単語をテキストファイルに出力
    with open(path_fav_words, 'w', encoding='UTF-8') as f:
        writer = csv.writer(f)
        writer.writerows(favTextWords)
        # for words in favTextWords:
        #     if type(words) is list:
        #         for word in words:
        #             f.write(word)
        #     else:
        #         f.write(word)
    
    # モデル作成
    # word2vec_data_model = word2vec.Word2Vec(favTextWords, sg=1, size=100, window=5, min_count=2, iter=100, workers=3)
    word2vec_data_model = word2vec.Word2Vec(favTextWords, sg=1, window=5, min_count=3, workers=3)
    
    # モデルのsave
    word2vec_data_model.save(path_model)
    
    # テスト用
    # return get_most_similar(str, "C:/Users/nakahira/Git/mynews/data/word2vec_data_model.model")zz

def tokenize(content, token_min_len, token_max_len, lower):
    return [
        str(token) for token in tokenize_ja(content, lower)
        if token_min_len <= len(token) <= token_max_len
    ]
def tokenize_ja(text, lower):
    node = tagger.parseToNode(str(text))
    while node:
        if node.feature.split(',')[0] in ["名詞"]:
            yield node.surface
        node = node.next

def get_most_similar(sample):
    model = word2vec.Word2Vec.load(path_model)
    return model.wv.most_similar(sample)

# ふたつの単語の類似度を取得
def get_similarity(word1, word2):
    model = word2vec.Word2Vec.load(path_model)
    if word1 in model.wv.key_to_index and word2 in model.wv.key_to_index:
        similarity = model.wv.similarity(word2, word1)
        return similarity
    return 0

# favモデルから単語だけを抽出
def get_fav_words():
    fav_words = []
    with open(path_fav_words, encoding='UTF-8') as f:
        reader = csv.reader(f)
        rows = [row for row in reader]
        for row in rows:
            for word in row:
                fav_words.append(word)
    return fav_words
