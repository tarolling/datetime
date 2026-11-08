"""Writes globs<N>.stn: N top-level string globals, then a print. Usage: gen.py N..."""
import sys

for n in map(int, sys.argv[1:]):
    lines = [f'g{i} = "s{i}"' for i in range(n)]
    lines.append("t = 0")
    lines += [f"t += g{i}.len()" for i in range(n)]
    lines.append('print("total {t}")')
    with open(f"globs{n}.stn", "w") as f:
        f.write("\n".join(lines) + "\n")
