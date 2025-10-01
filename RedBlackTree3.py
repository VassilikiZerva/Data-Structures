#Red - Black Tree

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None
        self.color = 1  
        self.value = key  

class RedBlackTree:
    def __init__(self):
        self.NIL = Node(0)
        self.NIL.color = 0  
        self.NIL.left = None
        self.NIL.right = None
        self.root = self.NIL
        self.size = 0

    def insert(self, key):
        new_node = Node(key)
        new_node.left = self.NIL
        new_node.right = self.NIL
        
        y = None
        x = self.root
        
        while x != self.NIL:
            y = x
            if new_node.key < x.key:
                x = x.left
            else:
                x = x.right
        
        new_node.parent = y
        if y is None:
            self.root = new_node
        elif new_node.key < y.key:
            y.left = new_node
        else:
            y.right = new_node
            
        if new_node.parent is None:
            new_node.color = 0  
            self.size += 1
            return
            
        if new_node.parent.parent is None:
            self.size += 1
            return
            
        self._fix_insert(new_node)
        self.size += 1
        
    def delete(self, key):
        self._delete_node(self.search(key))
        
    def _delete_node(self, z):
        if z == self.NIL:
            return
            
        y = z
        y_original_color = y.color
        
        if z.left == self.NIL:
            x = z.right
            self._transplant(z, z.right)
        elif z.right == self.NIL:
            x = z.left
            self._transplant(z, z.left)
        else:
            y = self._minimum(z.right)
            y_original_color = y.color
            x = y.right
            
            if y.parent == z:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
                
            self._transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
            
        if y_original_color == 0:
            self._fix_delete(x)
        
        self.size -= 1
            
    def search(self, key):
        return self._search_helper(self.root, key)
        
    def _search_helper(self, node, key):
        if node == self.NIL:
            return self.NIL
            
        if key == node.key:
            return node
            
        if key < node.key:
            return self._search_helper(node.left, key)
        
        return self._search_helper(node.right, key)
    
    def _left_rotate(self, x):
        y = x.right
        x.right = y.left
        
        if y.left != self.NIL:
            y.left.parent = x
            
        y.parent = x.parent
        
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
            
        y.left = x
        x.parent = y
        
    def _right_rotate(self, x):
        y = x.left
        x.left = y.right
        
        if y.right != self.NIL:
            y.right.parent = x
            
        y.parent = x.parent
        
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
            
        y.right = x
        x.parent = y
        
    def _fix_insert(self, k):
        while k.parent and k.parent.color == 1:  
            if k.parent == k.parent.parent.right: 
                u = k.parent.parent.left  
                
                if u.color == 1:  
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:  
                    if k == k.parent.left:  
                        k = k.parent
                        self._right_rotate(k)
                    
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self._left_rotate(k.parent.parent)
            else:  
                u = k.parent.parent.right  
                
                if u.color == 1:  
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:  
                    if k == k.parent.right:  
                        k = k.parent
                        self._left_rotate(k)
                    
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self._right_rotate(k.parent.parent)
                    
            if k == self.root:
                break
                
        self.root.color = 0  
        
    def _fix_delete(self, x):
        while x != self.root and x.color == 0:
            if x == x.parent.left:
                s = x.parent.right
                if s.color == 1:
                    s.color = 0
                    x.parent.color = 1
                    self._left_rotate(x.parent)
                    s = x.parent.right

                if s.left.color == 0 and s.right.color == 0:
                    s.color = 1
                    x = x.parent
                else:
                    if s.right.color == 0:
                        s.left.color = 0
                        s.color = 1
                        self._right_rotate(s)
                        s = x.parent.right

                    s.color = x.parent.color
                    x.parent.color = 0
                    s.right.color = 0
                    self._left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == 1:
                    s.color = 0
                    x.parent.color = 1
                    self._right_rotate(x.parent)
                    s = x.parent.left

                if s.right.color == 0 and s.left.color == 0:
                    s.color = 1
                    x = x.parent
                else:
                    if s.left.color == 0:
                        s.right.color = 0
                        s.color = 1
                        self._left_rotate(s)
                        s = x.parent.left

                    s.color = x.parent.color
                    x.parent.color = 0
                    s.left.color = 0
                    self._right_rotate(x.parent)
                    x = self.root
                    
        x.color = 0
        
    def _transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
            
        v.parent = u.parent
        
    def _minimum(self, node):
        while node.left != self.NIL:
            node = node.left
        return node
        
    def __len__(self):
        return self.size