import preprocessing
import collections


class PostingDocEntry:
    def __init__(self, doc_id):
        self.id = doc_id
        self.count = 1

    def term_hit(self):
        self.count += 1


class Posting:
    def __init__(self, term: str, documents: list[PostingDocEntry]):
        self.term = term
        self.documents = documents
        self.count = len(documents)

    def append_doc(self, doc_id):
        docs: list[PostingDocEntry] = list(filter(lambda d: d.id == doc_id, self.documents))
        if len(docs) > 0:
            docs[0].term_hit()
        else:
            self.documents.append(PostingDocEntry(doc_id))
            self.count = self.count + 1
        self.documents.sort(key=lambda d: d.id)


class Indexer:

    def __init__(self, doc_to_terms: list[preprocessing.DocToTerms]):
        self.docToTerms = doc_to_terms

    # Creates a lexicographic sorted inverted index
    def inverter_index(self):
        print('building inverted index')
        inverted_index: dict[str, Posting] = dict()
        for doc_terms in self.docToTerms:
            for term in doc_terms.terms:
                if term in inverted_index:
                    inverted_index[term].append_doc(doc_terms.id)
                else:
                    inverted_index[term] = Posting(term, [PostingDocEntry(doc_terms.id)])

        sorted_inverted_index = collections.OrderedDict()
        sorted_terms = sorted(inverted_index.keys())
        for s_term in sorted_terms:
            sorted_inverted_index[s_term] = inverted_index[s_term]
        return sorted_inverted_index

    def doc_id_to_doc_name_index(self):
        doc_id_name_index: dict[int, str] = dict()
        for doc_terms in self.docToTerms:
            doc_id_name_index[doc_terms.id] = doc_terms.name
        return doc_id_name_index
