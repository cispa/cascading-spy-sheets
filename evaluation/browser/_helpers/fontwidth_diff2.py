import json
import pprint
import math
import sys

if len(sys.argv) != 3:
    print("Please provide two file paths.")
    sys.exit(-1)

FILE_A = sys.argv[1]
FILE_B = sys.argv[2]

DATA_A = None
DATA_B = None

with open(FILE_A, "r") as json_file:
    DATA_A = json.load(json_file)

with open(FILE_B, "r") as json_file:
    DATA_B = json.load(json_file)

meta_a = DATA_A["meta"]
meta_b = DATA_B["meta"]
assert meta_a != meta_b

DATA_A = DATA_A["results"]
DATA_B = DATA_B["results"]

assert len(DATA_A) == len(DATA_B)

print(f"Checking for differences between `{meta_a['host']} {meta_a['os']} {meta_a['browser']} ({meta_a['release']})` and `{meta_b['host']} {meta_b['os']} {meta_b['browser']} ({meta_b['release']})`.")

num_total_diff_fonts = 0
num_total_diffs = 0
for font in DATA_A:
    diffs = []
    examples = []
    for style in DATA_A[font]:
        for weight in DATA_A[font][style]:
            for size in DATA_A[font][style][weight]:
                results_a = DATA_A[font][style][weight][size]
                results_b = DATA_B[font][style][weight][size]

                if results_a != results_b:
                    font_diff = True
                    diffs.append(f"{style} {weight}")
                    examples.append((results_a, results_b))

    if len(diffs) > 0:
        print(f"\n{font}")
        print(f"Example: {diffs[0]}")
        print(examples[0][0])
        print(examples[0][1])
        num_total_diffs += len(examples)
        num_total_diff_fonts += 1

print("\n--------------")
print(f"Total number of different fonts: {num_total_diff_fonts} / {len(DATA_A)}")
print(f"Total number of differences: {num_total_diffs}")