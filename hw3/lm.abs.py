"""
LM.ABS.PY
Elyse Endlich, Homework 3
"""

from __future__ import division

import math
import sys

# INITIALIZE DICTIONARIES #

# print("Creating dictionaries...")
unigram_counts = {'<UNK>': 0, '<s>': 0, '</s>': 0}
unigram_probs = {}
bigram_counts = {}
bigram_probs = {}
alpha_values = {}  # initialize dictionary for storing alpha values
# print("Dictionaries successfully created.")

# RETRIEVE D VALUE #

# print("Requesting user input for value of D...")
D = float(input("Please enter the value of D you would like to use for training the model: "))


# print("D value retrieved from user.")

def count(tuples):
    for bigram in tuples:
        # print("The bigram being trained is: ", bigram)
        x = bigram[0]
        y = bigram[1]

        # increment bigram count, initialize one or both levels of keys if necessary
        if x not in bigram_counts:
            bigram_counts[x] = {y: 1}
        elif y not in bigram_counts[x]:
            bigram_counts[x][y] = 1
        else:
            bigram_counts[x][y] += 1
        # print(bigram_counts[x])
    # print("Updated unigram counts: ", unigram_counts)
    # print("Updated bigram counts: ", bigram_counts)


# print("Count function defined successfully.")

def calc_unigram_probs():
    n = sum(unigram_counts.values()) - unigram_counts['<s>']
    for unigram in unigram_counts:
        unigram_probs[unigram] = unigram_counts[unigram] / n
    # print("Unigram probabilities: ", unigram_probs)


# print("Unigram probability function defined successfully.")

def calc_bigram_probs():
    for x in bigram_counts:
        if x not in bigram_probs:
            bigram_probs[x] = {}
        for y in bigram_counts[x]:
            # first step of abs calculation
            bigram_probs[x][y] = (bigram_counts[x][y] - D) / unigram_counts[x]
    # print("Bigram probabilities: ", bigram_probs)


# calculate alpha scores for all unigrams in the data set
def calc_alpha():
    for w1 in unigram_counts:
        if w1 != '</s>':
            # print('CALCULATING ALPHA FOR', w1)
            tmp = 0
            reserved_mass = (len(bigram_counts[w1]) * D / unigram_counts[w1])
            # print(len(bigram_counts[w1]), unigram_counts[w1])
            for key in bigram_probs[w1].keys():
                tmp += unigram_probs[key]
                # print(unigram_probs[key])
            alpha = reserved_mass / (1 - tmp)
            # print(alpha)
            alpha_values[w1] = alpha
    # print("Alpha values: ", alpha_values)


# print("Bigram probability function defined successfully.")

def train(training_file):
    f_train = open(training_file, encoding="utf8", errors='ignore')
    # print(f_train)
    # build up counts
    for line in f_train:
        # print(line)
        line = str("<s> " + line + " </s>")
        # print("The current line is ", line)
        words = line.strip().split()
        for i in range(0, len(words)):
            # Take just first occurrence of each unigram as <UNK>
            if not words[i] in unigram_counts:
                unigram_counts[words[i]] = 0
                words[i] = "<UNK>"
            unigram_counts[words[i]] += 1
        count(zip(words, words[1:]))
    # print(unigram_counts)
    unigram_counts['</s>'] = unigram_counts['<s>']
    for key, value in list(unigram_counts.items()):
        if value == 0:
            del unigram_counts[key]
    # counts completed, now calculate the probabilities
    calc_unigram_probs()
    calc_bigram_probs()
    calc_alpha()


# print("Training function defined successfully.")


def get_bigram_prob(bigram):
    # print("The bigram being tested is: ", bigram)
    x = bigram[0]
    y = bigram[1]
    if (x in bigram_probs) and (y in bigram_probs[x]):
        return bigram_probs[x][y]
    else:
        return alpha_values[x] * unigram_probs[y]


# print("Retrieving bigram probability function defined successfully.")


def perplexity(testing_file):
    # print("RUNNING PERPLEXITY FUNCTION...")
    f_test = open(testing_file, encoding="utf8", errors='ignore')
    n = 0
    log_prob_sum = 0
    for line in f_test:
        line = str("<s> " + line + " </s>")
        unigrams = line.strip().split()
        for i in range(0, len(unigrams)):
            if not unigrams[i] in unigram_counts:
                unigrams[i] = "<UNK>"
        # print(unigrams)
        # print(line)
        for bigram in zip(unigrams, unigrams[1:]):
            # print("CURRENTLY TESTING BIGRAM", bigram)
            n += 1
            bigram_prob = get_bigram_prob(bigram)
            # print(bigram_prob)
            if bigram_prob == 0:
                sys.exit("Error: Bigram probability equals zero, terminating!")
            else:
                log_prob_sum += math.log10(bigram_prob)
    return 10 ** abs(log_prob_sum / n)


# print("Perplexity function defined successfully.")


def main(training_file, testing_file):
    train(training_file)
    print("Perplexity: %.2f" % perplexity(testing_file))


# print("Main function defined successfully.")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage:\tlm.py <training file> <test file>')
        sys.exit(0)
    main(sys.argv[1], sys.argv[2])
