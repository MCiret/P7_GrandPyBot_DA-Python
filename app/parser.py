from typing import List
import spacy


class Parser:

    NLP = spacy.load('fr_core_news_md')
    WANTED_POS_TAGS = ('PROPN', 'NOUN', 'ADJ')
    NOT_WANTED_NOUN = ('bonjour', 'hello', 'aurevoir', 'au revoir', 'gpy', 'grandpy', 'salut')

    def __init__(self, text: str):
        self.text_all_original_tokens = Parser.NLP(text)
        self.text_all_reversed_case_tokens = Parser.NLP(Parser.text_reverse_case_first_char(text))

    def extract_interesting_tokens(self):
        self.interesting_tokens = []
        for inv_case_tok in self.text_all_reversed_case_tokens:
            if Parser.is_token_nouns_or_adj(inv_case_tok) and not Parser.is_stop_word(inv_case_tok)\
               and inv_case_tok.text not in Parser.NOT_WANTED_NOUN:
                for orig_tok in self.text_all_original_tokens:
                    if Parser.word_reverse_case_first_char(inv_case_tok.text) == orig_tok.text\
                       and Parser.is_token_nouns_or_adj(orig_tok) and not Parser.is_stop_word(orig_tok)\
                       and orig_tok.text not in Parser.NOT_WANTED_NOUN:
                        self.interesting_tokens.append(Parser.normalize_token(inv_case_tok))

    @staticmethod
    def normalize_token(token) -> str:
        return token.lemma_

    @staticmethod
    def is_token_nouns_or_adj(token):
        if token.pos_ in Parser.WANTED_POS_TAGS:
            return True
        else:
            return False

    @staticmethod
    def is_stop_word(token):
        if token.is_stop:
            return True
        else:
            return False

    @staticmethod
    def word_reverse_case_first_char(word: str):
        res_w = ""
        if word[0].islower():
            res_w = word.capitalize()
        else:
            res_w += word[0].lower()
            res_w += word[1:]
        return res_w

    @staticmethod
    def text_reverse_case_first_char(text: str):
        words = text.split()
        for i, w in enumerate(words):
            words[i] = Parser.word_reverse_case_first_char(w)
        return " ".join(words)

    @staticmethod
    def capitalize_all_words(words: List[str]):
        capitalized_words = []
        for w in words:
            capitalized_words.append(w.capitalize())
        return capitalized_words

    @staticmethod
    def decapitalize_all_words(words: List[str]):
        decapitalized_words = []
        for w in words:
            decapitalized_words.append(w.lower())
        return decapitalized_words
