#!/usr/bin/env python3

import json
import pprint
import os
import hashlib


def filter_json_by_allowlist(json_object, allowlist):
    filtered_json = {}
    for key, value in json_object.items():
        if key in allowlist:
            filtered_json[key] = value
    return filtered_json


directory = "./results/env"

hash_to_meta = dict()
hash_to_os = dict()
hash_to_browser_release = dict()

for filename in os.listdir(directory):
    if not (filename.endswith(".json") and "env" in filename):
        continue

    FILE_A = filename
    DATA_A = None

    with open(f"{directory}/{FILE_A}", "r") as json_file:
        DATA_A = json.load(json_file)

    meta_a = DATA_A["meta"]
    DATA_A = DATA_A["results"]
    DATA_A = filter_json_by_allowlist(
        DATA_A,
        [
            "safe-area-inset-top",
            "safe-area-inset-right",
            "safe-area-inset-bottom",
            "safe-area-inset-left",
        ],
    )

    # print("\n--------------")
    # print(
    #     f"`{meta_a['host']} {meta_a['os']} {meta_a['browser']} ({meta_a['release']})`."
    # )

    hash = hashlib.md5(json.dumps(DATA_A).encode()).hexdigest()
    if hash not in hash_to_meta:
        hash_to_meta[hash] = [meta_a]
    else:
        hash_to_meta[hash].append(meta_a)

    if hash not in hash_to_os:
        hash_to_os[hash] = [meta_a["os"]]
    else:
        hash_to_os[hash].append(meta_a["os"])

    if hash not in hash_to_browser_release:
        hash_to_browser_release[hash] = [
            f"{meta_a['host']} {meta_a['os']} {meta_a['browser']} ({meta_a['release']})"
        ]
    else:
        hash_to_browser_release[hash].append(
            f"{meta_a['host']} {meta_a['os']} {meta_a['browser']} ({meta_a['release']})"
        )

# print("\n--------------")
# pprint.pprint(hash_to_meta)

# print("\n--------------")
# pprint.pprint(hash_to_os)

print("\n--------------")
pprint.pprint(hash_to_browser_release)
