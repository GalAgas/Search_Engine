import re
from urllib.parse import urlparse

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from document import Document


class Parse:

    def __init__(self):
        self.stop_words = stopwords.words('english')

    #need to change connecting lists with +=
    def parse_hashtag(self, all_tokens_list , token):
        final = []
        final.append(token)
        tok = token[1:]

        if '_' in token:
            final += tok.split('_')

        else:
            #final += re.findall('[A-Z][^A-Z]*', tok)
            final += re.findall(r'[a-zA-Z0-9](?:[a-z0-9]+|[A-Z0-9]*(?=[A-Z]|$))', tok)

        #final = map(lambda x: x.lower(), final)
        final = [x.lower() for x in final]
        all_tokens_list += final



    def parse_url(self, all_tokens_list, token):
        #all_tokens_list += re.split('://, /, /?, =', token)
        #all_tokens_list += token.split(['://', '/', '/?', '='])

        # url = re.split('[/://?=]', token)
        # if ('www' in url[3]):
        #     split_address = url[3].split('.', 1)
        #     url[3] = split_address[1]
        #     url.insert(3, split_address[0])
        # all_tokens_list += url
        pass


    def parse_sentence(self, text):
        """
        This function tokenize, remove stop words and apply lower case for every word within the text
        :param text:
        :return:
        """
        #text_tokens = word_tokenize(text)
        #text_tokens_without_stopwords = [w.lower() for w in text_tokens if w not in self.stop_words]


        tokenized_text = [];

        #text_tokens = text.split(' ');
        text_tokens = re.split(' |\n\n|\n', text)
        #need to remove whitespace
        #text_tokens = re.split('[' '][\n\nn]', text)


        for token in text_tokens:
            if token.startswith('#'):
                self.parse_hashtag(tokenized_text, token)
            elif token.startswith('@'):
                tokenized_text.append(token)
            #starts with http & https
            elif token.startswith('http'):
                self.parse_url(tokenized_text, token)



        return tokenized_text

        #return text_tokens_without_stopwords

    def parse_doc(self, doc_as_list):
        """
        This function takes a tweet document as list and break it into different fields
        :param doc_as_list: list re-preseting the tweet.
        :return: Document object with corresponding fields.
        """
        tweet_id = doc_as_list[0]
        tweet_date = doc_as_list[1]
        full_text = doc_as_list[2]
        url = doc_as_list[3]
        retweet_text = doc_as_list[4]
        retweet_url = doc_as_list[5]
        quote_text = doc_as_list[6]
        quote_url = doc_as_list[7]
        term_dict = {}
        tokenized_text = self.parse_sentence(full_text)

        doc_length = len(tokenized_text)  # after text operations.

        for term in tokenized_text:
            if term not in term_dict.keys():
                term_dict[term] = 1
            else:
                term_dict[term] += 1

        document = Document(tweet_id, tweet_date, full_text, url, retweet_text, retweet_url, quote_text,
                            quote_url, term_dict, doc_length)
        return document


