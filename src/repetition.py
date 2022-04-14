"""
code adapted from https://github.com/ari-holtzman/degen/blob/master/metrics/repetition.py

returns a list of dicts which contains detailed fields on how each
example is repeating itself, specifically the phrase the generation is repeating
and how many times it is repeated.
"""


def calc_repetitions(sequences):

    objs = []
    max_n = 90
    n_repeated_examples = 0

    for gen in sequences:
        obj = {}
        rev_gen = list(reversed(gen))
        last_n_repeats = [0] * max_n

        for n in range(1, max_n + 1):
            n_repeat = 1
            while (
                len(rev_gen[n * n_repeat : n * (n_repeat + 1)]) == n
                and rev_gen[n * n_repeat : n * (n_repeat + 1)] == rev_gen[:n]
            ):
                n_repeat += 1
            last_n_repeats[n - 1] = n_repeat
        max_repeated_n = max(range(max_n), key=lambda x: last_n_repeats[x])
        if last_n_repeats[max_repeated_n] > 1 and (
            max_repeated_n + 1 >= 3 or last_n_repeats[max_repeated_n] > 50
        ):
            obj["repetition"] = {
                "repeated_phrase": list(reversed(rev_gen[: max_repeated_n + 1])),
                "repeated_times": last_n_repeats[max_repeated_n],
                "repeated_phrase_length": max_repeated_n + 1,
            }
            n_repeated_examples += 1
        else:
            obj["repetition"] = None

        objs.append(obj)

    return objs


if __name__ == "__main__":
    sequences = [
        "hello my name is hello my name is hello my name hello my hello my name is hello my name is hello my name is"
    ]
    sequences = [sequence.split() for sequence in sequences]
    print(sequences)
    print(calc_repetitions(sequences))
