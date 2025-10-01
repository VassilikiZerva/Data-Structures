# DSA Assignment 5 - Searching in Dynamic Sets
# Implementation and Performance Comparison of Different Data Structures

import time
import random
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
import sys

# Increase the recursion limit (a temporary fix if needed)
sys.setrecursionlimit(10000)

# ========================== Binary Search Tree ==========================
class BSTNode:
    def __init__(self, key, value=None):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None
        self.size = 0

    def insert(self, key, value=None):
        """Insert a key-value pair into the BST"""
        if self.root is None:
            self.root = BSTNode(key, value)
            self.size += 1
            return True

        current = self.root
        while True:
            if key == current.key:
                # Key already exists, update value
                current.value = value
                return False  # No new node was added
            elif key < current.key:
                if current.left is None:
                    current.left = BSTNode(key, value)
                    self.size += 1
                    return True
                current = current.left
            else:  # key > current.key
                if current.right is None:
                    current.right = BSTNode(key, value)
                    self.size += 1
                    return True
                current = current.right

    def search(self, key):
        """Search for a key in the BST, return the value or None if not found"""
        current = self.root
        while current is not None:
            if key == current.key:
                return current.value
            elif key < current.key:
                current = current.left
            else:  # key > current.key
                current = current.right
        return None

    def _find_min(self, node):
        """Find the minimum key in the subtree rooted at node"""
        current = node
        while current.left is not None:
            current = current.left
        return current

    def delete(self, key):
        """Delete a key from the BST using an iterative approach with parent pointers"""
        if not self.root:
            return False

        # Find the node to delete and its parent
        parent = None
        current = self.root
        is_left_child = False

        # Find the node
        while current is not None and current.key != key:
            parent = current
            if key < current.key:
                current = current.left
                is_left_child = True
            else:
                current = current.right
                is_left_child = False

        # If the key doesn't exist
        if current is None:
            return False

        # Case 1: Node has no children
        if current.left is None and current.right is None:
            if current == self.root:
                self.root = None
            elif is_left_child:
                parent.left = None
            else:
                parent.right = None

        # Case 2a: Node has only a right child
        elif current.left is None:
            if current == self.root:
                self.root = current.right
            elif is_left_child:
                parent.left = current.right
            else:
                parent.right = current.right

        # Case 2b: Node has only a left child
        elif current.right is None:
            if current == self.root:
                self.root = current.left
            elif is_left_child:
                parent.left = current.left
            else:
                parent.right = current.left

        # Case 3: Node has both children
        else:
            # Find the successor (minimum value in right subtree)
            successor = self._find_min(current.right)

            # If the successor is the right child
            if current.right == successor:
                successor.left = current.left
                if current == self.root:
                    self.root = successor
                elif is_left_child:
                    parent.left = successor
                else:
                    parent.right = successor
            else:
                # Find successor's parent
                successor_parent = current
                temp = current.right
                while temp != successor:
                    successor_parent = temp
                    temp = temp.left

                # Remove successor from its position
                successor_parent.left = successor.right

                # Put successor in place of current
                successor.left = current.left
                successor.right = current.right

                if current == self.root:
                    self.root = successor
                elif is_left_child:
                    parent.left = successor
                else:
                    parent.right = successor

        self.size -= 1
        return True

# ========================== Red-Black Tree ==========================
# Colors for Red-Black tree nodes
RED = True
BLACK = False

class RBNode:
    def __init__(self, key, value=None, color=RED):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.color = color

