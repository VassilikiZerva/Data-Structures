#Hash Table 

class HashTable:
    def __init__(self, initial_capacity=8, load_factor=0.75):
        self.capacity = initial_capacity
        self.size = 0
        self.table = [None] * self.capacity
        self.load_factor = load_factor
        self.DELETED = object()
        
        self.collision_count = 0
        self.probe_count = 0
    
    def _hash1(self, key):
        """Primary hash function"""
        return hash(key) % self.capacity
    
    def _hash2(self, key):
        """Secondary hash function for double hashing""" 
        return 1 + (hash(key) % (self.capacity - 1))
    
    def _get_position(self, key):
        """Find the position where key should be stored or is stored"""
        h1 = self._hash1(key)
        h2 = self._hash2(key)
        
        i = 0
        pos = h1
        
        while self.table[pos] is not None and self.table[pos] is not self.DELETED and self.table[pos][0] != key:
            self.probe_count += 1
            
            if i > 0:  
                self.collision_count += 1
                
            i += 1
            pos = (h1 + i * h2) % self.capacity
            
            if i >= self.capacity:
                return -1
                
        return pos
    
    def insert(self, key, value=None):
        """Insert a key-value pair into the hash table"""
        if (self.size + 1) / self.capacity > self.load_factor:
            self._resize(self.capacity * 2)
        
        pos = self._get_position(key)
        
        if self.table[pos] is not None and self.table[pos] is not self.DELETED and self.table[pos][0] == key:
            self.table[pos] = (key, value)
            return
        
        self.table[pos] = (key, value)
        self.size += 1
    
    def search(self, key):
        """Search for a key in the hash table"""
        pos = self._get_position(key)
        
        if pos != -1 and self.table[pos] is not None and self.table[pos] is not self.DELETED:
            return self.table[pos][1]  
        
        return None  
    
    def delete(self, key):
        """Delete a key from the hash table"""
        pos = self._get_position(key)
        
        if pos != -1 and self.table[pos] is not None and self.table[pos] is not self.DELETED:
            self.table[pos] = self.DELETED
            self.size -= 1
            
            if self.size > 0 and self.capacity > 8 and self.size / self.capacity < self.load_factor / 4:
                self._resize(self.capacity // 2)
                
            return True
        
        return False 
    
    def _resize(self, new_capacity):
        """Resize the hash table"""
        old_table = self.table
        
        self.capacity = new_capacity
        self.table = [None] * self.capacity
        old_size = self.size
        self.size = 0
        self.collision_count = 0
        self.probe_count = 0
        
        for entry in old_table:
            if entry is not None and entry is not self.DELETED:
                self.insert(entry[0], entry[1])
                
        if self.size != old_size:
            self.size = old_size
    
    def __len__(self):
        return self.size
    
    def get_stats(self):
        """Return statistics about the hash table operations"""
        return {
            "size": self.size,
            "capacity": self.capacity,
            "load_factor": self.size / self.capacity if self.capacity > 0 else 0,
            "collisions": self.collision_count,
            "probes": self.probe_count
        }
    
    def reset_stats(self):
        """Reset the collision and probe counters"""
        self.collision_count = 0
        self.probe_count = 0