import sys

import preprocessing
import indexer
import ranker
import util

INVERTED_INDEX_FILE_NAME = 'inverted_index'
DOC_ID_NAME_INDEX_NAME = 'doc_id_name_index'
TFIDF_NAME_INDEX_NAME = 'tfidf'


def build_index():
    if len(sys.argv) < 1:
        raise Exception('Clinical trails Data file directory path should be supplied to build the index')

    corpus_path = sys.argv[1]
    preprocessor = preprocessing.Preprocessor(corpus_path)
    doc_to_terms: list[preprocessing.DocToTerms] = preprocessor.parse()

    indexer_ob = indexer.Indexer(doc_to_terms)
    inverted_index: dict[str, indexer.Posting] = indexer_ob.inverter_index()
    doc_id_name_index: dict[int, str] = indexer_ob.doc_id_to_doc_name_index()

    tf_idf_ranker = ranker.Ranker(inverted_index, doc_id_name_index)
    _tfidf = tf_idf_ranker.tfidf()

    print('Indexing completed..saving...')
    util.save_obj(doc_id_name_index, DOC_ID_NAME_INDEX_NAME)
    util.save_obj(inverted_index, INVERTED_INDEX_FILE_NAME)
    util.save_pandas_df_as_pickle(_tfidf, TFIDF_NAME_INDEX_NAME)
    print('Saved index for quick results for future queries')


def load_index():
    if not util.is_saved(INVERTED_INDEX_FILE_NAME) and not util.is_saved(DOC_ID_NAME_INDEX_NAME) and not util.is_saved(TFIDF_NAME_INDEX_NAME):
        build_index()
    else:
        print('Found cached indexes! Using them ;)')
    _inverted_index: dict[str, indexer.Posting] = util.load_obj(INVERTED_INDEX_FILE_NAME)
    _doc_id_name_index: dict[int, str] = util.load_obj(DOC_ID_NAME_INDEX_NAME)
    _tfidf = util.load_pickle_as_pandas_df(TFIDF_NAME_INDEX_NAME)
    return {
        'tfidf': _tfidf,
        'inverted': _inverted_index,
        'did_name': _doc_id_name_index
    }


print('Loading...')
index = load_index()
print('Ready...(type exit to terminate)')

while True:
    query = input('what is the query?')
    # query = 'patient ARDS'

    if query == 'exit':
        break

    print('...')
    normalize_query: list[str] = preprocessing.query(query)
    tf_idf_ranker_q = ranker.Ranker(index['inverted'], index['did_name'])
    _tfidf_query = tf_idf_ranker_q.tfidf_query(normalize_query)

    document_results: [int, float] = ranker.top_10_relevant_documents(index['tfidf'], _tfidf_query)
    document_results = [{'document_name': index['did_name'][d_id[0]], 'similarity_score': d_id[1]} for d_id in document_results]
    print('Matching documents for the query - ', query)
    util.print_result(document_results)
