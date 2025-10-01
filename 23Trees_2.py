#2-3 Tree

class TwoThreeNode:
    def __init__(self, keys=None, children=None):
        self.keys = keys if keys else []
        self.children = children if children else []
        self.parent = None
    
    def is_leaf(self):
        return len(self.children) == 0
    
    def is_full(self):
        return len(self.keys) == 2
    
    def add_key(self, key):
        """Add a key to the node, maintaining sorted order"""
        self.keys.append(key)
        self.keys.sort()
    
    def add_child(self, child):
        """Add a child to the node, maintaining sorted order"""
        self.children.append(child)
        self.children.sort(key=lambda x: x.keys[0])
        child.parent = self

class TwoThreeTree:
    def __init__(self):
        self.root = None
        self.size = 0
    
    def search(self, key):
        """Search for a key in the tree"""
        if not self.root:
            return False
        
        return self._search_recursive(self.root, key)
    
    def _search_recursive(self, node, key):
        """Helper method for recursive search"""
        if key in node.keys:
            return True
        
        if node.is_leaf():
            return False
        
        if key < node.keys[0]:
            return self._search_recursive(node.children[0], key)
        elif len(node.keys) == 1 or key < node.keys[1]:
            return self._search_recursive(node.children[1], key)
        else:
            return self._search_recursive(node.children[2], key)
    
    def insert(self, key):
        """Insert a key into the tree"""
        if not self.root:
            self.root = TwoThreeNode([key])
            self.size += 1
            return
        
        leaf = self._find_leaf_for_insertion(self.root, key)
        
        if key in leaf.keys:
            return  
        
        self._insert_in_node(leaf, key, None)
        self.size += 1
    
    def _find_leaf_for_insertion(self, node, key):
        """Find the leaf node where key should be inserted"""
        if node.is_leaf():
            return node
        
        if key < node.keys[0]:
            return self._find_leaf_for_insertion(node.children[0], key)
        elif len(node.keys) == 1 or key < node.keys[1]:
            return self._find_leaf_for_insertion(node.children[1], key)
        else:
            return self._find_leaf_for_insertion(node.children[2], key)
    
    def _insert_in_node(self, node, key, right_child):
        """Insert key and optionally a right child into node, splits if necessary"""
        if key in node.keys:
            return  
        
        node.add_key(key)
        
        if right_child:
            idx = node.keys.index(key) + 1
            if idx < len(node.children):
                node.children.insert(idx, right_child)
            else:
                node.add_child(right_child)
            right_child.parent = node
    
        if not node.is_full() or len(node.keys) <= 2:
            return
        
        self._split_node(node)
    
    def _split_node(self, node):
        """Split a full node into two nodes"""
        middle_key = node.keys[1]
        
        right_node = TwoThreeNode([node.keys[2]], [])
        
        if not node.is_leaf():
            right_node.children = node.children[2:]
            for child in right_node.children:
                child.parent = right_node
            node.children = node.children[:2]
        
        node.keys = [node.keys[0]]
        
        if not node.parent:
            new_root = TwoThreeNode([middle_key], [node, right_node])
            self.root = new_root
            node.parent = new_root
            right_node.parent = new_root
        else:
            parent = node.parent
            self._insert_in_node(parent, middle_key, right_node)
    
    def delete(self, key):
        """Delete a key from the tree"""
        if not self.root:
            return
        
        node, idx = self._find_node_with_key(self.root, key)
        
        if not node:
            return  
        
        self.size -= 1
        
        if node.is_leaf():
            self._delete_from_leaf(node, idx)
        else:
            successor_node, successor_idx = self._find_successor(node, idx)
            node.keys[idx] = successor_node.keys[successor_idx]
            self._delete_from_leaf(successor_node, successor_idx)
    
    def _find_node_with_key(self, node, key):
        """Find node containing key and its index"""
        if key in node.keys:
            return node, node.keys.index(key)
        
        if node.is_leaf():
            return None, -1
        
        if key < node.keys[0]:
            return self._find_node_with_key(node.children[0], key)
        elif len(node.keys) == 1 or key < node.keys[1]:
            return self._find_node_with_key(node.children[1], key)
        else:
            return self._find_node_with_key(node.children[2], key)
    
    def _find_successor(self, node, idx):
        """Find the successor (smallest value in right subtree)"""
        child = node.children[idx + 1]
        while not child.is_leaf():
            child = child.children[0]
        return child, 0
    
    def _delete_from_leaf(self, node, idx):
        """Delete key at index from leaf node"""
        node.keys.pop(idx)
        
        if len(node.keys) > 0 or node == self.root:
            if len(node.keys) == 0 and len(node.children) == 0:
                self.root = None
            return
        
        self._rebalance(node)
    
    def _rebalance(self, node):
        """Rebalance tree after deletion"""
        if not node.parent:  
            if len(node.keys) == 0 and len(node.children) == 1:
                self.root = node.children[0]
                self.root.parent = None
            return
        
        parent = node.parent
        idx = parent.children.index(node)
        
        if idx > 0 and len(parent.children[idx-1].keys) > 1:  
            self._borrow_from_left(node, idx)
        elif idx < len(parent.children) - 1 and len(parent.children[idx+1].keys) > 1:  
            self._borrow_from_right(node, idx)
        else:  
            if idx > 0:  
                self._merge_with_left(node, idx)
            else:  
                self._merge_with_right(node, idx)
    
    def _borrow_from_left(self, node, idx):
        """Borrow a key from left sibling"""
        parent = node.parent
        left_sibling = parent.children[idx-1]
        
        node.keys.insert(0, parent.keys[idx-1])
        
        parent.keys[idx-1] = left_sibling.keys.pop()
        
        if not left_sibling.is_leaf():
            child = left_sibling.children.pop()
            node.children.insert(0, child)
            child.parent = node
    
    def _borrow_from_right(self, node, idx):
        """Borrow a key from right sibling"""
        parent = node.parent
        right_sibling = parent.children[idx+1]
        
        node.keys.append(parent.keys[idx])
        
        parent.keys[idx] = right_sibling.keys.pop(0)

        if not right_sibling.is_leaf():
            child = right_sibling.children.pop(0)
            node.children.append(child)
            child.parent = node
    
    def _merge_with_left(self, node, idx):
        """Merge node with its left sibling"""
        parent = node.parent
        left_sibling = parent.children[idx-1]
        
        left_sibling.keys.append(parent.keys.pop(idx-1))
        
        left_sibling.keys.extend(node.keys)
        if not node.is_leaf():
            left_sibling.children.extend(node.children)
            for child in node.children:
                child.parent = left_sibling
        
        parent.children.pop(idx)
        
        if len(parent.keys) == 0 and parent == self.root:
            self.root = left_sibling
            left_sibling.parent = None
        elif len(parent.keys) < 1:
            self._rebalance(parent)
    
    def _merge_with_right(self, node, idx):
        """Merge node with its right sibling"""
        parent = node.parent
        right_sibling = parent.children[idx+1]
        
        node.keys.append(parent.keys.pop(idx))
        
        node.keys.extend(right_sibling.keys)
        if not right_sibling.is_leaf():
            node.children.extend(right_sibling.children)
            for child in right_sibling.children:
                child.parent = node
        
        parent.children.pop(idx+1)
        
        if len(parent.keys) == 0 and parent == self.root:
            self.root = node
            node.parent = None
        elif len(parent.keys) < 1:
            self._rebalance(parent)
    
    def __len__(self):
        return self.size