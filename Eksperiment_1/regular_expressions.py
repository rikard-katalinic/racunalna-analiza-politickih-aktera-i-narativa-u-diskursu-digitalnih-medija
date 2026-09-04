import re, tempfile, shutil
#import pandas as pd

def merge_hashtags(file):
    with open(file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    merged_rows = []
    current = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        parts = line.split("|", 3)
        if len(parts) < 4:
            continue
        col1, col2, col3, col4 = parts

        if current is None:
            current = [col1, col2, col3, col4]
            continue

        if col2.startswith("##"):
            current[1] += col2[2:]
        else:
            merged_rows.append("|".join(current))
            current = [col1, col2, col3, col4]

    if current:
        merged_rows.append("|".join(current))

    with open("test.txt", "w", encoding="utf-8") as f:
        for row in merged_rows:
            f.write(row + "\n")


def remove_rows(file):
    pattern = re.compile(r'\|Socijaldemokrat.*\|')

    with open(file, "r", encoding="utf-8") as infile, \
        tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as outfile:
        
        """
        lines = infile.readlines()
        filtered = [s for s in lines if pattern.search(s)]
        print(filtered)
        """

        for line in infile:
            if not pattern.search(line):
                outfile.write(line)

    shutil.move(outfile.name, file)


def merge_csv(file):
    with open(file, "r", encoding="utf-8") as src, \
     open("sentimenti/sentiments_total.csv", "a", encoding="utf-8") as dst:
        for line in src:
            dst.write(line)


def divide(file):
    df = pd.read_csv(file, sep="|")

    for portal_value in df["portal"].unique():
        df[df["portal"] == portal_value].to_csv(
            f"portal_{portal_value}.txt",
            sep="|",
            index=False
        )


#merge_hashtags("entiteti/entities_vecernji.csv")
#merge_csv("sentimenti/sentiments_vecernji.csv")
remove_rows("rezultati/entities_total.csv")