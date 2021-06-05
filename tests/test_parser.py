from app.parser import Parser


class TestParser:

    PARSER = Parser("le La Du de est sont Taj mahal")

    class MockToken:
        def __init__(self, lemma=None, pos=None, stop_word=None):
            self.lemma_ = lemma
            self.pos_ = pos
            self.is_stop = stop_word

    @staticmethod
    def test_normalize_token():
        assert Parser.normalize_token(TestParser.MockToken(lemma='être')) == 'être'

    @staticmethod
    def test_is_token_nouns_or_adj():
        assert Parser.is_token_nouns_or_adj(TestParser.MockToken(pos='NOUN')) is True

    @staticmethod
    def test_is_stop_word():
        assert Parser.is_stop_word(TestParser.MockToken(stop_word='aussi')) is True

    def test_extract_interesting_tokens(self):
        def mock_normalize(token):
            return 'str'

        def mock_is_noun_or_adj(token):
            return True

        def mock_is_stop_word(token):
            return False

        bkup_normalize = Parser.normalize_token
        Parser.normalize_token = mock_normalize
        bkup_is_noun_or_adj = Parser.is_token_nouns_or_adj
        Parser.is_token_nouns_or_adj = mock_is_noun_or_adj
        bkup_is_stop_word = Parser.is_stop_word
        Parser.is_stop_word = mock_is_stop_word

        self.PARSER.extract_interesting_tokens()
        assert self.PARSER.interesting_tokens == ['str', 'str', 'str', 'str', 'str', 'str', 'str', 'str']

        Parser.normalize_token = bkup_normalize
        Parser.is_token_nouns_or_adj = bkup_is_noun_or_adj
        Parser.is_stop_word = bkup_is_stop_word

    @staticmethod
    def test_word_reverse_case_first_char():
        assert Parser.word_reverse_case_first_char('Un') == 'un'
        assert Parser.word_reverse_case_first_char('deux') == 'Deux'

    @staticmethod
    def test_text_reverse_case_first_char():
        def mock_word_inverse_case(word: str):
            return ("inversed_case_word")

        bkup_word_inverse_case = Parser.word_reverse_case_first_char
        Parser.word_reverse_case_first_char = mock_word_inverse_case

        assert Parser.text_reverse_case_first_char("Bonjour comment allez vous")\
               == "inversed_case_word inversed_case_word inversed_case_word inversed_case_word"

        Parser.word_reverse_case_first_char = bkup_word_inverse_case

    @staticmethod
    def test_capitalize_all_words():
        assert Parser.capitalize_all_words(['un', 'Deux', 'trois', 'Quatre', 'Cinq'])\
               == ['Un', 'Deux', 'Trois', 'Quatre', 'Cinq']

    @staticmethod
    def test_decapitalize_all_words():
        assert Parser.decapitalize_all_words(['un', 'Deux', 'trois', 'Quatre', 'Cinq'])\
               == ['un', 'deux', 'trois', 'quatre', 'cinq']
