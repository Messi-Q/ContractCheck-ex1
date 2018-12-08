#coding:utf-8
from gensim import corpora, models, similarities

documents = ["Shipment of gold damaged in a fire","Delivery of silver arrived in a silver truck","Shipment of gold arrived in a truck"]

# 分词
texts = [[word for word in document.lower().split()] for document in documents]
print(texts)

# 抽取词袋，将token映射为id
dictionary = corpora.Dictionary(texts)
print(dictionary.token2id)

# 由文档向量以及频率构成文档向量
corpus = [dictionary.doc2bow(text) for text in texts]
print(corpus)

# 计算tfidf权重,注意在gensim的tfidf算法中到文档频率的求解过程中对数之后+1了
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
for doc in corpus_tfidf:
    print(doc)
print(tfidf.dfs)
print(tfidf.idfs)
