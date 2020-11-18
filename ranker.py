import indexer
import pandas as pd
import math
import util


def logarithmic(x):
    if x > 0:
        return 1 + math.log10(x)
    return 0


def top_10_relevant_documents(tfidf, tfidf_query):
    dot_product = tfidf.multiply(tfidf_query['query'], axis="index")
    dot_product_sum = dict(dot_product.sum().sort_values(ascending=False))
    ranked_doc_ids = list(dot_product_sum.items())
    return ranked_doc_ids[:10]


class Ranker:
    def __init__(self, inverted_index: dict[str, indexer.Posting], doc_id_name_index: dict[int, str]):
        self.index = inverted_index
        self.vocabulary = list(inverted_index.keys())
        self.documents = list(doc_id_name_index.keys())
        self.N = len(self.documents)

    def tf(self):
        data_frame = pd.DataFrame()
        for doc in self.documents:
            dtf = [0] * len(self.vocabulary)
            for idx, term in enumerate(self.vocabulary):
                f_doc = list(filter(lambda d: d.id == doc, self.index[term].documents))
                if len(f_doc) > 0:
                    dtf[idx] = logarithmic(f_doc[0].count)
            data_frame.insert(0, doc, dtf, False)
        print('Computed tf dataframe shape: ', data_frame.shape)
        return data_frame

    def idf(self):
        data_frame = pd.DataFrame()
        for doc in self.documents:
            dtf = [0] * len(self.vocabulary)
            for idx, term in enumerate(self.vocabulary):
                dtf[idx] = math.log10(self.N / self.index[term].count)
            data_frame.insert(0, doc, dtf, False)
        print('Computed idf dataframe shape: ', data_frame.shape)
        return data_frame

    def tfidf(self):
        return self.tf() * self.idf()

    def tf_query(self, query: list[str]):
        qtf = [0] * len(self.vocabulary)
        for query_term in query:
            try:
                index_in_vocabulary = self.vocabulary.index(query_term)
                qtf[index_in_vocabulary] += 1
            except ValueError:
                # Fails if the query term is not present in the vocabulary
                pass
        return pd.DataFrame({'query': qtf})

    def idf_query(self, query):
        qtf = [0] * len(self.vocabulary)
        for query_term in query:
            try:
                index_in_vocabulary = self.vocabulary.index(query_term)
                qtf[index_in_vocabulary] = math.log10(self.N / self.index[query_term].count)
            except ValueError:
                # Fails if the query term is not present in the vocabulary
                pass
        return pd.DataFrame({'query': qtf})

    def tfidf_query(self, query: list[str]):
        return self.tf_query(query) * self.idf_query(query)
