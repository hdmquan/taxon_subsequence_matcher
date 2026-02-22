# Yura

Find hidden subsequences in scientific names of all known flora and fauna.

A subsequence means letters appear **in order** but not necessarily adjacent — like finding `PAL` in `P`ine`A`pp`L`e.

Data source: [GBIF Backbone Taxonomy](https://www.gbif.org/dataset/d7dddbf4-2cf0-4f39-9b2a-bb099caae36c) (~7.7M taxa).

## Setup

```bash
chmod +x setup.sh && ./setup.sh
```

Requires: `poetry`, `curl`, `unzip`

## Usage

```bash
poetry run python3 find.py [sequence] [word_count] [flags]
```

| Argument | Default | Description |
|---|---|---|
| `sequence` | `shadowshape` | Subsequence to search for |
| `word_count` | any | Filter results to N-word names only |
| `--direct` | off | Allow direct/substring-like matches (by default, runs of more than 2 consecutive matched letters are filtered out) |
| `--no-format` | off | Disable match highlighting |

By default, results are formatted with matched letters **bolded and uppercased**, unmatched letters lowercased — e.g. `**P**ine**A**pp**L**e`.

## Examples

```bash
# default: shadowshape, any word count
poetry run python3 find.py

# 1-word names containing "raptor" subsequence (36 matches, direct runs filtered)
poetry run python3 find.py raptor 1
# RAmisPinaTispORa  →  R·A·mis·P·ina·T·isp·O·R·a
# CRasPedoTHORax   →  c·R·a·s·P·edo·T·h·O·R·ax
# BRaDyPTerOscaRta →  b·R·a·d·y·P·T·er·O·sca·R·ta

# 2-word names, no formatting, allow direct matches
poetry run python3 find.py shadow 2 --direct --no-format
```
