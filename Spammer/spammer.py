"""
SPAMMER.PY - ELYSE ENDLICH

With many thanks to Dan Jurafsky, this program was adapted from the Stanford NLP class SpamLord homework assignment.
Please do not make this code or the data public.

This version has no patterns initially, but has two patterns suggested in comments.

Look for lines marked TODO for areas to potentially modify.
"""

from __future__ import division
import sys
import os
import re
import io
import pprint

"""
TODO
Add to these two lists of patterns to match email addresses and phone numbers
in the text, including examples of "obscured" addresses and/or numbers.
You are also free to modify other parts of the code, including the addition
of other lists of patterns, other than epatterns_edu[] and ppatterns[] below,
but this you do "at your own risk"! :-)
"""
# email .edu patterns

# each regular expression pattern should have exactly two sets of parentheses.
#   the first parenthesis should be around the someone part
#   the second parenthesis should be around the somewhere part
#   in an email address whose standard form is someone@somewhere.edu
epatterns_edu = []
epatterns_edu.append('(([A-Za-z]+\.)?([A-Za-z]+\-)?[A-Za-z]+)@([A-Za-z]+)\.edu')
epatterns_edu.append('(([A-Za-z]+\.)?([A-Za-z]+\-)?[A-Za-z]+)@([A-Za-z]+\.[A-Za-z]+)\.edu')
epatterns_edu.append('(([A-Za-z]+\[dot\])?[A-Za-z]+) ?\[at\] ?([A-Za-z]+) ?\[dot\] ?edu')
epatterns_edu.append('(([A-Za-z]+\[dot\])?[A-Za-z]+) \[at\] ([A-Za-z]+\.[A-Za-z]+)\.edu')
epatterns_edu.append('(([A-Za-z]+\.)?[A-Za-z]+) ?\(at\) ?([A-Za-z]+)\.edu')
epatterns_edu.append('(([A-Za-z]+\.)?[A-Za-z]+) ?\(at\) ?([A-Za-z]+) ?\(dot\) ?edu')
epatterns_edu.append('(([A-Za-z]+ DOT )?[A-Za-z]+) ?AT ?([A-Za-z]+) ?DOT ?edu')
epatterns_edu.append('(([A-Za-z]+ DOT )?[A-Za-z]+) ?AT ?([A-Za-z]+)\.edu')
epatterns_edu.append("(([A-Za-z]+ 'd0t' )?[A-Za-z]+) '@' ([A-Za-z]+) 'd0t' edu")

epatterns_com = []
epatterns_com.append('(([A-Za-z]+\.)?([A-Za-z]+\-)?[A-Za-z]+)@([A-Za-z]+)\.com')
epatterns_com.append('(([A-Za-z]+\.)?([A-Za-z]+\-)?[A-Za-z]+)@([A-Za-z]+\.[A-Za-z]+)\.com')
epatterns_com.append('(([A-Za-z]+\[dot\])?[A-Za-z]+) ?\[at\] ?([A-Za-z]+) ?\[dot\] ?com')
epatterns_com.append('(([A-Za-z]+\[dot\])?[A-Za-z]+) \[at\] ([A-Za-z]+\.[A-Za-z]+)\.com')
epatterns_com.append('(([A-Za-z]+\.)?[A-Za-z]+) ?\(at\) ?([A-Za-z]+)\.com')
epatterns_com.append('(([A-Za-z]+\.)?[A-Za-z]+) ?\(AT\) ?([A-Za-z]+)\.com')
epatterns_com.append('(([A-Za-z]+\.)?[A-Za-z]+) ?\(AT\) ?([A-Za-z]+)')
epatterns_com.append('(([A-Za-z]+\.)?[A-Za-z]+) ?\(at\) ?([A-Za-z]+) ?\(dot\) ?com')
epatterns_com.append('(([A-Za-z]+ DOT )?[A-Za-z]+) ?AT ?([A-Za-z]+) ?DOT ?com')
epatterns_com.append('(([A-Za-z]+ DOT )?[A-Za-z]+) ?AT ?([A-Za-z]+)\.com')
epatterns_com.append("(([A-Za-z]+ 'd0t' )?[A-Za-z]+) '@' ([A-Za-z]+) 'd0t' com")

