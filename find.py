import polars as pl
import sys
from multiprocessing import Pool, cpu_count

args = sys.argv[1:]
flags = {a for a in args if a.startswith("--")}
pos = [a for a in args if not a.startswith("--")]

SEQ = (pos[0] if len(pos) > 0 else "hameln").lower()
WORDS = int(pos[1]) if len(pos) > 1 else None
NO_DIRECT = "--direct" not in flags
FORMAT = "--no-format" not in flags

def match_positions(name: str, seq: str) -> list[int] | None:

    nl = name.lower()
    positions = []
    si = 0
    
    for i, c in enumerate(nl):
        
        if si < len(seq) and c == seq[si]:
            
            positions.append(i)
            si += 1
            
    return positions if si == len(seq) else None

def has_long_run(positions: list[int], limit: int = 2) -> bool:
    
    run = 1
    
    for i in range(1, len(positions)):
        
        if positions[i] == positions[i - 1] + 1:
            run += 1
            
            if run > limit:
                return True
            
        else:
            run = 1
            
    return False

def fmt(name: str, positions: list[int]) -> str:
    matched = set(positions)
    out = []
    i = 0
    while i < len(name):
        if i in matched:
            run = []
            while i < len(name) and i in matched:
                run.append(name[i].upper())
                i += 1
            out.append(f"**{''.join(run)}**")
        else:
            out.append(name[i].lower())
            i += 1
    return "".join(out)

def _check(args: tuple) -> list:
    
    names, seq, words, no_direct, do_fmt = args
    out = []
    
    for n in names:
        
        if words is not None and len(n.split()) != words:
            continue
        
        positions = match_positions(n, seq)
        
        if positions is None:
            continue
        
        if no_direct and has_long_run(positions):
            continue
        
        out.append(fmt(n, positions) if do_fmt else n)
        
    return out

def chunk(lst: list, n: int):
    
    k = len(lst) // n
    return [lst[i * k:(i + 1) * k] if i < n - 1 else lst[i * k:] for i in range(n)]

if __name__ == "__main__":
    
    names = pl.read_parquet("taxon.parquet").select("canonicalName").drop_nulls()["canonicalName"].to_list()
    workers = cpu_count()
    chunks = chunk(names, workers)
    
    with Pool(workers) as p:
        results = p.map(_check, [(c, SEQ, WORDS, NO_DIRECT, FORMAT) for c in chunks])
        
    hits = [n for r in results for n in r]
    word_label = f"{WORDS}-word" if WORDS else "any"
    
    print(f"Sequence: '{SEQ}' | Words: {word_label} | Matches: {len(hits)}")
    
    for h in hits:
        print(h)
