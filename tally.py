#!/usr/bin/env python3
"""Tally the community debloat lists in a CleanYourTV checkout.

Usage: python3 tally.py <path-to-cleanyourtv-checkout>
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

PACKAGE_LINE = re.compile(r"^([a-zA-Z][\w]*(?:\.[\w]+)+)\s*(?:#.*)?$")
COMES_BACK = re.compile(r"(comes back|re-?enabled at (every )?boot|re-?enables itself|back on after (a )?reboot)", re.I)
NOT_A_RETURN = re.compile(r"nothing|no package|ADB comes back|keyboard comes back", re.I)
MEM = re.compile(r"MemAvailable went from (\d+) MB to (?:about )?(\d+) MB")


def read_list(path):
    text = path.read_text(errors="replace")
    packages = [m.group(1) for line in text.splitlines() if (m := PACKAGE_LINE.match(line.strip()))]
    return text, packages


def main(root):
    examples = Path(root) / "examples"
    package_counts, brand_counts = Counter(), Counter()
    sizes, mem_gains, comes_back = [], [], []
    lists = sorted(examples.glob("*/debloat.txt"))
    for path in lists:
        text, packages = read_list(path)
        sizes.append(len(packages))
        package_counts.update(set(packages))
        meta = path.parent / "tv.json"
        if meta.exists():
            brand_counts[json.loads(meta.read_text()).get("brand", "?")] += 1
        if any(COMES_BACK.search(l) and not NOT_A_RETURN.search(l) for l in text.splitlines()):
            comes_back.append(path.parent.name)
        for before, after in MEM.findall(text):
            mem_gains.append(int(after) - int(before))

    entries = sum(package_counts.values())
    google = sum(n for p, n in package_counts.items() if p.startswith("com.google."))
    sizes.sort()
    print(f"lists: {len(lists)}  brands: {len(brand_counts)}")
    print(f"packages per list: median {sizes[len(sizes)//2]}, max {sizes[-1]}, total unique {len(package_counts)}")
    print(f"com.google.* share of all disable entries: {google}/{entries} ({100*google/entries:.0f}%)")
    print(f"lists noting a package that comes back after reboot: {len(comes_back)}")
    if mem_gains:
        mem_gains.sort()
        print(f"MemAvailable gain reported in {len(mem_gains)} lists: median +{mem_gains[len(mem_gains)//2]} MB")
    print("\ntop brands:", ", ".join(f"{b} {n}" for b, n in brand_counts.most_common(8)))
    print("\nmost-disabled packages:")
    for package, n in package_counts.most_common(15):
        print(f"{n:4d}  {package}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
