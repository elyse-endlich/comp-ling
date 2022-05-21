"""
MT.PY
Elyse Endlich and Simone Nikitina
April 2022

Search for "TODO" below to see places you may need to modify.

Major steps:
    -- read in a text file in a foreign language.
    -- read in a word-to-word, foreign-to-English dictionary
    -- map foreign words to English words via dictionary
    -- add part of speech (POS) tags to English words
    -- TODO: (student should add functions to rearrange/adjust/replace English words based on POS-based or other rules)
    -- output result
"""

import io
import re
import sys

from nltk import pos_tag

# constants
TAG = 1
NOTAG = 0

# pre-compiled regexes, for efficient later use

punc_strip = re.compile(r"[’\-]")  # we'll change apostrophes and hyphens to spaces in preprocessing

punc_keep = re.compile(
    r"([.,?!:;«»]+( |$)| [.,?!:;«»]+)")
# for other punctuation, so long as it doesn't have letters or numbers on BOTH sides of it,
#   we'll keep it (and separate it out with spaces on both sides after preprocessing)

"""
READ_FOREIGN: Takes file name as input, designating text file with body of foreign text to be translated. Everything is
lower-cased, apostrophes and hyphens are converted to spaces (splitting words in the process), and remaining punctuation
 such as sentence-final periods) is set off with spaces.
    Return a list of words (where any remaining punctuation are also now considered to be "words", as well).
"""


def read_foreign(foreign_text):
    f = []
    foreign_file = io.open(foreign_text, 'r', encoding="utf8")

    for line in foreign_file:
        line = line.lower()
        line = punc_strip.sub(r" ", line)
        line = punc_keep.sub(r" \1 ", line)
        f.extend(line.strip().split())

    return f


"""
READ_DICT: Takes file name as input, designating Foreign-to-English dictionary file.
Return a Python dictionary (hash table) with foreign words as keys
    and corresponding English words as values.
"""


def read_dict(f_to_e_dict):
    fdict = {}
    dictfile = io.open(f_to_e_dict, 'r', encoding="utf8")

    for line in dictfile:
        entries = line.strip().split(
            "\t")
# expected format for each line of dictionary input file is: FOREIGNWORD[tab]ENGLISHWORD (where [tab] means '\t')
        fdict[entries[0]] = entries[1]

    return fdict


"""
ENGL_WORDS: Inputs are (1) list of foreign words and (2) f-to-e word-to-word dictionary. Perform word-to-word
replacement. Restore capitalization to first word
    of each sentence. Return list of English words (still including punctuation "words"). Any foreign words not found in
     the dictionary are passed through unchanged.
"""


def engl_words(f, fdict):
    e = []

    for word in f:
        if word in fdict:
            word = fdict[word]

        # check if this is the beginning of the file or if the previous "word" was an end-of-sentence punctuation;
        # if so, capitalize current word.
        if len(e) == 0 or e[-1] in ".!?":
            word = word[0].upper() + word[1:]
        e.append(word)
    return e


"""
OUTPUT: Takes as input a list of tuples, where each tuple is a WORD / POSTAG pair. If flag is set ("TAG"), prints out
the list as a string with 
    each word formatted as "WORD/TAG". Otherwise (if flag is not set, i.e., "NOTAG"), just prints the words.
"""


def output(pos_words, flag):
    s = ""
    for item in pos_words:
        if flag:
            s += item[0] + "/" + item[1] + " "
        else:
            s += item[0] + " "
    print(s)


"""
MAIN: TODO--Note that you can change the call to function OUTPUT to use "NOTAG" instead of "TAG" to remove the POS tags
from your final print out.
"""


