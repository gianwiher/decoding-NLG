import re

from tqdm import tqdm

WIKI_PATH = "../data/datasets/wikitext-103-raw/"

BOS = "<|startoftext|>"
EOS = "<|endoftext|>"
UNK = "<|unk|>"


def data_loader(path):
    """generator object for memory efficient file reading"""
    with open(path) as f:
        for line in f:
            if line.strip():
                yield clean(line.strip().replace("<unk>", UNK))


def clean(string):
    """cleans most of the word tonkenization from wikitext"""

    # punctuation and closing parenthesis
    punctuation = re.compile(r"\s([\.\,\;\:\'\!\?\-\_\]\}\)\`])")
    quotes = re.compile(r'((?:^|\s)")\s([^"]+?)\s("(?:\s|$))')  # quotes
    ats = re.compile(r"(\s\@)(.)(\@\s)")  # wierd @ symbols
    opar = re.compile(r"([\(\[\{])\s")  # opening parenthesis

    replacements = [
        (quotes, r"\1\2\3"),
        (punctuation, r"\1"),
        (ats, r"\2"),
        (opar, r"\1"),
    ]

    for pattern, new in replacements:
        string = re.sub(pattern, new, string)

    return string


def main():
    splits = ["test", "train", "valid"]
    lens = {"test": 4358, "train": 1801350, "valid": 3760}
    for split in splits:
        source_path = WIKI_PATH + "wiki." + split + ".raw"
        output_path = WIKI_PATH + "wiki." + split + ".processed.txt"

        source_loader = data_loader(source_path)

        print(f"processing {split} split")

        with open(output_path, "w") as f:
            for source in tqdm(source_loader, total=lens[split]):
                f.write(source)
                f.write("\n")


if __name__ == "__main__":
    main()
