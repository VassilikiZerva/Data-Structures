#Assignment6 : Binary Decision Diagram (BDD)

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
    def __init__(self, num_vars, root):
        self.num_vars = num_vars
        self.root = root
        self.size = self.count_nodes(root)

    def count_nodes(self, node, visited=None):
        if visited is None:
            visited = set()
        if node is None or node in visited:
            return 0
        visited.add(node)
        if node.value is not None:
            return 1
        return 1 + self.count_nodes(node.low, visited) + self.count_nodes(node.high, visited)

def evaluate_expression(expr, inputs):
    try:
        env = {var: val for var, val in inputs.items()}
        return eval(expr, {}, env)
    except:
        return -1

def build_bdd(expr, vars_order, memo, inputs={}):
    key = (tuple(sorted(inputs.items())))
    if key in memo:
        return memo[key]

    if len(inputs) == len(vars_order):
        val = evaluate_expression(expr, inputs)
        node = BDDNode(value=str(int(bool(val))))
        memo[key] = node
        return node

    var = vars_order[len(inputs)]
    inputs0 = inputs.copy()
    inputs0[var] = 0
    low = build_bdd(expr, vars_order, memo, inputs0)

    inputs1 = inputs.copy()
    inputs1[var] = 1
    high = build_bdd(expr, vars_order, memo, inputs1)

    if low == high:
        memo[key] = low
        return low

    node = BDDNode(var=var, low=low, high=high)
    memo[key] = node
    return node

def BDD_create(bfunction, order):
    memo = {}
    root = build_bdd(bfunction, order, memo)
    return BDD(num_vars=len(order), root=root)

def BDD_use(bdd, inputs):
    node = bdd.root
    if len(inputs) != bdd.num_vars:
        return -1
    while node.value is None:
        index = bdd_order.index(node.var)
        val = inputs[index]
        if val == '0':
            node = node.low
        elif val == '1':
            node = node.high
        else:
            return -1
    return node.value

def generate_orders(variables, num_orders=None):
    if num_orders is None or num_orders >= len(list(itertools.permutations(variables))):
        return list(itertools.permutations(variables))
    orders = set()
    while len(orders) < num_orders:
        orders.add(tuple(random.sample(variables, len(variables))))
    return list(orders)

def BDD_create_with_best_order(bfunction):
    variables = sorted(set(filter(str.isalpha, bfunction)))
    orders = generate_orders(variables, max(10, len(variables)))
    best_bdd = None
    min_size = float('inf')
    for order in orders:
        bdd = BDD_create(bfunction, list(order))
        if bdd.size < min_size:
            min_size = bdd.size
            best_bdd = bdd
    return best_bdd 