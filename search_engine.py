import re

from reader import ReadFile
from configuration import ConfigClass
from parser_module import Parse
from indexer import Indexer
from searcher import Searcher
import utils


def run_engine():
    """

    :return:
    """
    number_of_documents = 0

    config = ConfigClass()
    r = ReadFile(corpus_path=config.get__corpusPath())
    p = Parse()
    indexer = Indexer(config)

    documents_list = r.read_file(file_name='C:\\Gal\\University\\Third_year\\semA\\IR\\Data\\Data\\date=07-09-2020\\covid19_07-09.snappy.parquet')
    # Iterate over every document in the file
    for idx, document in enumerate(documents_list):
        # parse the document
        parsed_document = p.parse_doc(document)
        number_of_documents += 1
        # index the document data
        indexer.add_new_doc(parsed_document)
    print('Finished parsing and indexing. Starting to export files')

    utils.save_obj(indexer.inverted_idx, "inverted_idx")
    utils.save_obj(indexer.postingDict, "posting")


def load_index():
    print('Load inverted index')
    inverted_index = utils.load_obj("inverted_idx")
    return inverted_index


def search_and_rank_query(query, inverted_index, k):
    p = Parse()
    query_as_list = p.parse_sentence(query)
    searcher = Searcher(inverted_index)
    relevant_docs = searcher.relevant_docs_from_posting(query_as_list)
    ranked_docs = searcher.ranker.rank_relevant_doc(relevant_docs)
    return searcher.ranker.retrieve_top_k(ranked_docs, k)


def main():
    run_engine()

    # example url
    test = 'https://www.instagram.com/p/CD7fAPWs3WM/?igshid=o9kf0ugp1l8x'
    all_tokens_list = ["drrrf", "wrwr"]
    url = re.split('[/://?=]', test)
    if ('www' in url[3]):
        split_address = url[3].split('.', 1)
        url[3] = split_address[1]
        url.insert(3, split_address[0])
    print(url)
    all_tokens_list += url
    print(all_tokens_list)


    query = input("Please enter a query: ")
    k = int(input("Please enter number of docs to retrieve: "))
    inverted_index = load_index()
    for doc_tuple in search_and_rank_query(query, inverted_index, k):
        print('tweet id: {}, score (unique common words with query): {}'.format(doc_tuple[0], doc_tuple[1]))
