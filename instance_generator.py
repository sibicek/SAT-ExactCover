import random
import os
output_dir = "instances"
output_file_name = "complex_instance_unsat.in"
script_dir = os.path.dirname(os.path.abspath(__file__))
output_file = os.path.join(output_dir, output_file_name)

n = 200    # number of elements
m = 5*n   # number of subsets
min_size = min(1, n //20)
max_size = max(1, n //5)
force_correct = False  # force at least one solution

def split_number_of_correct_subsets(total, min_val, max_val):
    def backtrack(remaining, parts_left, current):
        if parts_left == 0:
            if remaining == 0:
                return current
            return None

        min_possible = parts_left * min_val
        max_possible = parts_left * max_val

        if remaining < min_possible or remaining > max_possible:
            return None

        for v in range(min_val, max_val + 1):
            r = backtrack(remaining - v, parts_left - 1, current + [v])
            if r is not None:
                return r
        
        return None

    k_min = (total + max_val - 1) // max_val
    k_max = total // min_val

    if k_min > k_max:
        return None

    k = random.randint(k_min, k_max)
    return backtrack(total, k, [])

subsets = []

if force_correct:
    # generate sizes of subsets that will cover all elements
    sizes = split_number_of_correct_subsets(n, min_size, max_size)

    # shuffle sizes for randomness
    random.shuffle(sizes)

    # shuffle elements
    elements = list(range(1, n + 1))
    random.shuffle(elements)

    # create subsets that cover all elements
    for size in sizes:
        subset = sorted(elements[:size])
        subsets.append(subset)
        elements = elements[size:]

    # add additional random subsets until we reach m
    while len(subsets) < m:
        size = random.randint(min_size, max_size)
        subset = sorted(random.sample(range(1, n + 1), size))
        subsets.append(subset)
else:
    for _ in range(m):
        size = random.randint(min_size, max_size)
        subset = sorted(random.sample(range(1, n + 1), size))
        subsets.append(subset)

# randomly shuffle the subsets
random.shuffle(subsets)

with open(output_file, "w") as output:
    output.write(f"{n} {m}\n")
    for s in subsets:
        output.write(" ".join(map(str, s)) + "\n")
