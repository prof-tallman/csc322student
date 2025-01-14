
# Prof Tallman
# This is a simple encryption module that needs to be tested.
# Based on excerpts from personal solution to Playfair Cipher for CSC-314 course
# Project idea from Python Programming in Context by Miller, Ranum, and Anderson

def remove_duplicates(text:str, ignore_case:bool=False):
    """ Removes duplicates so that only the unique characters remain, in their original order. """
    text_unique = ''
    for ch in text:
        if ignore_case:
            if ch.lower() not in text_unique.lower():
                text_unique += ch
        else:
            if ch not in text_unique:
                text_unique += ch
    return text_unique


def decode_playfair_digrams(text:str, ignore_case:bool=True, sub:str='Q'):
    """ Removes Q-substitutions from a text according to Playfair digram rules. """
    idx = 1
    last = len(text) - 1
    output = text[0]
    text_lc = text.lower()
    sub_lc = sub.lower()
    while idx < last:
        if ignore_case:
            if text_lc[idx] == sub_lc and text_lc[idx-1] == text_lc[idx+1]:
                idx += 1
            else:
                output += text[idx]
                idx += 1
        else:
            if text[idx] == sub and text[idx-1] == text[idx+1]:
                idx += 1
            else:
                output += text[idx]
                idx += 1
    output += text[-1]
    return output


def main():
    """ Demonstrates how to use this module. """
    print("Removing Duplicates from string 'mississippi': ", end='')
    print(remove_duplicates('mississippi'))
    print("Decoding Playfair Digrams from string 'misQsisQsipQpi': ", end='')    
    print(decode_playfair_digrams('misQsisQsipQpi'))


if __name__ == '__main__':
    main()
