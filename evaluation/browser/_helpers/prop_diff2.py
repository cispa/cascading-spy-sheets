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

assert len(DATA_A) <= len(DATA_B)
if len(DATA_A) < len(DATA_B):
    print("WARNING: first file is shorter.")

print(
    f"Checking for differences between `{meta_a['host']} {meta_a['os']} {meta_a['browser']} ({meta_a['release']})` and `{meta_b['host']} {meta_b['os']} {meta_b['browser']} ({meta_b['release']})`."
)

BLOCK_ALLOW_TOGGLE = "BLOCK"

blocklist = [
    # transform
    "transform-origin",
    "perspective-origin",
    # color stuff
    "background-color",
    "border-block-end-color",
    "border-block-start-color",
    "border-bottom-color",
    "border-inline-end-color",
    "border-inline-start-color",
    "border-left-color",
    "border-right-color",
    "border-top-color",
    "column-rule-color",
    "outline-color",
    "caret-color",
    # text stuff
    "color",
    "-webkit-text-fill-color",
    "-webkit-text-stroke-color",
    "text-decoration",
    "text-decoration-color",
    "text-emphasis-color",
    # margins and padding
    "margin-block-end",
    "margin-block-start",
    "margin-bottom",
    "margin-top",
]

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

num_diffs = 0
num_total = 0
diffs = {}
for xpath in DATA_A:
    style_a, style_b = DATA_A[xpath], DATA_B[xpath]
    shared_props = set(style_a.keys()).intersection(set(style_b.keys()))
    for prop in sorted(shared_props):
        if BLOCK_ALLOW_TOGGLE == "BLOCK":
            if prop in blocklist:
                continue
        else:
            if prop not in allowlist:
                continue
        if style_a[prop] != style_b[prop]:
            if xpath not in diffs:
                diffs[xpath] = {}
            diffs[xpath][prop] = {"style_a": style_a[prop], "style_b": style_b[prop]}
            num_diffs += 1
        num_total += 1
    for prop in sorted(set(style_a.keys()) - shared_props):
        if BLOCK_ALLOW_TOGGLE == "BLOCK":
            if prop in blocklist:
                continue
        else:
            if prop not in allowlist:
                continue
        if xpath not in diffs:
            diffs[xpath] = {}
        diffs[xpath][prop] = {"style_a": style_a[prop], "style_b": ""}
        num_diffs += 1
    for prop in sorted(set(style_b.keys()) - shared_props):
        if BLOCK_ALLOW_TOGGLE == "BLOCK":
            if prop in blocklist:
                continue
        else:
            if prop not in allowlist:
                continue
        if xpath not in diffs:
            diffs[xpath] = {}
        diffs[xpath][prop] = {"style_a": "", "style_b": style_b[prop]}
        num_diffs += 1


print("\n--------------")
print(f"Total number of differences: {num_diffs} / {num_total}")

if num_diffs > 0:
    print("\n--------------")
    pprint.pprint(diffs)
