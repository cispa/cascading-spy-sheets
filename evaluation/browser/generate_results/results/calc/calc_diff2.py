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

print(f"Checking for differences between `{meta_a['host']} {meta_a['os']} {meta_a['browser']} ({meta_a['release']})` and `{meta_b['host']} {meta_b['os']} {meta_b['browser']} ({meta_b['release']})`.")

diffs = []
for i, run_a in enumerate(DATA_A):
    run_b = DATA_B[i]
    assert run_a["expression"] == run_b["expression"]
    if run_a["result"] != run_b["result"]:
        diffs.append({
            "expression": str(run_a["expression"]),
            "result_a": str(run_a["result"]).replace("px", ""),
            "result_b": str(run_b["result"]).replace("px", "")
        })


print("\n--------------")
print(f"Total number of differences: {len(diffs)} / {len(DATA_A)}")

if len(diffs) > 0:
    diffs = sorted(diffs, key=lambda x: len(x["expression"]))
    print("\n--------------")
    print("Shortest Expression:")
    pprint.pprint(diffs[0])

    diffs = sorted(diffs, key=lambda x: abs(float(x["result_a"]) - float(x["result_b"])), reverse=True)
    print("\nLargest Result Difference:")
    pprint.pprint(diffs[0])