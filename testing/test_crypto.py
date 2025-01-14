
# pip install pytest
# module filename must begin with test_XXX
# RUN: pytest

from crypto import remove_duplicates, decode_playfair_digrams

def test_remove_duplicates():
    assert remove_duplicates('Mississippi') == 'Misp'
    assert remove_duplicates('Top Secret', True) == 'Top Secr'
    assert remove_duplicates('Top Secret', False) == 'Top Secrt'
    assert remove_duplicates('ZZyxx 90210') == 'Zzyx 9021'

def test_decode_playfair_digrams():
    assert decode_playfair_digrams('bob') == 'bob'
    assert decode_playfair_digrams('MisQsisQsipQpi') == 'Mississippi'
    assert decode_playfair_digrams('Misqsisqsipqpi', True) == 'Mississippi'
    assert decode_playfair_digrams('Misqsisqsipqpi', False) == 'Misqsisqsipqpi'
    assert decode_playfair_digrams('Queen') == 'Queen'
    assert decode_playfair_digrams('enqueue', True, 'q') == 'enqueue'
    assert decode_playfair_digrams('abcq') == 'abcq'
    assert decode_playfair_digrams('ZXz', True, 'x') == 'Zz'
    assert decode_playfair_digrams('yXY', False, 'x') == 'yXY'

