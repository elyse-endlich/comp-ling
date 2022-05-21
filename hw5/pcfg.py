"""
PCFG.PY
Elyse Endlich
March 2022
"""

import io
import sys
import re

# pre-compile our common regular expressions for efficient re-use
embedding = re.compile(r"^(\([^()]*)(\(.*)")
resolved = re.compile(r"^\(([^ ]+) ([^)]+)\)(.*)")

"""
    The following dictionary is a single global 
    store for the learned set of CFG rules, both phrasal and lexical.
    Use as-is or modify as required for your implementation.
"""

cfg = {}

"""
ADD_RULE: Build CFG as a dictionary of dictionaries. If we haven't seen the current LHS tag before, 
    initialize a new second-level dictionary for this LHS tag.

    NOTE: for CFG implementation (as opposed to PCFG), we don't care how many times we see a given
    rule, only that we've seen it at least once, thus we can just keep reinitializing the same rule
    over and over again (i.e., with null value None).

    TODO: For PCFG, update to count appearances.
"""


def add_rule(lhs, rhs):
    if lhs not in cfg:
        cfg[lhs] = {rhs: 1}
    elif rhs not in cfg[lhs]:
        cfg[lhs][rhs] = 1
    else:
        cfg[lhs][rhs] += 1
    # cfg[lhs][rhs] = None


"""
BUILD_CFG: core recursive routine to crawl tree, resolve deeper embeddings, identify rule
    components, and call ADD_RULE to capture what's found
"""


def build_cfg(tree):
    # find any remaining further/deeper levels of embedding in the input tree/subtree
    further_embedding = embedding.match(tree)

    # capture whether this is a terminal node
    terminal = not further_embedding

    # loop to resolve all deeper embeddings. could be any number of right-hand nodes to resolve
    while further_embedding:
        # save everything to the left of the further embedding,
        #    e.g., for "(A B C (D (E (F G)))", preamble=="(A B C "
        preamble = further_embedding.group(1)

        # capture the continuation to be processed,
        #    e.g., for "(A B C (D (E (F G)))", subtree=="(D (E (F G)))"
        subtree = further_embedding.group(2)

        # recursively resolve further embedding. return from recursion will be flat
        #    e.g., return for processing subtree of "(D (E (F G)))" will be "D"
        subtree = build_cfg(subtree)

        # prepare to continue loop if we have multiple sisters with further embedding
        #    e.g., if tree was "(A (B C) (D E))", after recursion above, subtree will
        #    now be "B (D E)". We reconnect the preamble "(A " to make a now partially-
        #    resolved tree "(A B (D E))" and loop
        tree = preamble + subtree
        further_embedding = embedding.match(tree)

    # prepare to build a rule
    rule_components = resolved.match(tree)
    lhs = rule_components.group(1)
    rhs = rule_components.group(2)

    # mark as terminal node only if (sub)tree was already flat on entry to this call
    if terminal:
        rhs = "* " + rhs

    add_rule(lhs, rhs)

    tree_continuation = rule_components.group(3)
    return lhs + tree_continuation


"""
OUTPUT: Loop through full captured CFG, output formatted rules.
    TODO: Update to print formatted probabilities.
"""


def output(cfg):
    with open('long.pcfg', 'w') as f:
        for lhs in sorted(cfg):
            for rhs in sorted(cfg[lhs]):
                # print(lhs, rhs, cfg[lhs][rhs])
                prob = str(cfg[lhs][rhs]/sum(cfg[lhs].values()))
                if len(prob) > 8:
                    prob2 = float(prob)
                    prob = str(round(prob2, 6))
                print("%s -> %s \t\t%s" % (lhs, rhs, prob.ljust(8, '0')))
                f.write("%s -> %s \t\t%s\n" % (lhs, rhs, prob.ljust(8, '0')))


"""
Takes in the treebank training file, loops to begin
recursive processing of each sentence line. Outputs
resulting CFG at end.
"""


def main(treebank):
    treebank_file = io.open(treebank, 'r')
    for tree in treebank_file:
        build_cfg(tree.strip())
    output(cfg)


"""
Commandline interface takes the names of the treebank training file.
"""
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage:\tcfg.py <treebank training file>')
        sys.exit(0)
    main(sys.argv[1])