def main(foreign_text, f_to_e_dict):
    f = read_foreign(foreign_text)  # read foreign text into list of words
    fdict = read_dict(f_to_e_dict)  # read in dictionary
    e = engl_words(f, fdict)  # word-level substitution
    pos_e = pos_tag(
        e)
    # use NLTK function to find POS tags.
    # TODO: Acceptable to replace this with a search in your own static listing. See instructions.

    """
TODO: Here's where you can add your code (or calls to functions) to apply your 10-20 POS-based or other fix-up rules.
    """
    for i in range(len(pos_e)):
        # fix tagging
        # JJ
        if pos_e[i][0] in ('ugly', 'blue'):
            # print(pos_e[i])
            pos_e[i] = (pos_e[i][0], 'JJ')
            # print(pos_e[i])
        # VB
        if pos_e[i][0] in ('return', 'enter', 'follow', 'forbid'):
            # print(pos_e[i])
            pos_e[i] = (pos_e[i][0], 'VB')
            # print(pos_e[i])
        # VBD
        if pos_e[i][0] == 'asked':
            # print(pos_e[i])
            pos_e[i] = (pos_e[i][0], 'VBD')
            # print(pos_e[i])
        # quotations
        if pos_e[i][0] in ('«', '»'):
            # print(pos_e[i])
            pos_e[i] = ('"', '"')
            # print(pos_e[i])
    for i in range(len(pos_e) - 1, -1, -1):
        # switch adjectives and nouns
        if pos_e[i][1] in ('NN', 'NNS') and pos_e[i + 1][1] == 'JJ':
            # print(pos_e[i], pos_e[i + 1])
            pos_e[i], pos_e[i + 1] = pos_e[i + 1], pos_e[i]
            # print(pos_e[i], pos_e[i + 1])
        # flip 'there' and verbs
        if pos_e[i][1] == 'EX' and pos_e[i + 1][1] == 'VB':
            print(pos_e[i], pos_e[i + 1])
            pos_e[i], pos_e[i + 1] = pos_e[i + 1], pos_e[i]
            print(pos_e[i], pos_e[i + 1])
        # place object pronouns after verb
        if pos_e[i][1] == 'PRP' and pos_e[i + 1][1] == 'PRP' and pos_e[i + 2][1] in ('VBP', 'VB', 'VBD', 'VBN', 'VBG', 'VBZ'):
            print(pos_e[i], pos_e[i + 1], pos_e[i + 2])
            pos_e[i], pos_e[i + 1], pos_e[i + 2] = pos_e[i], pos_e[i + 2], pos_e[i + 1]
            print(pos_e[i], pos_e[i + 1], pos_e[i + 2])
        # 'to' construction
        if pos_e[i][0] == 'of' and pos_e[i + 1][1] == 'VB':
            print(pos_e[i], pos_e[i + 1])
            pos_e[i] = ('to', 'TO')
            print(pos_e[i], pos_e[i + 1])
        # deleting 'of'
        if pos_e[i][0] == 'of' and pos_e[i + 1][1] == 'JJ':
            print(pos_e[i], pos_e[i + 1])
            pos_e.pop(i)
            print(pos_e[i], pos_e[i + 1])
        # deleting 'in'
        if pos_e[i][0] == 'in' and pos_e[i + 1][1] in ('PRP$', 'VBD', 'JJ'):
            print(pos_e[i], pos_e[i + 1])
            pos_e.pop(i)
            print(pos_e[i], pos_e[i + 1])
        # moving pronouns
        if pos_e[i][1] == 'PRP$' and pos_e[i + 1][1] in ('VBD', 'VBG'):
            print(pos_e[i], pos_e[i + 1])
            pos_e[i], pos_e[i + 1] = pos_e[i + 1], pos_e[i]
            print(pos_e[i], pos_e[i + 1])
        # 'anyone'
        if pos_e[i][1] == 'RB' and pos_e[i + 2][0] == 'person':
            print(pos_e[i], pos_e[i + 1], pos_e[i + 2])
            pos_e[i + 2] = ('anyone', 'NN')
            print(pos_e[i], pos_e[i + 1], pos_e[i + 2])
        # move 'not' to after verb
        if pos_e[i][1] == "RB" and pos_e[i + 1][1] in ('VB', 'VBD', 'MD'):
            print(pos_e[i], pos_e[i + 1])
            pos_e[i], pos_e[i + 1] = pos_e[i + 1], pos_e[i]
            print(pos_e[i], pos_e[i + 1])
        # move 'the' to after verb and change to 'it'
        if pos_e[i][0] in ("the", 'The') and pos_e[i + 1][1] in ('VBP', 'VB', 'VBD', 'VBN', 'VBG', 'VBZ'):
            print(pos_e[i], pos_e[i + 1])
            pos_e[i], pos_e[i + 1] = pos_e[i + 1], pos_e[i]
            pos_e[i + 1] = ('it', 'PRP')
            print(pos_e[i], pos_e[i + 1])
        # 'there'
        if pos_e[i][0] in ('he', 'He') and pos_e[i + 3][0] in ('anyone', 'person', 'has', 'a'):
            print(pos_e[i], pos_e[i + 1], pos_e[i + 2], pos_e[i + 3])
            pos_e[i] = ('there', 'EX')
            print(pos_e[i], pos_e[i + 1], pos_e[i + 2], pos_e[i + 3])
        if pos_e[i][0] == 'one' and pos_e[i + 1][0] == 'time':
            print(pos_e[i], pos_e[i + 1])
            pos_e[i] = ('once', 'IN')
            pos_e.pop(i + 1)
            print(pos_e[i])
        if pos_e[i][0] == 'guard' and pos_e[i + 1][0] == 'furniture':
            print(pos_e[i], pos_e[i + 1])
            pos_e[i] = ('cabinet', 'NN')
            pos_e.pop(i + 1)
            print(pos_e[i])
        if pos_e[i][0] == 'spent' and pos_e[i + 1][0] == 'everywhere':
            print(pos_e[i], pos_e[i + 1])
            pos_e[i] = ('master', 'NN')
            pos_e[i+1] = ('key', 'NN')
            print(pos_e[i], pos_e[i + 1])
        # # 'had not''
        # if pos_e[i][1] == 'RB' and pos_e[i + 1][1] == 'VBD':
        #     print(pos_e[i], pos_e[i + 1])
        #     pos_e[i], pos_e[i + 1] = pos_e[i + 1], pos_e[i]
        #     print(pos_e[i], pos_e[i + 1])
    output(pos_e, NOTAG)  # print out the results. TODO: Change from "TAG" to "NOTAG" to suppress POS tags in print out.
    print(pos_e)


"""
Commandline interface takes the names of the foreign text file and the foreign-to-English dictionary.
"""
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage:\tmt.py <foreign text file> <f-to-e dictionary file')
        sys.exit(0)
    main(sys.argv[1], sys.argv[2])
