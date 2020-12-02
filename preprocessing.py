import hashlib
import re
import xml.etree.ElementTree as ET
from os import listdir
from os.path import isfile, join, isdir
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
nltk.download('stopwords')
nltk.download('wordnet')
# case insensitive stop words removal
def no_stopwords(tokens: list[str]):
    stop_words = set([s.upper() for s in stopwords.words('english')])
    return [w for w in tokens if not w.upper() in stop_words]


def lowercase(tokens: list[str]):
    return [w.lower() for w in tokens]


# used to convert plural to singular
def lemmatize(tokens: list[str]):
    wnl = WordNetLemmatizer()
    return [wnl.lemmatize(w) for w in tokens]


def intervention_type_other(tokens):
    if tokens[0] == "Other":
        return ["InterventionOther"]
    return tokens


# converts standard strings to processable string without special character, stop words
def normalize(text):
    # Phase values normalization is performed according to clinical trails standard for phase nomenclature
    text = re.sub(r'Early Phase 1', 'EarlyPhase1', text)
    text = re.sub(r'Phase 1/Phase 2', 'Phase1Phase2', text)
    text = re.sub(r'Phase 2/Phase 3', 'Phase2Phase3', text)
    text = re.sub(r'Phase\s*1', 'Phase1', text, flags=re.IGNORECASE)
    text = re.sub(r'Phase\s*2', 'Phase2', text, flags=re.IGNORECASE)
    text = re.sub(r'Phase\s*3', 'Phase3', text, flags=re.IGNORECASE)
    text = re.sub(r'Phase\s*4', 'Phase4', text, flags=re.IGNORECASE)

    text = re.sub(r'Combination Product', 'CombinationProduct', text)
    text = re.sub(r'Diagnostic Test', 'DiagnosticTest', text)
    text = re.sub(r'Dietary Supplement', 'DietarySupplement', text)
    text = re.sub(r'Intervention Other', 'InterventionOther', text, flags=re.IGNORECASE)

    text = re.sub(r'covid-19', 'covid19', text, flags=re.IGNORECASE)
    text = re.sub(r'covid19', 'covid19', text, flags=re.IGNORECASE)
    return text


def tokenize(text, funcs=()):
    text = normalize(text)
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    result: list[str] = tokenizer.tokenize(text)
    for func in funcs:
        result = func(result)
    return result


class XMLBlockProcessor:
    def __init__(self, xml_path, processing_unit_funcs=()):
        self.xml_path = xml_path
        self.funcs = processing_unit_funcs

    def tokens(self, text):
        return tokenize(text, self.funcs)


class DocToTerms:
    def __init__(self, doc_name, terms):
        self.id = hash(doc_name)
        self.name = doc_name
        self.terms = terms

    def hash(self):
        return hashlib.sha256(self.name.encode('utf-8')).hexdigest()


def query(query_str):
    query_str = normalize(query_str)
    return tokenize(query_str, [no_stopwords, lemmatize])


class Preprocessor:
    """
     - Paths from the xml clinical trails. the xml file is formatted according to https://clinicaltrials.gov/ct2/html/images/info/public.xsd standard
     - Any paths not present are ignored/ skipped
     - text is first normalized according clinical terms, tokenized and then different processing functions are according to the xml block type
    """
    xml_paths = [
        XMLBlockProcessor('brief_title', [no_stopwords, lemmatize]),
        XMLBlockProcessor('official_title', [no_stopwords, lemmatize]),
        XMLBlockProcessor('./brief_summary/textblock', [no_stopwords, lemmatize]),
        XMLBlockProcessor('./location_countries/country'),
        XMLBlockProcessor('./detailed_description/textblock', [no_stopwords, lemmatize]),
        XMLBlockProcessor('phase'),
        XMLBlockProcessor('./intervention/description', [no_stopwords, lemmatize]),
        XMLBlockProcessor('./intervention/intervention_type', [intervention_type_other]),
        XMLBlockProcessor('condition'),
        XMLBlockProcessor('keyword')
    ]

    def __init__(self, source):
        self.source = source

    def parse(self):
        if not isdir(self.source):
            raise Exception("Source path should be directory with data files")

        data_files = [f for f in listdir(self.source) if isfile(join(self.source, f))]
        
        all_doc_to_terms: list[DocToTerms] = []
        for doc_id, file_name in enumerate(data_files):
            all_tokens = self.get_tokens_from_doc(file_name)
            print('all token extracted from file', len(all_tokens))
            all_doc_to_terms.append(DocToTerms(file_name, all_tokens))

        return all_doc_to_terms

    def get_tokens_from_doc(self, file_name):
        xml_tree = ET.parse(join(self.source, file_name))
        all_tokens = []
        for data_block in self.xml_paths:
            for child in xml_tree.getroot().findall(data_block.xml_path):
                if child is not None:
                    print(f"""Processing file: {join(self.source, file_name)}, block: {data_block.xml_path}""")
                    #  merging results from all data blocks in to one doc corpus
                    all_tokens = all_tokens + data_block.tokens(child.text)
        return all_tokens
