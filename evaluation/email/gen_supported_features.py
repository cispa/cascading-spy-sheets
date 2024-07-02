import csv
from collections import defaultdict

client_to_features = defaultdict(set)
with open("css-detection.csv", "r") as f:
    reader = csv.DictReader(f, delimiter=";")
    for line in reader:
        client, feature = line["client"], line["feature"]
        client_to_features[client].add(feature)


client_to_interesting_features = dict()
for client in client_to_features:
    features = client_to_features[client]
    deduplicated_features = set(
        map(
            lambda x: x.replace("-body", "").replace("-head", ""),
            filter(lambda x: "-external" not in x, features),
        )
    )
    external_features = set(
        map(
            lambda x: x.replace("-external", ""),
            filter(lambda x: "-external" in x, features),
        )
    )
    deduplicated_features = set(
        filter(lambda x: "sanity" not in x, deduplicated_features)
    )

    interesting_features = dict()
    interesting_features["html"] = len(
        list(filter(lambda x: "html" in x, deduplicated_features))
    )
    interesting_features["iframe"] = "iframe" in deduplicated_features
    interesting_features["@font-face"] = "font-face" in deduplicated_features
    interesting_features["@container"] = "container" in deduplicated_features
    interesting_features["@supports"] = "supports" in deduplicated_features
    interesting_features["@media"] = len(
        list(filter(lambda x: x.startswith("media"), deduplicated_features))
    )
    interesting_features["@media calc()"] = "media-width-calc" in deduplicated_features
    interesting_features["@font-face (ext)"] = (
        "font-face" in deduplicated_features.union(external_features)
    )
    interesting_features["@container (ext)"] = (
        "container" in deduplicated_features.union(external_features)
    )
    interesting_features["@supports (ext)"] = "supports" in deduplicated_features.union(
        external_features
    )
    interesting_features["@media (ext)"] = len(
        list(
            filter(
                lambda x: x.startswith("media"), deduplicated_features.union(external_features)
            )
        )
    )
    interesting_features["@media calc() (ext)"] = (
        "media-width-calc" in deduplicated_features.union(external_features)
    )
    interesting_features["total"] = len(deduplicated_features)
    interesting_features["total (ext)"] = len(
        deduplicated_features.union(external_features)
    )
    interesting_features["sanity"] = (
        "TODO"
        if "sanity-yes" not in features
        else (
            "PASS"
            if "sanity-yes" in features and "sanity-no" not in features
            else "FAIL"
        )
    )

    client_to_interesting_features[client] = interesting_features

# @media | @supports | @container
print(f"| {'Email Client':<20}| {'HTML':<5} | {'@media':<6} | {'Container':<10} | {'Supports':<10} | {'@media':<15} | {'Conclusion':<15} |")
#for client, interesting_features in sorted(
#    client_to_interesting_features.items(),
#    key=lambda x: x[1]["total (ext)"],
#    reverse=True,
#):

for client, interesting_features in client_to_interesting_features.items():
    # print(f"\n--- {client}:")
    # pprint.pprint(interesting_features)
    num_html = interesting_features["html"]
    num_media = interesting_features["@media (ext)"]
    num_container = interesting_features["@container (ext)"]
    num_media = interesting_features["@media (ext)"]
    supports = interesting_features["@supports (ext)"]
    os_fp = (
        interesting_features["iframe"]
        or interesting_features["@media calc() (ext)"]
        or interesting_features["@container (ext)"]
    )
    font_fp = (
        interesting_features["@font-face (ext)"]
        or interesting_features["@container (ext)"]
    )
    print_detect = "media-print" in client_to_features[client]
    proxy = False
    print(
        f"| {client:<20}| {num_html:<5} | {num_media:<6} | {num_container:<10} | {supports:<10} | {num_media:<15} | {''.join(['X' for _ in range(os_fp + font_fp + (not proxy))]):<15} |"
    )
    
#    import os
#    os.system("clear")
#    
#for client in client_to_interesting_features.keys():
#    print(f"{client} -> {client_to_interesting_features[client]['@media calc() (ext)']}")
    
    # print("")
    # pprint.pprint(client_to_features[client])

# print("\n")
# print(f"Number of clients that support iframes: {len(list(filter(lambda c_f: c_f[1]['iframe'], client_to_interesting_features.items())))} / {len(client_to_interesting_features)}")
# print(f"Number of clients that support @font-face: {len(list(filter(lambda c_f: c_f[1]['@font-face (ext)'], client_to_interesting_features.items())))} / {len(client_to_interesting_features)}")
# print(f"Number of clients that support @container: {len(list(filter(lambda c_f: c_f[1]['@container (ext)'], client_to_interesting_features.items())))} / {len(client_to_interesting_features)}")
# print(f"Number of clients that support @supports: {len(list(filter(lambda c_f: c_f[1]['@supports (ext)'], client_to_interesting_features.items())))} / {len(client_to_interesting_features)}")
# print(f"Number of clients that support @media calc(): {len(list(filter(lambda c_f: c_f[1]['@media calc() (ext)'], client_to_interesting_features.items())))} / {len(client_to_interesting_features)}")