# GAVE UP ON:
# Garcia (email and phone)
# Jurafsky (email)
# Kauchak (email)
# Kung (email)
# Moore (email)
# Hudgings (phone)
# Rad (phone)

# phone patterns
# each regular expression pattern should have exactly three sets of parentheses.
#   the first parenthesis should be around the area code part XXX
#   the second parenthesis should be around the exchange part YYY
#   the third parenthesis should be around the number part ZZZZ
#   in a phone number whose standard form is XXX-YYY-ZZZZ
ppatterns = []
ppatterns.append('(\d{3})-(\d{3})-(\d{4})')
ppatterns.append('(\d{3}) (\d{3}) (\d{4})')
ppatterns.append('(\(\d{3}\)) (\d{3})-(\d{4})')
ppatterns.append('(\(\d{3}\))\n  (\d{3})-(\d{4})')
ppatterns.append('(\(\d{3}\)) (\d{3}) (\d{4})')
ppatterns.append('(\d{3})[^A-Za-z0-9 \(\)\.\-]+(\d{3}) (\d{4})')
ppatterns.append('(909)\.(\d{3})\.(\d{4})')
ppatterns.append('\+1 (\d{3})\.(\d{3})\.(\d{4})')
ppatterns.append('(\(\d{3}\)) (\d{3})(\d{4})')
ppatterns.append('(909)(\d{3})(\d{4})')
ppatterns.append('(909) (\d{3})(\d{4})')

"""
This function takes in a filename along with the file object and
scans its contents against regex patterns. It returns a list of
(filename, type, value) tuples where type is either an 'e' or a 'p'
for email or phone, and value is the formatted phone number or email.
The canonical formats are:
    (name, 'p', '###-###-#####')
    (name, 'e', 'someone@something')
If the numbers you submit are formatted differently they will not
match the gold answers

TODO
If you have added other lists beyond epaterns[] and ppatterns[],  you
may need to add additional for-loops that match the patterns in those lists
and produce correctly formatted results to append to the res list.
"""
def process_file(name, f):
    # note that debug info should be printed to stderr
    # sys.stderr.write('[process_file]\tprocessing file: %s\n' % (path))
    #print(name)
    res = []
    for line in f:
        # print(line)
        for epat in epatterns_edu:
            # each epat has 2 sets of parentheses so each match will have 2 items in a list
            matches = re.findall(epat,line)
            #matches = [tuple(s if s != "(com)" else "com" for s in tup) for tup in matches]
            #matches = [tuple(s if s != "(edu)" else "edu" for s in tup) for tup in matches]
            # print(matches)
            for m in matches:
                # string formatting operator % takes elements of list m
                #   and inserts them in place of each %s in the result string
                # print(m)
                if len(m) == 3:
                    email = '%s@%s.edu' % (m[0], m[2])
                    email = re.sub("\[dot\]", ".", email)
                    email = re.sub(" DOT ", ".", email)
                    email = re.sub(" 'd0t' ", ".", email)
                    # print("LEN3", email)
                elif len(m) == 4:
                    email = '%s@%s.edu' % (m[0], m[-1])
                    email = re.sub("\[dot\]", ".", email)
                    email = re.sub(" DOT ", ".", email)
                    email = re.sub(" 'd0t' ", ".", email)
                    # print("LEN3", email)
                else:
                    email = '%s@%s.edu' % m
                    # print("OTHER", email)

                res.append((name,'e',email))

        for epat in epatterns_com:
            # each epat has 2 sets of parentheses so each match will have 2 items in a list
            matches = re.findall(epat,line)
            #matches = [tuple(s if s != "(com)" else "com" for s in tup) for tup in matches]
            #matches = [tuple(s if s != "(edu)" else "edu" for s in tup) for tup in matches]
            # print(matches)
            for m in matches:
                # string formatting operator % takes elements of list m
                #   and inserts them in place of each %s in the result string
                # print(m)
                if len(m) == 3:
                    email = '%s@%s.com' % (m[0], m[2])
                    email = re.sub("\[dot\]", ".", email)
                    email = re.sub(" DOT ", ".", email)
                    email = re.sub(" 'd0t' ", ".", email)
                    # print("LEN3", email)
                elif len(m) == 4:
                    email = '%s@%s.com' % (m[0], m[-1])
                    email = re.sub("\[dot\]", ".", email)
                    email = re.sub(" DOT ", ".", email)
                    email = re.sub(" 'd0t' ", ".", email)
                    # print("LEN3", email)
                else:
                    email = '%s@%s.com' % m
                    # print("OTHER", email)

                res.append((name,'e',email))

        for ppat in ppatterns:
            # each ppat has 3 sets of parentheses so each match will have 3 items in a list
            matches = re.findall(ppat,line)
            for m in matches:
                phone = '%s-%s-%s' % m
                phone = re.sub("\(", "", phone)
                phone = re.sub("\)", "", phone)
                res.append((name,'p',phone))
    return res