class RedBlackTree:
    def __init__(self):
        self.root = None
        self.size = 0

    def is_red(self, node):
        if node is None:
            return False
        return node.color == RED

    def rotate_left(self, h):
        x = h.right
        h.right = x.left
        x.left = h
        x.color = h.color
        h.color = RED
        return x

    def rotate_right(self, h):
        x = h.left
        h.left = x.right
        x.right = h
        x.color = h.color
        h.color = RED
        return x

    def flip_colors(self, h):
        h.color = RED
        h.left.color = BLACK
        h.right.color = BLACK

    def insert(self, key, value=None):
        """Insert a key-value pair into the Red-Black tree"""
        def _insert(node, key, value):
            if node is None:
                self.size += 1
                return RBNode(key, value)

            if key < node.key:
                node.left = _insert(node.left, key, value)
            elif key > node.key:
                node.right = _insert(node.right, key, value)
            else:  # key == node.key
                node.value = value
                return node

            # Balance the tree
            if self.is_red(node.right) and not self.is_red(node.left):
                node = self.rotate_left(node)
            if self.is_red(node.left) and self.is_red(node.left.left):
                node = self.rotate_right(node)
            if self.is_red(node.left) and self.is_red(node.right):
                self.flip_colors(node)

            return node

        old_size = self.size
        self.root = _insert(self.root, key, value)
        self.root.color = BLACK  # Root must be black
        return old_size != self.size  # Return True if a new node was added

    def search(self, key):
        """Search for a key in the Red-Black tree"""
        current = self.root
        while current is not None:
            if key == current.key:
                return current.value
            elif key < current.key:
                current = current.left
            else:  # key > current.key
                current = current.right
        return None

    # We'll simplify the Red-Black Tree delete operation to avoid recursion depth issues
    def delete(self, key):
        """Delete a key from the Red-Black tree - simplified version"""
        if not self.search(key):
            return False

        # Find the node and delete it
        # For simplicity, we'll use a less efficient but more stable approach
        # that doesn't rely on deep recursion
        temp_tree = RedBlackTree()
        stack = []
        current = self.root

        # Traverse the tree and collect all nodes except the one to delete
        while current or stack:
            if current:
                if current.key != key:
                    temp_tree.insert(current.key, current.value)
                if current.right:
                    stack.append(current.right)
                current = current.left
            else:
                current = stack.pop()

        # Replace this tree with the temp tree
        self.root = temp_tree.root
        self.size = temp_tree.size

        return True

