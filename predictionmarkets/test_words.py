from predictionmarkets.words import int_to_words, words_to_int

def test_conversion():
    for n in [0, 1, 2, 4, 2**10, 2**15, 2**20, 2**10*3**10]:
        assert words_to_int(int_to_words(n)) == n
