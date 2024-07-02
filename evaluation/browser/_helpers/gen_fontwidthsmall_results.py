#!/usr/bin/env python3

import json
import pprint
import math
from collections import Counter
import sys
import os
import hashlib

hash_to_meta = dict()
hash_to_os = dict()
hash_to_browser_release = dict()

files = []

# directory = "./results/fontcontainer"
# for filename in os.listdir(directory):
#     if not (filename.endswith(".json") and "fontcontainer" in filename):
#         continue
#     files.append(f"{directory}/{filename}")

directory = "./results/fontcontainer-small"
for filename in os.listdir(directory):
    if not (filename.endswith(".json") and "fontcontainer-small" in filename):
        continue
    files.append(f"{directory}/{filename}")

previous_fonts = set()
for filepath in files:
    FILE_A = filepath
    DATA_A = None

    with open(filepath, "r") as json_file:
        DATA_A = json.load(json_file)

    meta_a = DATA_A["meta"]
    DATA_A = DATA_A["results"]

    if len(previous_fonts) == 0:
        previous_fonts = set(DATA_A.keys())
    else:
        print("")
        print(filepath)
        assert previous_fonts == set(DATA_A.keys())

    # print(
    #     f"Checking for differences on `{meta_a['host']} {meta_a['os']} {meta_a['browser']} ({meta_a['release']})`."
    # )

    no_differences = set()
    num_total_diff_fonts = 0
    num_total_diffs = 0
    for font in DATA_A:
        if font == "ThisFontDoesNotExist":
            continue
        diffs = []
        examples = []
        for style in DATA_A[font]:
            for weight in DATA_A[font][style]:
                for size in DATA_A[font][style][weight]:
                    results_a = DATA_A[font][style][weight][size]
                    baseline = DATA_A["ThisFontDoesNotExist"][style][weight][size]

                    if results_a != baseline:
                        diffs.append(f"{style} {weight} {size}")
                        examples.append((results_a, baseline))

                for size in range(6, 12):
                    if size == 11:
                        continue
                    if str(size) in DATA_A[font][style][weight]:
                        del DATA_A[font][style][weight][str(size)]
            for weight in range(200, 1100, 100):
                if str(weight) in DATA_A[font][style]:
                    del DATA_A[font][style][str(weight)]

        if len(diffs) > 0:
            # print(f"\n{font}")
            # print(f"Example: {diffs[0]}")
            # print(examples[0][0])
            # print(examples[0][1])
            num_total_diffs += len(examples)
            num_total_diff_fonts += 1
        else:
            no_differences.add(font)

    print("\n--------------")
    print(
        f"`{meta_a['host']} {meta_a['os']} {meta_a['browser']} ({meta_a['release']})`."
    )
    print(
        f"Total number of detected fonts: {num_total_diff_fonts} / {len(DATA_A) - 1}"
    )

    hash = hashlib.md5(json.dumps(DATA_A).encode()).hexdigest()
    if hash not in hash_to_meta:
        hash_to_meta[hash] = [meta_a]
    else:
        hash_to_meta[hash].append(meta_a)

    if hash not in hash_to_os:
        hash_to_os[hash] = [meta_a['os']]
    else:
        hash_to_os[hash].append(meta_a['os'])

    if hash not in hash_to_browser_release:
        hash_to_browser_release[hash] = [f"{meta_a['host']} {meta_a['os']} {meta_a['browser']} ({meta_a['release']})"]
    else:
        hash_to_browser_release[hash].append(f"{meta_a['host']} {meta_a['os']} {meta_a['browser']} ({meta_a['release']})")

# print("\n--------------")
# pprint.pprint(hash_to_meta)

# print("\n--------------")
# pprint.pprint(hash_to_os)

print("\n--------------")
pprint.pprint(hash_to_browser_release)