# ========================== Hash Table with Open Addressing ==========================
class HashTable:
    def __init__(self, initial_capacity=16, load_factor=0.75):
        self.capacity = initial_capacity
        self.size = 0
        self.table = [None] * self.capacity
        self.deleted = object()  # Sentinel for deleted slots
        self.load_factor = load_factor

    def _hash1(self, key):
        """Primary hash function"""
        return hash(key) % self.capacity

    def _hash2(self, key):
        """Secondary hash function for double hashing"""
        # Make sure the second hash is odd and non-zero
        return 2 * (hash(key) % ((self.capacity // 2) or 1)) + 1

    def _find_slot(self, key):
        """Find the slot for a key using double hashing"""
        hash1 = self._hash1(key)
        hash2 = self._hash2(key)
        i = 0

        # Limit probing to capacity to avoid infinite loops
        while i < self.capacity:
            index = (hash1 + i * hash2) % self.capacity
            if self.table[index] is None:
                return index, False  # Found an empty slot
            if self.table[index] is self.deleted:
                # Found a deleted slot, can be used for insert but not for search
                deleted_index = index
                i += 1
                continue
            if self.table[index][0] == key:
                return index, True  # Found the key
            i += 1

        # If we've checked all slots and found a deleted slot, return it
        if 'deleted_index' in locals():
            return deleted_index, False

        # Table is full/no slot found (should not happen if we resize properly)
        return None, False

    def _resize(self, new_capacity):
        """Resize the hash table"""
        old_table = self.table
        self.capacity = new_capacity
        self.table = [None] * self.capacity
        old_size = self.size
        self.size = 0

        # Re-insert all entries from the old table
        for item in old_table:
            if item is not None and item is not self.deleted:
                self.insert(item[0], item[1])

    def insert(self, key, value=None):
        """Insert a key-value pair into the hash table"""
        # Check if resizing is needed
        if (self.size + 1) / self.capacity > self.load_factor:
            self._resize(2 * self.capacity)

        index, found = self._find_slot(key)
        if index is None:  # Should not happen with proper resizing
            return False

        if found:
            # Update existing key
            self.table[index] = (key, value)
            return False
        else:
            # Insert new key
            self.table[index] = (key, value)
            self.size += 1
            return True

    def search(self, key):
        """Search for a key in the hash table"""
        hash1 = self._hash1(key)
        hash2 = self._hash2(key)
        i = 0

        while i < self.capacity:
            index = (hash1 + i * hash2) % self.capacity
            if self.table[index] is None:
                return None  # Key not found
            if self.table[index] is not self.deleted and self.table[index][0] == key:
                return self.table[index][1]  # Return the value
            i += 1

        return None  # Key not found after checking all possible positions

    def delete(self, key):
        """Delete a key from the hash table"""
        hash1 = self._hash1(key)
        hash2 = self._hash2(key)
        i = 0

        while i < self.capacity:
            index = (hash1 + i * hash2) % self.capacity
            if self.table[index] is None:
                return False  # Key not found
            if self.table[index] is not self.deleted and self.table[index][0] == key:
                self.table[index] = self.deleted
                self.size -= 1

                # Resize if needed (if load factor gets too low)
                if self.size > 0 and self.capacity > 16 and self.size / self.capacity < 0.25:
                    self._resize(self.capacity // 2)

                return True
            i += 1

        return False  # Key not found

# ========================== Testing Framework ==========================
def generate_random_operations(n_operations, keys_range=(0, 1000000), operation_ratios={'insert': 0.33, 'search': 0.33, 'delete': 0.34}):
    """Generate a list of random operations: insert, search, delete"""
    operations = []
    keys_set = set()  # Keep track of keys for more realistic testing

    for _ in range(n_operations):
        op_type = random.choices(
            ['insert', 'search', 'delete'],
            weights=[operation_ratios['insert'], operation_ratios['search'], operation_ratios['delete']]
        )[0]

        if op_type == 'insert':
            # For insert, we prefer a new key
            if len(keys_set) > 0 and random.random() < 0.2:  # 20% chance to reinsert existing key
                key = random.choice(list(keys_set))
            else:
                key = random.randint(*keys_range)
                keys_set.add(key)
            operations.append(('insert', key))

        elif op_type == 'search':
            # For search, we prefer an existing key but sometimes try non-existent
            if len(keys_set) > 0 and random.random() < 0.8:  # 80% chance to search existing key
                key = random.choice(list(keys_set))
            else:
                key = random.randint(*keys_range)
            operations.append(('search', key))

        elif op_type == 'delete':
            # For delete, we prefer an existing key but sometimes try non-existent
            if len(keys_set) > 0 and random.random() < 0.8:  # 80% chance to delete existing key
                key = random.choice(list(keys_set))
                keys_set.discard(key)  # Using discard instead of remove in case key not in set
            else:
                key = random.randint(*keys_range)
            operations.append(('delete', key))

    return operations

def test_data_structure(ds_name, ds_class, operations):
    """Test a data structure with a sequence of operations"""
    ds = ds_class()
    times = []

    for op, key in operations:
        start_time = time.time()

        if op == 'insert':
            ds.insert(key)
        elif op == 'search':
            ds.search(key)
        elif op == 'delete':
            ds.delete(key)

        end_time = time.time()
        times.append(end_time - start_time)

    # Calculate statistics
    avg_time = sum(times) / len(times)
    return {
        'ds_name': ds_name,
        'total_time': sum(times),
        'avg_time': avg_time,
        'min_time': min(times),
        'max_time': max(times),
        'times': times
    }

def test_operation_types(ds_name, ds_class, operations):
    """Test a data structure and separately measure times for each operation type"""
    ds = ds_class()
    times = {'insert': [], 'search': [], 'delete': []}

    for op, key in operations:
        start_time = time.time()

        if op == 'insert':
            ds.insert(key)
        elif op == 'search':
            ds.search(key)
        elif op == 'delete':
            ds.delete(key)

        end_time = time.time()
        times[op].append(end_time - start_time)

    # Calculate statistics
    stats = {'ds_name': ds_name}
    for op in times:
        if times[op]:  # Check if there are any operations of this type
            stats[f'{op}_total'] = sum(times[op])
            stats[f'{op}_avg'] = sum(times[op]) / len(times[op])
            stats[f'{op}_min'] = min(times[op])
            stats[f'{op}_max'] = max(times[op])

    return stats

def run_size_scaling_test(data_structures, sizes, operations_per_size=100):
    """Test how data structures scale with different input sizes"""
    results = defaultdict(list)

    for size in sizes:
        print(f"Testing with size {size}...")
        # Generate operations with the desired mix of operations
        operations = generate_random_operations(operations_per_size)

        # First, perform inserts to populate data structures
        setup_operations = [('insert', i) for i in range(size)]

        for ds_name, ds_class in data_structures:
            print(f"  Testing {ds_name}...")
            ds = ds_class()

            # Setup phase: insert initial data
            for op, key in setup_operations:
                ds.insert(key)

            # Measurement phase
            start_time = time.time()
            for op, key in operations:
                if op == 'insert':
                    ds.insert(key)
                elif op == 'search':
                    ds.search(key)
                elif op == 'delete':
                    ds.delete(key)
            end_time = time.time()

            avg_time = (end_time - start_time) / operations_per_size
            results[ds_name].append(avg_time)

    return results, sizes

def run_operation_ratio_test(data_structures, ratios, size=10000, operations_per_test=1000):
    """Test data structures with different operation type ratios"""
    results = []

    for ratio_name, ratio in ratios.items():
        print(f"Testing with ratio {ratio_name}...")
        # Generate operations with the desired mix of operations
        operations = generate_random_operations(operations_per_test, operation_ratios=ratio)

        # First, perform inserts to populate data structures
        setup_operations = [('insert', i) for i in range(size)]

        ratio_results = {'ratio_name': ratio_name}
        for ds_name, ds_class in data_structures:
            print(f"  Testing {ds_name}...")
            ds = ds_class()

            # Setup phase: insert initial data
            for op, key in setup_operations:
                ds.insert(key)

            # Measure separate operation types
            times = {'insert': [], 'search': [], 'delete': []}

            for op, key in operations:
                start_time = time.time()

                if op == 'insert':
                    ds.insert(key)
                elif op == 'search':
                    ds.search(key)
                elif op == 'delete':
                    ds.delete(key)

                end_time = time.time()
                times[op].append(end_time - start_time)

            # Calculate averages
            for op in times:
                if times[op]:  # Check if there are any operations of this type
                    ratio_results[f'{ds_name}_{op}_avg'] = sum(times[op]) / len(times[op])

        results.append(ratio_results)

    return results

def plot_scaling_results(results, sizes):
    """Plot how data structures scale with input size"""
    plt.figure(figsize=(12, 8))

    for ds_name, times in results.items():
        plt.plot(sizes, times, marker='o', label=ds_name)

    plt.xlabel('Initial Data Structure Size')
    plt.ylabel('Average Operation Time (seconds)')
    plt.title('Data Structure Performance Scaling with Size')
    plt.legend()
    plt.grid(True)
    plt.savefig('scaling_results.png')
    plt.show()

def plot_operation_ratio_results(results):
    """Plot performance for different operation ratios"""
    ds_names = set()
    op_types = ['insert', 'search', 'delete']
    ratio_names = [r['ratio_name'] for r in results]

    # Identify all data structure names
    for result in results:
        for key in result:
            if '_avg' in key:
                ds_name = key.split('_')[0]
                ds_names.add(ds_name)

    # Create grouped bar charts for each operation type
    for op_type in op_types:
        plt.figure(figsize=(12, 8))
        bar_width = 0.8 / len(ds_names)
        index = np.arange(len(ratio_names))

        for i, ds_name in enumerate(sorted(ds_names)):
            times = []
            for result in results:
                key = f"{ds_name}_{op_type}_avg"
                if key in result:
                    times.append(result[key])
                else:
                    times.append(0)  # No operations of this type in this test

            plt.bar(index + i * bar_width, times, bar_width, label=ds_name)

        plt.xlabel('Operation Ratio Profile')
        plt.ylabel('Average Operation Time (seconds)')
        plt.title(f'Performance for {op_type.capitalize()} Operations')
        plt.xticks(index + bar_width * (len(ds_names) - 1) / 2, ratio_names)
        plt.legend()
        plt.grid(True, axis='y')
        plt.savefig(f'{op_type}_ratio_results.png')
        plt.show()

# ========================== Main Testing Function ==========================
def main():
    # Define the data structures to test
    data_structures = [
        ('BST', BinarySearchTree),
        ('Red-Black Tree', RedBlackTree),
        ('Hash Table', HashTable)
    ]

    print("Running tests for different data structure sizes...")
    # Define sizes to test (reduced for faster testing)
    sizes = [100, 1000, 5000, 10000, 20000]
    scaling_results, sizes = run_size_scaling_test(data_structures, sizes)

    print("Running tests for different operation ratios...")
    # Define different operation ratios to test
    operation_ratios = {
        'balanced': {'insert': 0.33, 'search': 0.33, 'delete': 0.34},
        'insert_heavy': {'insert': 0.6, 'search': 0.2, 'delete': 0.2},
        'search_heavy': {'insert': 0.2, 'search': 0.6, 'delete': 0.2},
        'delete_heavy': {'insert': 0.2, 'search': 0.2, 'delete': 0.6}
    }
    ratio_results = run_operation_ratio_test(data_structures, operation_ratios, size=5000)

    # Plot the results
    print("Plotting results...")
    plot_scaling_results(scaling_results, sizes)
    plot_operation_ratio_results(ratio_results)

    print("Tests completed!")

if __name__ == "__main__":
      main()