import MeCab
 
# 拡張辞書mecab-ipadic-neologdを-dで指定
# 'mecabrc -d /usr/lib/mecab/dic/mecab-ipadic-neologd'
mecab = MeCab.Tagger()
# wikiで形態素解析しようとしている
# wv = KeyedVectors.load_word2vec_format('./wiki.vec.pt', binary=True)
# ディレクトリパス
dir_path = '../data/'

# testメソッド
# def test():
#     text = '飛行機の音ではなかった。耳の後ろ側を飛んでいた虫の羽音だった。'
#     result = extract_words(text)
#     f = open('test.txt', 'w', encoding='UTF-8')
#     for res in result:
#         f.write(res + '\n')
#     f.close
# 文章を単語に分ける
def extract_words(text):
    node = mecab.parseToNode(text)
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
    text_result = ' '.join(words)
    return text_result

# 訓練データから訓練ベクトル生成
# def create_train_bector():
#     # 最初に、CSVファイルを削除
#     if os.path.isfile("train.csv"):
#         os.removez("train.csv")
#     favorites = []
#     # Favoritesモデルからすべての記事を取得
#     favorite_objects = Favorites.objects.all()
#     # Favoritesモデルの本文を単語化
#     for obj in favorite_objects:
#         favorites.append(get_words_main(obj.text))
#     # 本文の単語をベクトル化してFavoritesベクトルを作成
    
#     # Articlesモデルからすべての記事を取得
#     artcle_objects = Articles.objects.all()
#     # Articlesモデルのタイトルを単語化
    
#     # タイトルの単語をベクトル化してArticlesベクトルを作成
    
    
#     # Favoritesベクトルを用いてモデルを作成
    
#     # モデルにArticlesベクトルを読ませて、結果を取得

# MeCabのテストメソッド
# def analyze_test(texts):
#     csv_mediator.write('contents.csv', texts)
#     train_words = get_words('contents.csv')
#     # trainされたデータをwords.csvに格納
#     with open('words.csv', 'w', encoding='UTF-8') as f_train_words:
#         writer = csv.writer(f_train_words, lineterminator='\n')
#         for w in train_words:
#             writer.writerow(w)
#     # words.csvからdictionaryを作る
#     words = []
#     with open('words.csv', 'r') as r_train_words:
#         reader = csv.reader(r_train_words)
#         for row in reader:
#             words.append(row)
#     create_dictionary(words)
#     # mecabの結果を返す
#     result = []
#     for text in texts:
#         this = mecab.parse(text)
#         result.append(this)
#     return result

# 以下を使用して、csvファイル内の文字列を名詞に分ける
# 1. get_words_main
# 2. tokenize
# def get_words(path):
#     word = []
#     with open(path, 'r', encoding='UTF-8') as f_contents:
#         rows = f_contents.readlines()
#         for row in rows:
#             word.append(get_words_main(row))
#     return word
# # 文字列を1行もらい、トークンにする
# def get_words_main(row):
#     return [token for token in tokenize(row)]
# # mecabを利用して文字列を名詞に分ける
# def tokenize(row):
#     node = mecab.parseToNode(row)
#     while node:
#         if node.feature.split(',')[0] == '名詞':
#             yield node.surface.lower()
#         node = node.next

# gensimを用いてdictionaryを作る
# def create_dictionary(words):
#     dictionary = corpora.Dictionary(words)
#     # dictionary.filter_extremes(no_below=0, no_above=0.1)
#     dictionary.save_as_text('dictionary.txt')
