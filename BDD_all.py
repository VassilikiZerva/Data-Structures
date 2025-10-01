#Assignment 6 : Binary Decision Diagram (BDD) 

import itertools
import time
import random

class BDDNode:
    def __init__(self, var=None, low=None, high=None, value=None):
        self.var = var      
        self.low = low      
        self.high = high    
        self.value = value  

class BDD:
    def __init__(self, root, variables, size):
        self.root = root
        self.variables = variables
        self.num_vars = len(variables)
        self.size = size

def eval_function(expr, var_assignments):
    try:
        return str(int(eval(expr, {}, var_assignments)))
    except:
        return None

def build_bdd(expr, variables, index, memo, assignment):
    if index == len(variables):
        result = eval_function(expr, assignment)
        return BDDNode(value=result)

    var = variables[index]
    key = (index, tuple(sorted(assignment.items())))
    if key in memo:
        return memo[key]

    assignment[var] = 0
    low = build_bdd(expr, variables, index + 1, memo, assignment.copy())

    assignment[var] = 1
    high = build_bdd(expr, variables, index + 1, memo, assignment.copy())

    if low.value == high.value and low.value is not None:
        return low

    node = BDDNode(var=var, low=low, high=high)
    memo[key] = node
    return node

def count_nodes(node, visited):
    if node in visited:
        return 0
    visited.add(node)
    if node.value is not None:
        return 1
    return 1 + count_nodes(node.low, visited) + count_nodes(node.high, visited)

def BDD_create(boolean_function, variable_order):
    memo = {}
    assignment = {}
    root = build_bdd(boolean_function, variable_order, 0, memo, assignment)
    size = count_nodes(root, set())
    return BDD(root, variable_order, size)

def generate_orders(variables):
    orders = []
    n = len(variables)
    for i in range(n):
        orders.append(variables[i:] + variables[:i])
    return orders

def BDD_create_with_best_order(boolean_function):
    variables = sorted(list({c for c in boolean_function if c.isalpha()}))
    orders = generate_orders(variables)

    best_bdd = None
    best_size = float('inf')

    for order in orders:
        bdd = BDD_create(boolean_function, order)
        if bdd.size < best_size:
            best_size = bdd.size
            best_bdd = bdd

    return best_bdd

def BDD_use(bdd, input_string):
    if len(input_string) != len(bdd.variables):
        return -1

    current = bdd.root
    var_index = {v: i for i, v in enumerate(bdd.variables)}

    while current.value is None:
        var = current.var
        idx = var_index[var]
        if input_string[idx] == '0':
            current = current.low
        elif input_string[idx] == '1':
            current = current.high
        else:
            return -1

    return current.value

def generate_random_expression(variables, num_clauses=3):
    expr = []
    for _ in range(num_clauses):
        clause = []
        for var in variables:
            if random.choice([True, False]):
                if random.choice([True, False]):
                    clause.append(f"not {var}")
                else:
                    clause.append(f"{var}")
        if clause:
            expr.append("(" + " and ".join(clause) + ")")
    return " or ".join(expr) if expr else "0"

def test_bdd_system(num_vars=5, num_tests=100):
    variables = [chr(65 + i) for i in range(num_vars)]
    total_reduction = 0
    total_extra_reduction = 0
    total_time_create = 0
    total_time_best = 0

    for _ in range(num_tests):
        expr = generate_random_expression(variables)

        start_time = time.time()
        bdd1 = BDD_create(expr, variables)
        end_time = time.time()
        total_time_create += end_time - start_time

        start_time = time.time()
        bdd2 = BDD_create_with_best_order(expr)
        end_time = time.time()
        total_time_best += end_time - start_time

        max_nodes = 2 ** num_vars
        reduction = (1 - bdd1.size / max_nodes) * 100
        extra_reduction = (1 - bdd2.size / bdd1.size) * 100

        total_reduction += reduction
        total_extra_reduction += extra_reduction

        for bits in itertools.product([0, 1], repeat=num_vars):
            input_str = ''.join(map(str, bits))
            var_dict = {variables[i]: bits[i] for i in range(num_vars)}
            expected = eval_function(expr, var_dict)
            got = BDD_use(bdd1, input_str)
            if expected != got:
                print("Mismatch:", expr, input_str, expected, got)

    print(f"Average reduction: {total_reduction / num_tests:.2f}%")
    print(f"Extra reduction with best order: {total_extra_reduction / num_tests:.2f}%")
    print(f"Average creation time (default order): {total_time_create / num_tests:.4f}s")
    print(f"Average creation time (best order): {total_time_best / num_tests:.4f}s")

test_bdd_system(num_vars=13, num_tests=100)