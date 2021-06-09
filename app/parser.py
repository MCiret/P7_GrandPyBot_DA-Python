from typing import List
import spacy


class Parser:
    """
    A Parser is a tokenized string using spaCy module and stored in text_tokens attribute.
    It is used to extract key words from the user question which are stored in interesting_tokens.

    Static methods are used for interesting tokens selection or strings formatting.
    """

    NLP = spacy.load('fr_core_news_md')
    WANTED_ENT_TYPE = ('LOC', 'GPE', 'FAC')
    NOT_WANTED_NOUN = ('bonjour', 'hello', 'aurevoir', 'au revoir', 'gpy', 'grandpy', 'salut')

    def __init__(self, text: str):
        self.text_tokens = Parser.NLP(Parser.capitalize_text(text))

    def extract_interesting_tokens(self):
        self.interesting_tokens = []
        for tok in self.text_tokens:
            if Parser.is_token_place_entity(tok) and not Parser.is_stop_word(tok)\
               and tok.text.lower() not in Parser.NOT_WANTED_NOUN:
                self.interesting_tokens.append(tok.text)

    @staticmethod
    def is_token_place_entity(token) -> bool:
        if token.ent_type_ in Parser.WANTED_ENT_TYPE:
            return True
        else:
            return False

    @staticmethod
    def is_stop_word(token) -> bool:
        if token.is_stop:
            return True
        else:
            return False

    @staticmethod
    def word_reverse_case_first_char(word: str) -> str:
        res_w = ""
        if word[0].islower():
            res_w = word.capitalize()
        else:
            res_w += word[0].lower()
            res_w += word[1:]
        return res_w

    @staticmethod
    def capitalize_text(text: str) -> str:
        words = text.split()
        for i, w in enumerate(words):
            words[i] = w.capitalize()
        return " ".join(words)

    @staticmethod
    def capitalize_words_list(words: List[str]) -> List[str]:
        capitalized_words = []
        for w in words:
            capitalized_words.append(w.capitalize())
        return capitalized_words

    @staticmethod
    def decapitalize_words_list(words: List[str]) -> List[str]:
        decapitalized_words = []
        for w in words:
            decapitalized_words.append(w.lower())
        return decapitalized_words

    @staticmethod
    def underscored_joined_words(text: str) -> str:
        return "_".join(text.split())
