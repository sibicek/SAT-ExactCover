#!/usr/bin/env python3
import subprocess
from argparse import ArgumentParser

def load_instance(path):
    """Load Exact Cover instance from file."""
    with open(path, 'r') as f:
        lines = f.read().strip().splitlines()
    n, m = map(int, lines[0].split())
    rows = []
    for i in range(1, 1+m):
        if i >= len(lines):
            rows.append([])
        else:
            row = [int(x) for x in lines[i].split()] if lines[i].strip() else []
            rows.append(row)
    return n, m, rows

def encode(n, m, rows):
    """Encode Exact Cover instance into CNF clauses."""
    clauses = []
    covers = {e: [] for e in range(1, n+1)}
    for i, row in enumerate(rows, start=1):
        for e in row:
            if 1 <= e <= n:
                covers[e].append(i)

    # At least one
    for e in range(1, n+1):
        clause = covers[e].copy()
        clause.append(0)
        clauses.append(clause)

    # At most one
    for e in range(1, n+1):
        rows_list = covers[e]
        for i in range(len(rows_list)):
            for j in range(i+1, len(rows_list)):
                clauses.append([-rows_list[i], -rows_list[j], 0])

    num_vars = m
    return clauses, num_vars

def write_dimacs(path, clauses, num_vars):
    """Write CNF in DIMACS format to file."""
    with open(path, 'w') as f:
        f.write(f"p cnf {num_vars} {len(clauses)}\n")
        for cl in clauses:
            f.write(' '.join(str(lit) for lit in cl) + '\n')

def call_solver(cnf_path, solver_binary="./glucose-simple"):
    """Call Glucose solver and return completed process."""
    cmd = [solver_binary, '-model', cnf_path]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc


def parse_model(proc):
    """Parse SAT model returned by Glucose."""
    out = proc.stdout.decode('utf-8', errors='ignore')
    model = []
    for line in out.splitlines():
        line = line.strip()
        if line.startswith('v '):
            parts = line.split()[1:]
            for lit in parts:
                val = int(lit)
                if val != 0:
                    model.append(val)
    chosen_rows = [v for v in model if v > 0]
    return chosen_rows, out

def print_result(proc, rows, cnf, verb=0):
    """Print SAT result; if verb==1, also print CNF and solver stdout."""
    if verb == 1 and cnf is not None:
        print("### CNF formula (DIMACS) ###")
        for clause in cnf:
            print(" ".join(str(lit) for lit in clause))
        print("############################\n")
    
    stdout_text = proc.stdout.decode('utf-8')
    stderr_text = proc.stderr.decode('utf-8')
    
    if verb == 1:
        print("### Solver output ###")
        print(stdout_text)
        print(stderr_text)
        print("####################\n")
    
    if proc.returncode == 20:
        print("UNSAT")
    elif proc.returncode == 10:

        model = []
        for line in stdout_text.splitlines():
            if line.startswith("v "):
                model.extend(int(x) for x in line.split()[1:] if int(x) != 0)
        chosen_rows = [v for v in model if v > 0]
        print("SAT")
        print("Chosen rows (1-based):", sorted(chosen_rows))
        print("\nSelected subsets:")
        for r in sorted(chosen_rows):
            print(f"Row {r}: {rows[r-1]}")
    else:
        print("Solver returned code", proc.returncode)
        print(stdout_text)
        print(stderr_text)

def main():
    parser = ArgumentParser()

    parser.add_argument(
        "-i", "--input",
        default="instance.in",
        type=str,
        help="The instance file.",
    )
    parser.add_argument(
        "-o", "--output",
        default="formula.cnf",
        type=str,
        help="Output file for the DIMACS format.",
    )
    parser.add_argument(
        "-s", "--solver",
        default="./glucose-simp",
        type=str,
        help="The SAT solver to be used.",
    )
    parser.add_argument(
        "-v","--verb",
        default=0,
        type=int,
        choices=range(0,2),
        help=(
            "Verbosity of the SAT solver used."
        ),
    )

    args = parser.parse_args()

    print(f"Loading instance: {args.input}")
    n, m, rows = load_instance(args.input)

    cnf, num_vars = encode(n, m, rows)

    write_dimacs(args.output, cnf, num_vars)
    proc = call_solver(args.output, args.solver)

    print_result(proc, rows, cnf, args.verb)

if __name__ == "__main__":
    main()
