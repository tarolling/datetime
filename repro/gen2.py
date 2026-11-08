import sys
k, nf = int(sys.argv[1]), int(sys.argv[2])
name = "a_function_with_a_rather_long_name_to_grow_the_symbol_table_"
lines = [f"fn {name}{i}(x: int) -> int:\n    ret x + 1\n" for i in range(nf)]
lines.append('pad = "' + "x" * k + '"')
lines.append('s = "hello"')
lines.append("t = 0")
lines += [f"t = {name}{i}(t)" for i in range(nf)]
lines.append("print(s, pad.len(), t)")
open(f"big{k}_{nf}.stn", "w").write("\n".join(lines) + "\n")
