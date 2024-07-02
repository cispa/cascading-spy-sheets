#!/usr/bin/env python3

import json
import pprint
import os
import hashlib

directory = "./results/valuecontainer"

hash_to_browser_release = dict()

for filename in os.listdir(directory):
    if not filename.endswith(".json"):
        continue

    FILE_A = filename
    DATA_A = None

    with open(f"{directory}/{FILE_A}", "r") as json_file:
        DATA_A = json.load(json_file)

    meta_a = DATA_A["meta"]
    DATA_A = DATA_A["results"]

    print("\n--------------")
    print(
        f"`{meta_a['host']} {meta_a['os']} {meta_a['browser']} ({meta_a['release']})`."
    )
    pprint.pprint(DATA_A)

    hash = hashlib.md5(json.dumps(DATA_A).encode()).hexdigest()
    if hash not in hash_to_browser_release:
        hash_to_browser_release[hash] = [f"{meta_a['host']} {meta_a['os']} {meta_a['browser']} ({meta_a['release']})"]
    else:
        hash_to_browser_release[hash].append(f"{meta_a['host']} {meta_a['os']} {meta_a['browser']} ({meta_a['release']})")

print("\n--------------")
pprint.pprint(hash_to_browser_release)