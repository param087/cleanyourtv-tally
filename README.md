# cleanyourtv-tally

A small Python script that reads every community debloat list in [CleanYourTV](https://github.com/Gathin23/cleanyourtv) (`examples/*/debloat.txt`) and counts which packages people switch off most, how much of that is Google versus the TV maker, and how many lists report a package that turns itself back on after a reboot.

## Run

```
git clone --depth 1 https://github.com/Gathin23/cleanyourtv
python3 tally.py cleanyourtv
```

Python 3.8+, no dependencies.

## What it found (upstream commit 065d5d1, 27 Oct 2026)

- 335 lists, 92 brands, median 22 packages per list, 1465 unique packages.
- The 9 most-disabled packages are all `com.google.*` (feedback in 247 lists, Play Games 203, Play Movies 144, recommendation rows 130).
- But Google is only 25% of all disable entries: the long tail is the TV maker's own apps.
- 36 lists note at least one package that re-enables itself at boot, so "disabled" is not always permanent.

Full output in `output.txt`. The "comes back" count is a text match on the list comments, so treat it as approximate.
