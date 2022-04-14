import csv
import re

from tqdm import tqdm

# change this to the directory where the writing prompt dataset is located
WP_PATH = "../data/datasets/writingPrompts/"

BOS = "<|startoftext|>"
EOS = "<|endoftext|>"
SEP = "<|seperator|>"
NL = "<newline>"


def data_loader(path):
    """loads lines into memory from file"""
    with open(path) as f:
        for line in f:
            yield clean(
                line.strip()
                .replace(NL, "")
                .replace("*", "")
                .replace("``", '"')
                .replace("''", '"')
            )


def clean(string):
    """cleans most of the word tonkenization from writingpromts"""

    # punctuation and closing parenthesis
    punctuation = re.compile(r"\s([\.\,\;\:\'\!\?\-\_\]\}\)\`])")
    quotes = re.compile(r'((?:^|\s)")\s([^"]+?)\s("(?:\s|$))')  # quotes
    nts = re.compile(r"(\w)\s(n\'t)")  # had n't -> hadn't
    opar = re.compile(r"([\(\[\{])\s")  # opening parenthesis

    replacements = [
        (quotes, r"\1\2\3"),
        (punctuation, r"\1"),
        (nts, r"\1\2"),
        (opar, r"\1"),
    ]

    for pattern, new in replacements:
        string = re.sub(pattern, new, string)

    return string


def main():
    csv_file = False
    splits = ["test", "train", "valid"]
    lens = {"test": 15138, "train": 272600, "valid": 15620}
    for split in splits:
        source_path = WP_PATH + split + ".wp_source"
        target_path = WP_PATH + split + ".wp_target"
        output_path = WP_PATH + split + ".comb.txt"

        source_loader = data_loader(source_path)
        target_loader = data_loader(target_path)
        print(f"processing {split} split")

        if not csv_file:
            with open(output_path, "w") as f:
                for source, target in tqdm(
                    zip(source_loader, target_loader), total=lens[split]
                ):
                    if source.startswith("[WP]"):
                        f.write(BOS + source + SEP + target + EOS)
                        f.write("\n")

        else:
            output_path = output_path.replace("txt", "csv")
            header = ["text"]
            with open(output_path, "w", newline="") as csvfile:
                writer = csv.writer(
                    csvfile, delimiter=",", quoting=csv.QUOTE_MINIMAL, quotechar='"'
                )
                writer.writerow(header)
                for source, target in tqdm(
                    zip(source_loader, target_loader), total=lens[split]
                ):
                    if source.startswith("[WP]"):
                        line = BOS + source + SEP + target + EOS
                        writer.writerow([line])


if __name__ == "__main__":
    main()
