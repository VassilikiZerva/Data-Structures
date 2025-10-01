#Assignment6 : Binary Decision Diagram (BDD) - Testing

from BDD import BDD_create, BDD_create_with_best_order, BDD_use
import random
import time
import itertools

operators = ['and', 'or', 'not']

def generate_random_expression(variables):
    expr = []
    for _ in range(random.randint(1, 3 * len(variables))):
        choice = random.choice(variables + operators + ['(', ')'])
        if choice == 'not':
            var = random.choice(variables)
            expr.append(f'(not {var})')
        else:
            expr.append(choice)
    return ' '.join(expr)

def generate_input_combinations(n):
    return list(itertools.product([0, 1], repeat=n))

def test_bdd_system():
    max_vars = 13
    trials_per_var = 100
    for num_vars in range(2, max_vars + 1):
        variables = [chr(ord('A') + i) for i in range(num_vars)]
        print(f"\nTesting {num_vars} variables...")

        total_reduction = 0
        total_reduction_best = 0
        correct_count = 0
        total_time = 0

        for _ in range(trials_per_var):
            expr = generate_random_expression(variables)
            try:
                start = time.time()
                bdd = BDD_create(expr, variables)
                time1 = time.time() - start
                size_normal = bdd.size

                best_bdd = BDD_create_with_best_order(expr)
                size_best = best_bdd.size

                total_time += time1
                reduction = (2 ** num_vars - size_normal) / (2 ** num_vars)
                better_reduction = (size_normal - size_best) / size_normal

                total_reduction += reduction
                total_reduction_best += better_reduction

                for values in generate_input_combinations(num_vars):
                    input_str = ''.join(str(v) for v in values)
                    expected = eval(expr, {}, dict(zip(variables, values)))
                    result = BDD_use(bdd, input_str)
                    if str(int(bool(expected))) != result:
                        break
                else:
                    correct_count += 1
            except Exception as e:
                continue

        print(f"Average reduction: {total_reduction / trials_per_var:.2f}")
        print(f"Extra reduction by best order: {total_reduction_best / trials_per_var:.2f}")
        print(f"Correct BDDs: {correct_count}/{trials_per_var}")
        print(f"Average BDD_create time: {total_time / trials_per_var:.4f}s")

if __name__ == "__main__":
    test_bdd_system() 