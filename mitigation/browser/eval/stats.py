import json
import pprint
import numpy as np

def read_json_file(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


file_path1 = "resultsWithExtension.json"
file_path2 = "resultsWithoutExtension.json"

data1 = read_json_file(file_path1)
data2 = read_json_file(file_path2)

diff_keys = [
    "requestCount",
    "responseCount",
    "accumulatedRequestBodySize",
    "accumulatedResposeBodySize",
    "navigationDuration",
    "resourceDuration",
    "fcp",
]

diffs = {}
urls = set(data1.keys()).intersection(set(data2.keys()))

for url in urls:
    diffs[url] = {}
    for diff_key in diff_keys:
        if diff_key in data1[url] and diff_key in data2[url]:
            diffs[url][diff_key] = data1[url][diff_key] - data2[url][diff_key]


pprint.pprint(diffs)
print(f"\nDiffs: {len(diffs)}")
print(f"Skips: {len(set(data1.keys()).difference(set(data2.keys())))}")

print(f"\nAverage Request Count: {np.average([ data2[url]['requestCount'] for url in urls])}")
print(f"Average Request Count Diff: {np.average([ diffs[url]['requestCount'] for url in urls])}")

print(f"\nMedian Request Count: {np.median([ data2[url]['requestCount'] for url in urls])}")
print(f"Median Request Count Diff: {np.median([ diffs[url]['requestCount'] for url in urls])}")

print(f"\nAverage accumulatedResposeBodySize: {np.average([ data2[url]['accumulatedResposeBodySize'] for url in urls]) / 1000}KB")
print(f"Average accumulatedResposeBodySize Diff: {np.average([ diffs[url]['accumulatedResposeBodySize'] for url in urls]) / 1000}KB")

print(f"\nMedian accumulatedResposeBodySize: {np.median([ data2[url]['accumulatedResposeBodySize'] for url in urls]) / 1000}KB")
print(f"Median accumulatedResposeBodySize Diff: {np.median([ diffs[url]['accumulatedResposeBodySize'] for url in urls]) / 1000}KB")