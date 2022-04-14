# importing module
import logging
from collections import Counter

import numpy as np

logger = logging.getLogger(__name__)


def get_k_grams(sequence, k):
    """Returns the k-grams of the input sequence"""

    grams = []
    if len(sequence) < k:
        logger.warning(f"input sequence len is {len(sequence)} but k is {k}")
        return np.nan

    for i in range(len(sequence) - k + 1):
        grams.append(tuple(sequence[i : i + k]))

    return grams


def dist_k(sequences, k):
    """
    Number of unique k-grams divided by the number of tokens
    :param sequences: a list of sequences of tokens
    :param k: size of k-gram
    """
    res = []
    for sequence in sequences:
        kgrams = get_k_grams(sequence, k)
        if kgrams is np.nan:
            res.append(np.nan)
            continue
        unique = len(set(kgrams))
        total = len(sequence) - k + 1
        res.append(unique / total if total != 0 else np.nan)
    return res


def ent_k(sequences, k):
    """
    Returns entropy of empirical distribution over k-grams
    :param sequences: a list of sequences of tokens
    :param k: size of k-gram
    """
    res = []

    for sequence in sequences:
        k_counter = Counter()
        kgrams = get_k_grams(sequence, k)

        if kgrams is np.nan:
            res.append(np.nan)
            continue

        k_counter.update(kgrams)

        counts = np.array(list(k_counter.values()))
        s = counts.sum()

        res.append(
            (-1.0 / s) * np.sum(counts * np.log(counts / s)) if s != 0 else np.nan
        )

    return res


def ngram_diversity(sequences, n):
    """Returns the mean of the fraction of unique k-grams for k in {1,...,n}."""

    divs = np.array([dist_k(sequences, k) for k in range(1, n + 1)])
    return divs.mean(axis=0).tolist()


def ngram_diversity_from_kdivs(kdivs):
    return np.array(kdivs).mean(axis=0).tolist()


def len_distribution(sentences):
    """returns counter of sentence lengths"""
    lens = Counter()
    for sentence in sentences:
        lens[len(sentence)] += 1
    return lens


def lengths(sentences):
    lst = []
    for sentence in sentences:
        lst.append(len(sentence))
    return lst


def vocab_size_distribution(sequences):
    """returns the vocabulary size of each sequence"""
    vocab_sizes = Counter()
    for sentence in sequences:
        vocab_sizes[len(set(sentence))] += 1
    return vocab_sizes


def vocab_distribution(sequences):
    """"""
    vocab = Counter()
    for sequence in sequences:
        if sequence:
            vocab.update(get_k_grams(sequence, 1))
    return vocab


if __name__ == "__main__":
    string = "ich liebe dich ich liebe dich nicht"
    string2 = "The quick brown fox jumps over the lazy dog."
    string3 = "The bees are happy"
    strings = [string, string2, string3]
    k = 2
    seq = [s.split() for s in strings]

    ek = ent_k(seq, k)
    dk = dist_k(seq, k)

    print(f'The sequence "{string}" contains the following {k}-grams:')
    print(get_k_grams(seq[0], k))
    print(f"Dist-{k}: {dk}")
    print(f"Ent-{k}: {ek}")
    print("N-gram div:", ngram_diversity(seq, 3))
    print("lengths: ", len_distribution(seq))
    print("vocab sizes: ", vocab_size_distribution(seq))
    print("vocab_distribution: ", vocab_distribution(seq))
