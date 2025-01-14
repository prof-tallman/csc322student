
# RUN: python [module]

import unittest
import crypto

class CryptoTest(unittest.TestCase):
    ''' Uses PyUnit to test the crypto.py module. '''
    
    def test_remove_duplicates(self):
        self.assertEqual(crypto.remove_duplicates('Mississippi', True), 'Misp')
        self.assertEqual(crypto.remove_duplicates('Mississippi', False), 'Misp')
        self.assertEqual(crypto.remove_duplicates('Top Secret', True), 'Top Secr')
        self.assertEqual(crypto.remove_duplicates('Top Secret', False), 'Top Secrt')
        self.assertEqual(crypto.remove_duplicates('Zzyxx 90210', True), 'Zyx 9021')
        self.assertEqual(crypto.remove_duplicates('Zzyxx 90210', False), 'Zzyx 9021')

    def test_decode_playfair_digrams(self):
        self.assertEqual(crypto.decode_playfair_digrams('MisQsisQsipQpi', True, 'Q'), 'Mississippi')
        self.assertEqual(crypto.decode_playfair_digrams('MisQsisQsipQpi', False, 'Q'), 'Mississippi')
        self.assertEqual(crypto.decode_playfair_digrams('Misqsisqsipqpi', True, 'Q'), 'Mississippi')
        self.assertEqual(crypto.decode_playfair_digrams('Misqsisqsipqpi', False, 'Q'), 'Misqsisqsipqpi')
        self.assertEqual(crypto.decode_playfair_digrams('Queen', True, 'Q'), 'Queen')
        self.assertEqual(crypto.decode_playfair_digrams('Queen', False, 'Q'), 'Queen')
        self.assertEqual(crypto.decode_playfair_digrams('queen', True, 'Q'), 'queen')
        self.assertEqual(crypto.decode_playfair_digrams('queen', False, 'Q'), 'queen')
        self.assertEqual(crypto.decode_playfair_digrams('enQueue', True, 'Q'), 'enQueue')
        self.assertEqual(crypto.decode_playfair_digrams('enQueue', False, 'Q'), 'enQueue')
        self.assertEqual(crypto.decode_playfair_digrams('enqueue', True, 'Q'), 'enqueue')
        self.assertEqual(crypto.decode_playfair_digrams('enqueue', False, 'Q'), 'enqueue')
        self.assertEqual(crypto.decode_playfair_digrams('ZXYQzxyq', True, 'Q'), 'ZXYQzxyq')
        self.assertEqual(crypto.decode_playfair_digrams('BOBbob', True, 'Q'), 'BOBbob')


if __name__ == '__main__':
    unittest.main()