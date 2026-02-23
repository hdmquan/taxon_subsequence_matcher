#!/bin/bash
set -e

echo "Installing dependencies..."
poetry install

echo "Downloading GBIF backbone taxonomy (~926MB so uh)..."
curl -L "https://hosted-datasets.gbif.org/datasets/backbone/current/backbone.zip" -o backbone.zip

echo "Extracting..."
unzip -o backbone.zip -d backbone/

echo "Converting to parquet..."
poetry run python3 -c "
import polars as pl
df = pl.read_csv('backbone/Taxon.tsv', separator='\t', quote_char=None, infer_schema_length=0, ignore_errors=True)
df.write_parquet('taxon.parquet')
print(f'Done: {df.shape[0]:,} rows')
"

echo "Cleaning up..."
rm -rf backbone/ backbone.zip

echo "Ready. See: README.md. Run: poetry run python3 find.py <sequence> [word_count]"