"""
You should not edit this function.
"""
def process_dir(data_path):
    # get filename candidates
    guess_list = []
    for fname in os.listdir(data_path):
        if fname[0] == '.':
            continue
        path = os.path.join(data_path,fname)
        f = io.open(path,'r', encoding='latin-1')
        f_guesses = process_file(fname, f)
        guess_list.extend(f_guesses)
    return guess_list

"""
You should not edit this function.
Given a path to a tsv (tab-separated values) file of gold emails and phone numbers
this function returns a list of tuples of the canonical form:
(filename, type, value)
"""
def get_gold(gold_path):
    # get gold answers
    gold_list = []
    f_gold = io.open(gold_path,'r')
    for line in f_gold:
        gold_list.append(tuple(line.strip().split('\t')))
    return gold_list

"""
You should not edit this function.
Given a list of guessed contacts and gold contacts, this function
computes the intersection and set differences, to compute the true
positives, false positives, and false negatives, and from these
also precision, recall, and F1-score (harmonic mean of precision
and recall). Importantly, it converts all strings to lower
case before comparing
"""
def score(guess_list, gold_list):
    guess_list = [(fname, _type, value.lower()) for (fname, _type, value) in guess_list]
    gold_list = [(fname, _type, value.lower()) for (fname, _type, value) in gold_list]
    guess_set = set(guess_list)
    gold_set = set(gold_list)

    tp = guess_set.intersection(gold_set)
    fp = guess_set - gold_set
    fn = gold_set - guess_set

    pp = pprint.PrettyPrinter()
    print ('True Positives (%d): ' % len(tp))
    pp.pprint(tp)
    print ('False Positives (%d): ' % len(fp))
    pp.pprint(fp)
    print ('False Negatives (%d): ' % len(fn))
    pp.pprint(fn)

    recall = len(tp)/(len(tp)+len(fn))
    if len(tp)+len(fp) > 0:
        precision = len(tp)/(len(tp)+len(fp))
        f1 = (2*precision*recall)/(precision+recall)
    else:
        precision = 0
        f1 = 0
    print ('Summary: tp=%d, fp=%d, fn=%d, precision=%.4f, recall=%.4f, F1=%.4f' % (len(tp),len(fp),len(fn),precision,recall,f1))

"""
You should not edit this function.
It takes in the string path to the data directory and the gold file
"""
def main(data_path, gold_path):
    guess_list = process_dir(data_path)
    gold_list =  get_gold(gold_path)
    score(guess_list, gold_list)

"""
commandline interface takes a directory name and gold file.
It then processes each file within that directory and extracts any
matching emails or phone numbers and compares them to the gold file
"""
if __name__ == '__main__':
    if (len(sys.argv) != 3):
        print ('usage:\tspammer.py <data_dir> <gold_file>')
        sys.exit(0)
    main(sys.argv[1],sys.argv[2])
