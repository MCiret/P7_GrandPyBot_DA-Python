from app.parser import Parser


class TestParser:

    PARSER = Parser("Bonjour où est le taj mahal ?")

    class MockToken:
        def __init__(self, ent_type=None, stop_word_bool=None):
            self.ent_type_ = ent_type
            self.is_stop = stop_word_bool

    @staticmethod
    def test_is_token_place_entity():
        assert Parser.is_token_place_entity(TestParser.MockToken(ent_type='LOC')) is True
        assert Parser.is_token_place_entity(TestParser.MockToken(ent_type='GPE')) is True
        assert Parser.is_token_place_entity(TestParser.MockToken(ent_type='DATE')) is False

    @staticmethod
    def test_is_stop_word():
        assert Parser.is_stop_word(TestParser.MockToken(stop_word_bool=True)) is True
        assert Parser.is_stop_word(TestParser.MockToken(stop_word_bool=False)) is False

    def test_extract_interesting_tokens(self):

        def mock_is_place_entity(token):
            return True

        def mock_is_stop_word(token):
            return False

        bkup_is_place_entity = Parser.is_token_place_entity
        Parser.is_token_place_entity = mock_is_place_entity
        bkup_is_stop_word = Parser.is_stop_word
        Parser.is_stop_word = mock_is_stop_word

        self.PARSER.extract_interesting_tokens()
        assert self.PARSER.interesting_tokens == ['Où', 'Est', 'Le', 'Taj', 'Mahal', '?']

        Parser.is_token_place_entity = bkup_is_place_entity
        Parser.is_stop_word = bkup_is_stop_word

    @staticmethod
    def test_word_reverse_case_first_char():
        assert Parser.word_reverse_case_first_char('Un') == 'un'
        assert Parser.word_reverse_case_first_char('deux') == 'Deux'

    @staticmethod
    def test_capitalize_text():
        assert Parser.capitalize_text("Ou est Albi en france ?") == "Ou Est Albi En France ?"
        assert Parser.capitalize_text("l'adresse d'Openclassrooms") == "Adresse Openclassrooms"

    @staticmethod
    def test_capitalize_words_list():
        assert Parser.capitalize_words_list(['un', 'Deux', 'trois', 'Quatre', 'Cinq'])\
               == ['Un', 'Deux', 'Trois', 'Quatre', 'Cinq']

    @staticmethod
    def test_decapitalize_words_list():
        assert Parser.decapitalize_words_list(['un', 'Deux', 'trois', 'Quatre', 'Cinq'])\
               == ['un', 'deux', 'trois', 'quatre', 'cinq']

    @staticmethod
    def test_underscored_joined_words():
        assert Parser.underscored_joined_words("Un mot a joindre") == "Un_mot_a_joindre"
