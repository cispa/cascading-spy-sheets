#!/usr/bin/env python3

import json
import pprint
import os
import hashlib

allowlist = [
    "font-size",
    "font-family",
    "inline-size",
    "block-size",
    "width",
    "height",
    "aspect-ratio",
    "orientation",
]


def filter_json_by_allowlist(json_object, allowlist):
    filtered_json = {}
    for key, properties in json_object.items():
        filtered_properties = {
            prop: value for prop, value in properties.items() if prop in allowlist
        }
        filtered_json[key] = filtered_properties
    return filtered_json


directory = "./results/props"

hash_to_meta = dict()
hash_to_os = dict()
hash_to_browser_release = dict()

for filename in os.listdir(directory):
    if not (filename.endswith(".json") and "props" in filename):
        continue

    FILE_A = filename
    DATA_A = None

    with open(f"{directory}/{FILE_A}", "r") as json_file:
        DATA_A = json.load(json_file)

    meta_a = DATA_A["meta"]
    DATA_A = DATA_A["results"]
    DATA_A = filter_json_by_allowlist(DATA_A, allowlist)

    hash = hashlib.md5(json.dumps(DATA_A).encode()).hexdigest()

    if hash not in hash_to_browser_release:
        hash_to_browser_release[hash] = [
            f"{meta_a['host']} {meta_a['os']} {meta_a['browser']} ({meta_a['release']})"
        ]
    else:
        hash_to_browser_release[hash].append(
            f"{meta_a['host']} {meta_a['os']} {meta_a['browser']} ({meta_a['release']})"
        )

print("\n--------------")
pprint.pprint(hash_to_browser_release)
